from dataclasses import dataclass
import os
import platform
from pathlib import Path

@dataclass
class BuilderConfig:
    theme:str
    os:str
    languages: list[str]
    ai: list[str]

def detect_os() -> str:
    match platform.system():
        case "Linux":
            return "linux"
        case "Windows":
            return "windows"
        case "Darwin":
            return "macos"
        case _:
            raise RuntimeError("Unsupported operating system")


def get_nvim_config_dir(os_name: str | None = None) -> Path:
    if os_name is None:
        os_name = detect_os()

    match os_name:
        case "windows":
            local_app_data = os.environ.get("LOCALAPPDATA")
            if local_app_data:
                return Path(local_app_data) / "nvim"
            return Path.home() / "AppData" / "Local" / "nvim"
        case "macos":
            return Path.home() / "Library" / "Application Support" / "nvim"
        case _:
            xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
            if xdg_config_home:
                return Path(xdg_config_home) / "nvim"
            return Path.home() / ".config" / "nvim"

config = BuilderConfig(
        theme = "catppuccin",
        os = detect_os(),
        languages = [],
        ai = []
        )
