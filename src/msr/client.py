from __future__ import annotations

import asyncio
import logging
import traceback

import Patch
import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from kvui import GameManager

from .data.constants import GAME_NAME
from .game_interface import LuaError, SamusReturnsInterface

OTHER_WORLD_ITEMS = 0b001


BACKOFF_LONG = 3.0
BACKOFF_SHORT = 1.0
POLL_COOLDOWN = 0.5


class SamusReturnsManager(GameManager):
    base_title = "Archipelago Metroid: Samus Returns Client"


class SamusReturnsFilter(logging.Filter):
    last_message: str | None

    def __init__(self):
        self.last_message = None

    def clear(self):
        self.last_message = None

    def filter(self, record: logging.LogRecord):
        matches = record.getMessage() == self.last_message
        if matches:
            return False
        self.last_message = record.getMessage()
        return True


class SamusReturnsCommandProcessor(ClientCommandProcessor):
    ctx: SamusReturnsContext

    # def _cmd_test_lua(self, *code: str):
    #     """Run some Lua code in the game."""
    #     joined_code = " ".join(code)
    #     Utils.async_start(self.ctx.test_lua(joined_code))

    def _cmd_test_hud(self, *text: str):
        """Write a message to the HUD."""
        Utils.async_start(self.ctx.game_interface.display_hud_message(" ".join(text)))


class SamusReturnsContext(CommonContext):
    game = GAME_NAME
    command_processor = SamusReturnsCommandProcessor
    items_handling = OTHER_WORLD_ITEMS

    log_filter: SamusReturnsFilter

    game_sync_task: asyncio.Task
    game_interface: SamusReturnsInterface

    def __init__(self, server_address: str | None, password: str | None):
        super().__init__(server_address, password)

        self.log_filter = SamusReturnsFilter()
        logger.addFilter(self.log_filter)
        self.game_interface = SamusReturnsInterface()

    def run_gui(self):
        ui = SamusReturnsManager(self)
        self.ui = ui
        self.ui_task = asyncio.create_task(ui.async_run(), name="UI")

    async def game_sync_loop(self):
        logger.debug("Starting Samus Returns connector, attempting to connect to game")
        while not self.exit_event.is_set():
            try:
                if not self.game_interface.is_connected():
                    if await self.game_interface.connect("localhost"):
                        logger.debug("Connected")
                    else:
                        await asyncio.sleep(BACKOFF_LONG)
                        continue

                # if not self.server:
                #     logger.info("Waiting for player to connect to server")
                #     await asyncio.sleep(BACKOFF_SHORT)
                #     continue
                # if not self.slot:
                #     logger.debug("Waiting for slot")
                #     await asyncio.sleep(BACKOFF_SHORT)
                #     continue

                if await self.game_interface.is_in_game():
                    await self.handle_game_ready()
                    await asyncio.sleep(POLL_COOLDOWN)
                else:
                    await asyncio.sleep(BACKOFF_SHORT)
            except OSError as e:
                logger.error(str(e))
                await asyncio.sleep(BACKOFF_LONG)
            except Exception:
                logger.error(traceback.format_exc())
                await asyncio.sleep(BACKOFF_LONG)

    async def handle_game_ready(self):
        logger.debug("In-game stub")

    async def test_lua(self, code: str):
        try:
            result = await self.game_interface.connector.run_lua(code)
            logger.info(result)
        except (OSError, LuaError) as e:
            logger.exception(str(e))


def launch_game(rom_file: str):
    import subprocess
    import webbrowser

    from . import SamusReturnsWorld

    auto_start: str | bool = SamusReturnsWorld.settings.emulator_settings.auto_start

    if isinstance(auto_start, str):
        subprocess.Popen([auto_start, rom_file], close_fds=True)
    elif auto_start:
        webbrowser.open(rom_file)


def launch(*launch_args: str):
    async def main():
        parser = get_base_parser()
        parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an apmsr patch")
        args = parser.parse_args(launch_args)

        if args.patch_file:
            metadata, result_file = Patch.create_rom_file(args.patch_file)
            logger.info(f"Patch with meta-data {metadata} was written to {result_file}")
            if "server" in metadata:
                args.connect = metadata["server"]
            launch_game(result_file)

        ctx = SamusReturnsContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.game_sync_task = asyncio.create_task(ctx.game_sync_loop(), name="Samus Returns Sync")

        await ctx.exit_event.wait()
        await ctx.shutdown()
        await ctx.game_sync_task

    import logging

    import colorama

    Utils.init_logging("Metroid: Samus Returns Client", exception_logger="Client", loglevel=logging.DEBUG)
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
