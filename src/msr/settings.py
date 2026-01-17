from collections.abc import Sequence
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


class RomStart(str):
    """
    Set this to false to never autostart a ROM (such as after patching).
    Set it to true to have the operating system default program open the ROM.
    Alternatively, set it to a path to a program to open your ROM with.
    """


class SamusReturnsSettings(settings.Group):
    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: RomStart | bool = True
