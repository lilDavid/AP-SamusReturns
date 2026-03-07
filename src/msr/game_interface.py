import asyncio
import pkgutil
import struct
from collections.abc import Sequence
from dataclasses import dataclass
from enum import IntEnum, IntFlag

from CommonClient import logger

from .data.internal_names import AreaId, ItemId

UUID_LENGTH = 36  # 32 hex digits + 4 hyphens


def get_lua_file(file):
    lua = pkgutil.get_data(__name__, f"data/lua/{file}")
    assert lua is not None
    return lua


SR_PORT = 42069


TIMEOUT = 5.0
BOOTSTRAP_BACKOFF = 1.0
DEBUG_PREVIEW_LENGTH = 32


class PacketType(IntEnum):
    HANDSHAKE = 1
    LOG_MESSAGE = 2
    REMOTE_LUA_EXEC = 3
    NEW_INVENTORY = 5
    COLLECTED_INDICES = 6
    RECEIVED_ITEMS = 7
    GAME_STATE = 8
    MALFORMED = 9


class Subscription(IntFlag):
    LOGGING = 1
    MULTIWORLD = 2


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
            self.streams = await asyncio.wait_for(asyncio.open_connection(self.address, SR_PORT), 10)
        except TimeoutError:
            logger.debug("Connection failed: Timeout")
            self.disconnect()
            return False
        except OSError as e:
            logger.debug(f"Connection failed: {e}")
            self.disconnect()
            return False

        return True

    def disconnect(self):
        if self.streams is not None:
            self.streams[1].close()
        self.streams = None
        self.request_number = 0

    async def send_msg(self, packet: PacketType, data: bytes | bytearray):
        if self.streams is None:
            raise OSError("Not connected")

        writer = self.streams[1]
        try:
            msg = struct.pack(">B", packet) + data
            logger.debug("> %s %s (%d bytes)", packet.name, data[:DEBUG_PREVIEW_LENGTH], len(msg))
            assert len(msg) <= 4096
            writer.write(msg)
            await writer.drain()
        except OSError:
            self.disconnect()
            raise

    async def read_msg(self):
        if self.streams is None:
            raise OSError("Not connected")
        reader = self.streams[0]

        p = await reader.read(1)
        if p == b"":
            self.disconnect()
            raise OSError("Connection closed")

        _packet = p[0]
        try:
            packet = PacketType(_packet)
        except ValueError:
            self.disconnect()
            raise Exception(f"Unrecognized packet type {_packet}") from None

        logger.debug("< %s", packet.name)
        match packet:
            case PacketType.HANDSHAKE:
                _sequence = (await reader.read(1))[0]
                data = ""
            case PacketType.REMOTE_LUA_EXEC:
                _sequence, _success, size = struct.unpack("<BBI", await reader.read(6))
                data = (await reader.read(size)).decode("utf-8", errors="replace")
            case (
                PacketType.LOG_MESSAGE
                | PacketType.NEW_INVENTORY
                | PacketType.COLLECTED_INDICES
                | PacketType.RECEIVED_ITEMS
                | PacketType.GAME_STATE
            ):
                size = struct.unpack("<I", await reader.read(4))[0]
                data = (await reader.read(size)).decode("utf-8", errors="replace")
            case PacketType.MALFORMED:
                type, received, expected = struct.unpack("<BII", await reader.read(9))
                self.disconnect()
                raise Exception(
                    f"Game was sent a {PacketType(type)} malformed packet, received {received} expected {expected}"
                )
        return packet, data

    async def receive_msgs(self):
        if self.streams is None:
            raise OSError("Not connected")

        reader = self.streams[0]
        while reader == self.streams[0]:
            yield await self.read_msg()

    async def run_lua(self, code: str | bytes):
        if isinstance(code, str):
            code_bytes = code.encode()
        else:
            code_bytes = code
        payload = struct.pack("<I", len(code_bytes)) + code_bytes
        await self.send_msg(PacketType.REMOTE_LUA_EXEC, payload)


@dataclass
class SamusReturnsState:
    config_id: str | None = None
    scenario: AreaId | None = None

    def is_in_game(self):
        return self.scenario is not None


LOCATION_BATCH_SIZE = 80


class SamusReturnsInterface:
    connector: SamusReturnsConnector
    game_state: SamusReturnsState
    game_task: asyncio.Task | None

    def __init__(self):
        self.connector = SamusReturnsConnector()
        self.game_state = SamusReturnsState()
        self.game_task = None

    def is_connected(self):
        return self.connector.is_connected()

    async def connect(self, address: str):
        if self.is_connected():
            return True
        if not await self.connector.connect(address):
            self.disconnect()
            return False

        try:
            await self.connector.send_msg(
                PacketType.HANDSHAKE,
                struct.pack("<B", Subscription.LOGGING | Subscription.MULTIWORLD),
            )
            await self.connector.read_msg()

            await self.load_rando_code()
            await self.connector.read_msg()

            await self.connector.run_lua('Game.AddSF(2.0, RL.SendRandoIdentifier, "")')
            await self.connector.read_msg()
            await self.connector.run_lua('Game.AddSF(2.0, RL.UpdateRDVClient, "")')
            await self.connector.read_msg()

            self.game_task = asyncio.Task(self.read_messages(), name="Samus Returns Connector")
        except OSError:
            self.disconnect()
            return False

        return True

    def disconnect(self):
        self.connector.disconnect()
        self.game_task = None

    async def load_rando_code(self):
        await self.connector.run_lua(get_lua_file("bootstrap.lua"))

    async def read_messages(self):
        async for msg in self.connector.receive_msgs():
            try:
                packet, data = msg
                logger.debug("%s", data)
                match packet:
                    case PacketType.GAME_STATE:
                        key, value = data.split(":")
                        match key:
                            case "rando_id":
                                self.game_state.config_id = value[:-UUID_LENGTH]
                            case "scenario":
                                try:
                                    self.game_state.scenario = AreaId(value)
                                except ValueError:
                                    self.game_state.scenario = None
                            case _:
                                logger.debug("Unrecognized game state key: %s", key)
            except Exception:
                import traceback

                traceback.print_exc()

    async def get_locations(self):
        return None

    async def get_inventory(self):
        return None

    async def give_items(self, items: Sequence[tuple[ItemId, int]]):
        return

    async def display_hud_message(self, text: str):
        return
