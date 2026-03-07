import asyncio
import pkgutil
import struct
from enum import IntEnum, IntFlag

from CommonClient import logger

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


class SRConnectorError(RuntimeError):
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
            raise SRConnectorError("Not connected")

        writer = self.streams[1]
        try:
            msg = struct.pack(">B", packet) + data
            logger.debug("> %s %s (%d bytes)", packet.name, data[:DEBUG_PREVIEW_LENGTH], len(msg))
            assert len(msg) <= 4096
            writer.write(msg)
            await writer.drain()
        except OSError as e:
            self.disconnect()
            raise SRConnectorError(*e.args) from None

    async def read_msg(self):
        if self.streams is None:
            raise SRConnectorError("Not connected")
        reader = self.streams[0]

        p = await reader.read(1)
        if p == b"":
            self.disconnect()
            raise SRConnectorError("Connection closed")

        _packet = p[0]
        try:
            packet = PacketType(_packet)
        except ValueError:
            self.disconnect()
            raise SRConnectorError(f"Unrecognized packet type {_packet}") from None

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
                raise SRConnectorError(
                    f"Game was sent a {PacketType(type)} malformed packet, received {received} expected {expected}"
                )
        return packet, data

    async def receive_msgs(self):
        if self.streams is None:
            raise SRConnectorError("Not connected")

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
