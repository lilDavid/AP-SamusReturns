from collections.abc import Sequence
from enum import StrEnum
from typing import ClassVar, Self

import settings

from .patch import MD5_US_DECRYPTED


class RomFile(settings.UserFilePath):
    """File name of the Metroid: Samus Returns ROM."""

    description = "Metroid: Samus Returns ROM file (decrypted format)"
    copy_to = "Metroid Samus Returns.cci"
    md5s: ClassVar[list[str | bytes]] = [MD5_US_DECRYPTED]

    def browse(self, filetypes: Sequence[tuple[str, Sequence[str]]] | None = None, **kwargs) -> Self | None:
        if filetypes is None:
            filetypes = (("3DS ROM image", (".3ds", ".cci")),)
        return super().browse(filetypes, **kwargs)


class ConsoleSdPath(settings.UserFolderPath):
    """
    3DS SD card root. If set, the patcher can automatically place randomizer
    files into <SD>/luma/titles/<game id>.
    """

    description = "3DS SD card path"


class ConsoleIp(str):
    """
    Your 3DS's local IP address. You can find this ***.
    """


class EmulatorUserPath(settings.UserFolderPath):
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


class TargetSystem(StrEnum):
    """
    Set this to "console" or "emulator" to automatically place randomizer files
    in the matching path and start the emulator if appropriate. This setting
    also determines what IP address the client will try to look for by default.
    """

    CONSOLE = "console"
    EMULATOR = "emulator"


class ConsoleSettings(settings.Group):
    sd_path: ConsoleSdPath | None = None
    ip_address: ConsoleIp | None = None


class EmulatorSettings(settings.Group):
    user_path: EmulatorUserPath | None = None
    rom_start: EmulatorRomStart | bool = True


class SamusReturnsSettings(settings.Group):
    rom_file: RomFile = RomFile(RomFile.copy_to)
    console_settings: ConsoleSettings = ConsoleSettings()
    emulator_settings: EmulatorSettings = EmulatorSettings()
    target_system: TargetSystem = TargetSystem.EMULATOR
