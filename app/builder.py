from pathlib import Path
import shutil

def apply_theme(config):
    source = Path("../themes") / f"{config.theme}.lua"

    destination = (
        Path.home()
        / ".config"
        / "nvim"
        / "lua"
        / "config"
        / "theme.lua"
    )

    shutil.copy(source, destination)
