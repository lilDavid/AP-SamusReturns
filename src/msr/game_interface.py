import asyncio
import struct
from enum import IntEnum

from CommonClient import logger

from .data.internal_names import AreaId

SR_PORT = 42069


TIMEOUT = 5.0


class PacketType(IntEnum):
    HANDSHAKE = 1
    LOG_MESSAGE = 2
    REMOTE_LUA_EXEC = 3
    NEW_INVENTORY = 5
    COLLECTED_INDICES = 6
    RECEIVED_ITEMS = 7
    GAME_STATE = 8
    MALFORMED = 9


MULTIWORLD_SUBSCRIPTION = 2


class LuaError(RuntimeError):
    pass


class SamusReturnsConnector:
    address: str | None
    streams: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None
    lock: asyncio.Lock
    request_number: int

    def __init__(self):
        self.address = None
        self.streams = None
        self.lock = asyncio.Lock()
        self.request_number = 0

    def is_connected(self):
        return self.streams is not None

    async def connect(self, address: str):
        if self.is_connected() and address == self.address:
            return True
        self.disconnect()
        self.address = address

        try:
            self.streams = await asyncio.open_connection(self.address, SR_PORT)
            await self._request(PacketType.HANDSHAKE, struct.pack("<B", 0))
        except OSError as e:
            logger.debug(str(e))
            self.disconnect()
            return False

        return True

    def disconnect(self):
        if self.streams is not None:
            self.streams[1].close()
        self.streams = None
        self.request_number = 0

    async def _request(self, packet: PacketType, data: bytes | bytearray) -> bytes:
        async with self.lock:
            if self.streams is None:
                raise OSError("Not connected")
            reader, writer = self.streams

            try:
                request = struct.pack(">B", packet) + data
                assert len(request) <= 4096
                writer.write(request)
                await asyncio.wait_for(writer.drain(), timeout=5)
                response = await asyncio.wait_for(reader.read(4096), timeout=5)

                if response == b"":
                    raise OSError("Connection closed")

                response_packet, sequence = response[:2]
                if response_packet != packet or sequence != self.request_number:
                    raise OSError("Unexpected response")

                self.request_number += 1
                self.request_number &= 0xFF
                return response[2:]
            except OSError:
                self.disconnect()
                raise

    async def run_lua(self, code: str | bytes):
        if isinstance(code, str):
            code_bytes = code.encode()
        else:
            code_bytes = code
        payload = struct.pack("<I", len(code_bytes)) + code_bytes
        try:
            response = await self._request(PacketType.REMOTE_LUA_EXEC, payload)
        except TimeoutError:
            return None
        success, _ = struct.unpack_from("<BI", response)
        data = response[struct.calcsize("<BI") :].decode()
        if not success:
            raise LuaError(data)
        return data


class SamusReturnsInterface:
    connector: SamusReturnsConnector

    def __init__(self):
        self.connector = SamusReturnsConnector()

    def is_connected(self):
        return self.connector.is_connected()

    async def connect(self, address: str):
        return await self.connector.connect(address)

    def disconnect(self):
        self.connector.disconnect()

    async def is_in_game(self):
        scenario = await self.connector.run_lua("return Scenario.CurrentScenarioID")
        try:
            AreaId(scenario)
            return True
        except ValueError:
            return False

    async def display_hud_message(self, text: str):
        await self.connector.run_lua(f"Scenario.QueueAsyncPopup({text!r})")
