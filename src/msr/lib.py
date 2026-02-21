import importlib.util
import shutil
import sys
import zipfile
from collections.abc import Sequence
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType

import Utils


class SamusReturnsLibFinder(MetaPathFinder):
    """Lazily copies the contents of the lib path in this apworld into the AP cache dir"""

    checked_cache: bool
    module_cache: set[str] | None
    loaded: bool

    def __init__(self):
        self.checked_cache = False
        self.module_cache = None
        self.loaded = False

    def find_spec(
        self, fullname: str, path: Sequence[str] | None, target: ModuleType | None = None
    ) -> ModuleSpec | None:
        from . import SamusReturnsWorld

        if self.loaded:
            return None

        world = Path(__file__).parent
        apworld = zipfile.ZipFile(world.parent)

        # If cached, use that if the version matches
        cached_lib = Path(Utils.cache_path(f"{world.name}/lib"))
        if not self.checked_cache:
            self.checked_cache = True
            try:
                with open(cached_lib / "VERSION.txt") as version:
                    cache_version = Utils.tuplize_version(version.read())
                if cache_version == SamusReturnsWorld.world_version:
                    self.loaded = True
                    sys.path.append(str(cached_lib))
                    return importlib.util.find_spec(fullname)
            except FileNotFoundError:
                pass

        lib = zipfile.Path(apworld, f"{world.name}/lib/")

        # Try to wait until importer actually needs something from us (read: OSSR)
        if self.module_cache is None:
            self.module_cache = {
                path.stem if path.suffix == ".py" else path.name
                for path in lib.iterdir()
                if path.suffix != ".dist-info"
            }
        if fullname not in self.module_cache:
            return None

        # Extract the dependencies
        self.loaded = True

        try:
            shutil.rmtree(cached_lib)
        except FileNotFoundError:
            pass
        cached_lib.mkdir(parents=True, exist_ok=True)

        apworld.extractall(
            Utils.cache_path(),
            [name for name in apworld.namelist() if name.startswith(f"{world.name}/lib/")],
        )
        with open(cached_lib / "VERSION.txt", "w") as version:
            version.write(SamusReturnsWorld.world_version.as_simple_string())

        sys.path.append(str(cached_lib))
        return importlib.util.find_spec(fullname)


if zipfile.is_zipfile(Path(__file__).parents[1]):
    sys.meta_path.append(SamusReturnsLibFinder())
