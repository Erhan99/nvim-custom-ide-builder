import os
import platform
import tempfile
from pathlib import Path
import shutil
from installers.winget import WingetInstaller
from installers.apt import AptInstaller
import subprocess

EXECUTABLES = {
    "git": "git",
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

    if config.os == "linux":
        if shutil.which("node") is None:
            install_latest_node()
        if shutil.which("nvim") is None:
            install_latest_neovim()
    else:
        if not is_installed("neovim"):
            installer.install("neovim")
        if not is_installed("node"):
            installer.install("node")

    for exe in EXECUTABLES:
        if not is_installed(exe):
            installer.install(exe)

    apply_theme(config.theme)
    
    generate_ai(config)


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

def has_dependency(dependency):
    return shutil.which(dependency) is not None

def install_latest_neovim():
    arch = platform.machine()

    if arch == "x86_64":
        archive = "nvim-linux-x86_64.tar.gz"
    elif arch in ("aarch64", "arm64"):
        archive = "nvim-linux-arm64.tar.gz"
    else:
        raise RuntimeError(f"Unsupported architecture: {arch}")

    url = (
        "https://github.com/neovim/neovim/releases/latest/download/"
        + archive
    )

    with tempfile.TemporaryDirectory() as temp:
        os.chdir(temp)

        subprocess.run(
            ["wget", url],
            check=True,
        )

        subprocess.run(
            ["tar", "-xzf", archive],
            check=True,
        )

        subprocess.run(
            ["sudo", "rm", "-rf", "/opt/nvim"],
            check=True,
        )

        folder = archive.replace(".tar.gz", "")

        subprocess.run(
            ["sudo", "mv", folder, "/opt/nvim"],
            check=True,
        )

        subprocess.run(
            [
                "sudo",
                "ln",
                "-sf",
                "/opt/nvim/bin/nvim",
                "/usr/local/bin/nvim",
            ],
            check=True,
        )

def install_latest_node():
    subprocess.run(
        [
            "bash",
            "-c",
            "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash",
        ],
        check=True,
    )

    subprocess.run(
        [
            "bash",
            "-c",
            'export NVM_DIR="$HOME/.nvm" && '
            '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && '
            "nvm install --lts",
        ],
        check=True,
    )

    subprocess.run(
        [
            "bash",
            "-c",
            'export NVM_DIR="$HOME/.nvm" && '
            '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && '
            "nvm use --lts",
        ],
        check=True,
    )

AI_PLUGINS = {
    "copilot": {
        "repo": "zbirenbaum/copilot.lua",
        "opts": {
            "suggestion": {
                "enabled" : True,
                "auto_trigger": True,
                "keymap": {
                    "accept": "<Tab>",
                    "next": "<M- ]>",
                    "prev": "<M- [>",
                    "dismiss": "<C- ]>",
                    }
            },
            "panel": {
                "enabled": False
            }
        }
    },
    "claude code": {
        "repo": "greggh/claude-code.nvim",
    },
    "codex": {
        "repo": "johnseth97/codex.nvim",
        "opts": {
            "autoinstall": True,
            }
    },
}

def to_lua(value):
    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, str):
        return f'"{value}"'

    if isinstance(value, (int, float)):
        return str(value)

    if isinstance(value, list):
        return "{ " + ", ".join(to_lua(v) for v in value) + " }"

    if isinstance(value, dict):
        items = []

        for key, val in value.items():
            items.append(f"{key} = {to_lua(val)}")

        return "{ " + ", ".join(items) + " }"

    raise TypeError(f"Unsupported type: {type(value)}")

def generate_ai(config):
    destination = (
        Path.home()
        / ".config"
        / "nvim"
        / "lua"
        / "plugins"
        / "ai.lua"
    )

    with open(destination, "w") as file:
        file.write("return {\n")

        for ai in config.ai:
            plugin = AI_PLUGINS[ai]

            file.write("    {\n")
            file.write(f'        "{plugin["repo"]}",\n')

            if "opts" in plugin:
                file.write(f'        opts = {to_lua(plugin["opts"])},\n')

            file.write("    },\n\n")

        file.write("}\n")
