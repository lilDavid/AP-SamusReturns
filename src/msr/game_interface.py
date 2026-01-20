import asyncio
import pkgutil
import struct
from collections import Counter
from collections.abc import Sequence
from enum import IntEnum

from CommonClient import logger
from open_samus_returns_rando import lua_editor as osrr_lua

from . import items, locations
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
            self.streams = await asyncio.wait_for(asyncio.open_connection(self.address, SR_PORT), 10)
            await self._request(PacketType.HANDSHAKE, struct.pack("<B", 0))
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

    async def _request(self, packet: PacketType, data: bytes | bytearray) -> bytes:
        async with self.lock:
            if self.streams is None:
                raise OSError("Not connected")
            reader, writer = self.streams

            try:
                request = struct.pack(">B", packet) + data
                logger.debug(f"> {packet.name} {data[:DEBUG_PREVIEW_LENGTH]} ({len(request)} bytes)")
                assert len(request) <= 4096
                writer.write(request)
                await asyncio.wait_for(writer.drain(), timeout=5)
                response = await asyncio.wait_for(reader.read(4096), timeout=5)
                logger.debug(f"< {response[:DEBUG_PREVIEW_LENGTH]} ({len(response)} bytes)")

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


LOCATION_BATCH_SIZE = 80


class SamusReturnsInterface:
    connector: SamusReturnsConnector

    def __init__(self):
        self.connector = SamusReturnsConnector()

    def is_connected(self):
        return self.connector.is_connected()

    async def connect(self, address: str):
        if self.is_connected():
            return True
        return await self.connector.connect(address)

    def disconnect(self):
        self.connector.disconnect()

    async def get_config_identifier(self):
        rando_id = await self.connector.run_lua("return Init.sThisRandoIdentifier")
        if rando_id is None:
            return None
        return rando_id[:-UUID_LENGTH]

    async def load_rando_code(self):
        # Bootstrap
        if await self.connector.run_lua("return AP") != "nil":
            # Already loaded (we don't expect the code to change between DC and reconnect)
            return

        await self.connector.run_lua(get_lua_file("bootstrap.lua"))

        location_data = [
            (location.ap_id, location.scenario, location.internal_name())
            for location in locations.location_table.values()
        ]
        batches = [
            location_data[i : i + LOCATION_BATCH_SIZE] for i in range(0, len(location_data), LOCATION_BATCH_SIZE)
        ]
        template = "for k, v in pairs({}) do AP.LocationMapping[k] = v end"
        for batch in batches:
            table = "{"
            for id, scenario, name in batch:
                table += f'[{id}]={{"{scenario}","{name}"}},'
            table += "}"
            code = template.format(table)
            await self.connector.run_lua(code)

        code = "AP.ItemMapping = {"
        for item in items.item_data_table.values():
            code += f'[{item.ap_id}] = "{item.item_id}",'
        code += "}"
        await self.connector.run_lua(code)

    async def is_in_game(self):
        return await self.get_area() is not None

    async def get_area(self):
        result = await self.connector.run_lua("return Game.GetCurrentGameModeID() .. ';' .. Scenario.CurrentScenarioID")
        if result is None:
            return None
        game_mode, scenario = result.split(";")
        if game_mode != "INGAME":
            return None
        try:
            return AreaId(scenario)
        except ValueError:
            logger.debug(f"Unrecognized scenario: {scenario}")
            return None

    async def get_locations(self):
        result = await self.connector.run_lua("return AP.CheckLocations()")
        if result is None:
            return None
        locations: set[int] = {int(id) for id in result.split(",")} if result else set()
        logger.debug(f"Got location list: {locations}")
        return locations

    async def get_inventory(self):
        from . import SamusReturnsWorld

        result = await self.connector.run_lua("return AP.GetInventory()")
        if result is None:
            return None
        pairs = (map(int, kvp.split("=")) for kvp in result.split(","))
        inventory = Counter({SamusReturnsWorld.item_id_to_name[id]: count for id, count in pairs})
        logger.debug(f"Current inventory: {inventory}")
        return inventory

    async def give_items(self, items: Sequence[tuple[ItemId, int]]):
        resources = ",".join([f'{{item_id="{item}",quantity={amount}}}' for item, amount in items])
        await self.connector.run_lua(f"{osrr_lua.get_parent_for(items[0][0])}.OnPickedUp({{ {{ {resources} }} }})")

    async def display_hud_message(self, text: str):
        await self.connector.run_lua(f"Scenario.QueueAsyncPopup({text!r})")
