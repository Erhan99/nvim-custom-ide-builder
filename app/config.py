from dataclasses import dataclass
import platform 

@dataclass
class BuilderConfig:
    theme:str
    os:str

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

config = BuilderConfig(
        theme = "catppuccin",
        os = detect_os()
        )
