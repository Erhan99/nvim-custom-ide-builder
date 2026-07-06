from pathlib import Path
import shutil
from installers.winget import WingetInstaller
from installers.apt import AptInstaller

EXECUTABLES = {
    "neovim": "nvim",
    "git": "git",
    "node": "node",
    "npm": "npm",
    "ripgrep": "rg",
    "fd": ["fd", "fdfind"],
}

def is_installed(tool):
    executable = EXECUTABLES[tool]

    if isinstance(executable, list):
        return any(shutil.which(cmd) for cmd in executable)

    return shutil.which(executable) is not None

def build(config):
    installer = get_installer()
    
    for exe in EXECUTABLES:
        if not is_installed(exe):
            installer.install(exe)

    apply_theme(config.theme)

def apply_theme(theme):
    source = Path("../themes") / f"{theme}.lua"

    destination = (
        Path.home()
        / ".config"
        / "nvim"
        / "lua"
        / "config"
        / "theme.lua"
    )

    shutil.copy(source, destination)

INSTALLERS = {
    "winget": WingetInstaller,
    "apt": AptInstaller,
}

def get_installer():
    for executable, installer_cls in INSTALLERS.items():
        if shutil.which(executable):
            return installer_cls()

    raise RuntimeError("No supported package manager found")
