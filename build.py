#!/usr/bin/env python3

import json
import logging
import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

# TODO: Support 3.14 once both AP and Lupa do
PYTHON_VERSIONS = ["3.11", "3.12", "3.13"]

PLATFORMS = {
    "win_amd64": ["win_amd64"],
    "macosx_x86_64": ["macosx_11_0_universal", "macosx_11_0_x86_64"],
    "macosx_arm64": ["macosx_11_0_universal", "macosx_11_0_arm64"],
    "linux_x86_64": ["manylinux_2_28_x86_64", "manylinux_2_17_x86_64"],
}

BASE_PATH = Path(__file__).parent

WORLD_NAME = "msr"
WORLD_PATH = BASE_PATH / "src" / WORLD_NAME
with open(WORLD_PATH / "archipelago.json", "r", encoding="utf-8") as file:
    GAME_NAME: str = json.load(file)["game"]

LIB_PATH = WORLD_PATH / "lib"
BUILD_PATH = BASE_PATH / "build"
LIB_PATCHES = BASE_PATH / "lib_patches"
REQUIREMENTS = BASE_PATH / "requirements.txt"

ap_path: Path


def clean_build_path():
    BUILD_PATH.mkdir(exist_ok=True)
    for child in BUILD_PATH.iterdir():
        shutil.rmtree(child, ignore_errors=True)


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


def call_ap_component(component: str, *args: str):
    cmd = [sys.executable, "Launcher.py", component]
    if args:
        cmd += ["--", *args]
    subprocess.check_call(cmd, cwd=ap_path)


def build_apworld():
    setup_requirements()

    logger.info("Packaging APWorld")
    call_ap_component("Build APWorlds", GAME_NAME)
    apworld_name = f"{WORLD_NAME}.apworld"
    shutil.copy(ap_path.joinpath("build", "apworlds", apworld_name), BUILD_PATH / apworld_name)


def get_file_safe_name(name: str) -> str:
    return "".join(c for c in name if c not in '<>:"/\\|?*')


def generate_template():
    logger.info("Creating template")
    call_ap_component("Generate Template Options", "--skip_open_folder")
    template_name = f"{get_file_safe_name(GAME_NAME)}.yaml"
    shutil.copy(ap_path.joinpath("Players", "Templates", template_name), BUILD_PATH / template_name.replace(" ", "_"))


logger = logging.Logger(Path(__file__).name)
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", default=None, help="Path to your Archipelago source code")
    parser.add_argument("-q", "--quiet", action="store_true", help="Print less information")
    args = parser.parse_args()

    ap_path = Path(args.path or os.getenv("AP_SOURCE_PATH") or os.getenv("AP_PATH") or os.getcwd())

    if args.quiet:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)

    clean_build_path()
    build_apworld()
    generate_template()
