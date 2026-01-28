#!/usr/bin/env python3

import json
import logging
import os
import shutil
import subprocess
import sys
import zipfile
from argparse import ArgumentParser
from pathlib import Path

# TODO: Support 3.14 once Lupa does
PYTHON_VERSIONS = ["3.11", "3.12", "3.13"]

PLATFORMS = {
    "win_amd64": ["win_amd64"],
    "macosx_x86_64": ["macosx_11_0_universal", "macosx_11_0_x86_64"],
    "macosx_arm64": ["macosx_11_0_universal", "macosx_11_0_arm64"],
    "linux_x86_64": ["manylinux_2_28_x86_64", "manylinux_2_17_x86_64"],
}

WORLD_NAME = "msr"

BASE_PATH = Path(__file__).parent
WORLD_PATH = BASE_PATH / "src" / WORLD_NAME
LIB_PATH = WORLD_PATH / "lib"
BUILD_PATH = BASE_PATH / "build"
LIB_PATCHES = BASE_PATH / "lib_patches"

REQUIREMENTS = BASE_PATH / "requirements.txt"


EXCLUDE = [
    "**/__pycache__",
    "**/__MACOSX",
    "**/.DS_STORE",
]


def clean_build_path(path: Path):
    assert path == BUILD_PATH or BUILD_PATH in path.parents, path
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def install_dependency(
    name: str | None = None,
    *,
    requirements: str | Path | None = None,
    target: str | Path | None = None,
    python_version: str | None = None,
    platforms: list[str] | None = None,
):
    args: list[str | Path] = [sys.executable, "-m", "pip", "install", "-q", "--only-binary=:all:"]
    if name is not None:
        args.append(name)
    if requirements is not None:
        args.append("-r")
        args.append(requirements)
    if target is not None:
        args.append("-t")
        args.append(target)
    if python_version:
        args.append("--python-version")
        args.append(python_version)
    if platforms:
        for platform in platforms:
            args.append("--platform")
            args.append(platform)
    subprocess.check_call(args)


def apply_patch(source_file: Path, patch_file: Path):
    subprocess.check_call(["patch", source_file, patch_file])


def setup_requirements():
    try:
        shutil.rmtree(LIB_PATH)
    except FileNotFoundError:
        pass
    LIB_PATH.mkdir()

    temp_lib = BUILD_PATH / "lib"
    for name, platforms in PLATFORMS.items():
        for version in PYTHON_VERSIONS:
            logger.info(f"Installing dependencies for {version}-{name}")
            install_dependency(requirements=REQUIREMENTS, target=temp_lib, python_version=version, platforms=platforms)
            shutil.copytree(temp_lib, LIB_PATH, dirs_exist_ok=True)
            shutil.rmtree(temp_lib)

    for patch_file in LIB_PATCHES.rglob("*.patch"):
        source_file = LIB_PATH / patch_file.relative_to(LIB_PATCHES).with_suffix("")
        apply_patch(source_file, patch_file)


def get_files():
    files: set[Path] = set()
    for path in WORLD_PATH.rglob("*"):
        files.add(path)
    for pattern in EXCLUDE:
        for path in WORLD_PATH.glob(pattern):
            if path.is_dir():
                files.difference_update(path.rglob("*"))
            try:
                files.remove(path)
            except KeyError:
                pass
    files.remove(WORLD_PATH / "archipelago.json")
    return files


def build_apworld():
    setup_requirements()

    logger.info("Packaging APWorld")

    from worlds.Files import APWorldContainer

    with open(WORLD_PATH / "archipelago.json", "r", encoding="utf-8") as file:
        manifest: dict = json.load(file)
    zip_path = BUILD_PATH / f"{WORLD_NAME}.apworld"
    container = APWorldContainer(str(zip_path))
    container.game = manifest["game"]
    manifest.update(container.get_manifest())

    BUILD_PATH.mkdir(parents=True, exist_ok=True)
    zip_path = BUILD_PATH / f"{WORLD_NAME}.apworld"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as apworld:
        for path in get_files():
            relative_path = f"{WORLD_NAME}/{path.relative_to(WORLD_PATH)}"
            apworld.write(path, relative_path)
        apworld.writestr(f"{WORLD_NAME}/archipelago.json", json.dumps(manifest))


def generate_template():
    import Options
    import Utils

    logger.info("Creating template")

    templates = BUILD_PATH / "templates"
    templates.mkdir(parents=True, exist_ok=True)
    Options.generate_yaml_templates(templates, generate_hidden=False)
    with open(WORLD_PATH / "archipelago.json", "r", encoding="utf-8") as file:
        game: str = json.load(file)["game"]
    template = templates / f"{Utils.get_file_safe_name(game)}.yaml"
    template.rename(BUILD_PATH / f"{template.name.replace(' ', '_')}")
    clean_build_path(templates)


logger = logging.Logger(Path(__file__).name)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", default=None, help="Path to your Archipelago source code")
    parser.add_argument("-q", "--quiet", action="store_true", help="Print less information")
    args = parser.parse_args()

    ap_path = args.path or os.getenv("AP_SOURCE_PATH") or os.getenv("AP_PATH") or os.getcwd()
    sys.path.append(ap_path)

    logging.basicConfig()
    logging.root.setLevel(logging.CRITICAL)

    if args.quiet:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)

    clean_build_path(BUILD_PATH)
    build_apworld()
    generate_template()
