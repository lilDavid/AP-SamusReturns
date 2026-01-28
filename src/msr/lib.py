import importlib.util
import sys
import zipfile
from collections.abc import Sequence
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType


class SamusReturnsLibFinder(MetaPathFinder):
    """Lazily copies the contents of the lib path in this apworld into a temp dir"""

    module_cache: set[str] | None
    loaded: bool

    def __init__(self):
        self.module_cache = None
        self.loaded = False

    def find_spec(
        self, fullname: str, path: Sequence[str] | None, target: ModuleType | None = None
    ) -> ModuleSpec | None:
        if self.loaded:
            return None

        world = Path(__file__).parent
        apworld = zipfile.ZipFile(world.parent)
        lib = zipfile.Path(apworld, f"{world.name}/lib/")

        if self.module_cache is None:
            self.module_cache = {
                path.stem if path.suffix == ".py" else path.name
                for path in lib.iterdir()
                if path.suffix != ".dist-info"
            }
        if fullname not in self.module_cache:
            return None

        import tempfile

        self.loaded = True
        temp_dir = Path(tempfile.mkdtemp())
        apworld.extractall(temp_dir, [name for name in apworld.namelist() if name.startswith(f"{world.name}/lib/")])
        sys.path.append(str(temp_dir / f"{world.name}/lib"))
        return importlib.util.find_spec(fullname)


if zipfile.is_zipfile(Path(__file__).parents[1]):
    sys.meta_path.append(SamusReturnsLibFinder())
