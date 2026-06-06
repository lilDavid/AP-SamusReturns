import shutil
from collections.abc import Sequence
from enum import StrEnum
from pathlib import Path
from typing import Self

import settings

from . import patch


class RomFile(settings.UserFilePath):
    """File name of the Metroid: Samus Returns ROM."""

    description = "Metroid: Samus Returns ROM file (decrypted format)"

    def browse(self, filetypes: Sequence[tuple[str, Sequence[str]]] | None = None, **kwargs) -> Self | None:
        # Pared down from FilePath.browse() just so we can support multiple file types
        if filetypes is None:
            filetypes = (("3DS ROM image", (".cia", ".3ds", ".cci", ".app", ".cxi")),)
        result = super().browse(filetypes, **kwargs)
        if result is None:
            return None
        destination = self.__class__(f"Metroid Samus Returns{Path(result).suffix}")
        shutil.copy(result, destination.resolve(), follow_symlinks=True)
        return destination

    @classmethod
    def validate(cls, path: str):
        match patch.get_title_id(path):
            case patch.TITLE_ID_US | patch.TITLE_ID_EU:
                pass
            case patch.TITLE_ID_JP:
                raise ValueError("The JP version of Metroid: Samus Returns is not supported")
            case title_id:
                raise ValueError(
                    f"Invalid title ID: expected {patch.TITLE_ID_US} or {patch.TITLE_ID_EU}, got {title_id}"
                )


class TargetSystem(StrEnum):
    """
    Set this to "console" or "emulator" to automatically place randomizer files
    in the matching path and start the emulator if appropriate. This setting
    also determines what IP address the client will try to look for by default.
    """

    CONSOLE = "console"
    EMULATOR = "emulator"


class ConsoleSdPath(settings.FolderPath):
    """
    3DS SD card root. If set, the patcher can automatically place randomizer
    files into <SD>/luma/titles/<game id>.
    """

    description = "3DS SD card path"


class ConsoleIp(str):
    """
    Your 3DS's local IP address. You can find this by opening the Homebrew
    Launcher and pressing the Y button.
    """


class EmulatorUserPath(settings.FolderPath):
    """
    Azahar user path. If set, the patcher can automatically place randomizer
    files into <Azahar path>/load/mods/<game id>.
    """

    description = "Azahar user path"


class EmulatorRomStart(str):
    """
    Set this to false to never autostart a ROM (such as after patching).
    Set it to true to have the operating system default program open the ROM.
    Alternatively, set it to a path to a program to open your ROM with.
    """


class TrackerTrickLogic(StrEnum):
    """
    Controls what tricks will show as Glitched accessible in Universal Tracker.
    Set this to "next_level" to show locations reachable with tricks set one
    level above the selected difficulty. Set it to "all" to show locations
    reachable with any tricks that aren't already in logic.
    """

    NEXT_LEVEL = "next_level"
    ALL = "all"


class TrackerExplainPoNR(settings.Bool):
    """
    Set this to true to explain the rules required to cross points of no return
    in Universal Tracker. Set it to false to only display that you need to
    escape the area.
    """


class ConsoleSettings(settings.Group):
    sd_path: ConsoleSdPath | None = None
    ip_address: ConsoleIp | None = None


class EmulatorSettings(settings.Group):
    user_path: EmulatorUserPath | None = None
    rom_start: EmulatorRomStart | bool = True


class TrackerSettings(settings.Group):
    show_tricks: TrackerTrickLogic = TrackerTrickLogic.NEXT_LEVEL
    explain_ponr: TrackerExplainPoNR | bool = True


class SamusReturnsSettings(settings.Group):
    rom_file: RomFile = RomFile(RomFile.copy_to)
    target_system: TargetSystem = TargetSystem.EMULATOR
    console_settings: ConsoleSettings = ConsoleSettings()
    emulator_settings: EmulatorSettings = EmulatorSettings()
    universal_tracker_settings: TrackerSettings = TrackerSettings()
