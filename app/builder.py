import os
import platform
import tempfile
from pathlib import Path
import shutil
from installers.winget import WingetInstaller
from installers.apt import AptInstaller
import subprocess
from config import get_nvim_config_dir

EXECUTABLES = {
    "git": "git",
    "ripgrep": "rg",
    "fd": ["fd", "fdfind"],
}

PACKAGE_CHECKS = {
    "neovim": "nvim",
    "node": "node",
    "npm": "npm",
}

LANGUAGE_SUPPORT = {
    "python": {
        "treesitter": ["python"],
        "lsp": ["pyright"],
        "formatters": ["black"],
    },
    "javascript": {
        "treesitter": ["javascript"],
        "lsp": ["tsserver"],
        "formatters": ["prettier"],
    },
    "typescript": {
        "treesitter": ["typescript"],
        "lsp": ["tsserver"],
        "formatters": ["prettier"],
    },
    "java": {
        "treesitter": ["java"],
        "lsp": ["jdtls"],
        "formatters": ["google_java_format"],
    },
    "c#": {
        "treesitter": ["c_sharp"],
        "lsp": ["omnisharp"],
        "formatters": ["csharpier"],
    },
    "c++": {
        "treesitter": ["cpp"],
        "lsp": ["clangd"],
        "formatters": ["clang_format"],
    },
    "c": {
        "treesitter": ["c"],
        "lsp": ["clangd"],
        "formatters": ["clang_format"],
    },
    "php": {
        "treesitter": ["php"],
        "lsp": ["intelephense"],
        "formatters": ["php_cs_fixer"],
    },
    "go": {
        "treesitter": ["go"],
        "lsp": ["gopls"],
        "formatters": ["gofmt"],
    },
    "rust": {
        "treesitter": ["rust"],
        "lsp": ["rust_analyzer"],
        "formatters": ["rustfmt"],
    },
}

def is_installed(tool):
    if tool in PACKAGE_CHECKS:
        return shutil.which(PACKAGE_CHECKS[tool]) is not None

    executable = EXECUTABLES[tool]

    if isinstance(executable, list):
        return any(shutil.which(cmd) for cmd in executable)

    return shutil.which(executable) is not None

def build(config):
    installer = get_installer()
    packages = ("neovim", "node", "npm")

    if config.os == "linux":
        for package in packages:
            if is_installed(package):
                continue

            if package == "neovim":
                install_latest_neovim()
            elif package == "node":
                install_latest_node()
            elif package == "npm":
                # npm is bundled with the Node.js install path on Linux.
                continue
    else:
        for package in packages:
            if not is_installed(package):
                installer.install(package)

    for exe in EXECUTABLES:
        if not is_installed(exe):
            installer.install(exe)

    apply_theme(config.theme)
    
    generate_ai(config)
    configure_neovim_to_support_languages(config)


def apply_theme(theme):
    source = Path(__file__).resolve().parent.parent / "themes" / f"{theme}.lua"

    destination = get_nvim_config_dir() / "lua" / "config" / "theme.lua"

    destination.parent.mkdir(parents=True, exist_ok=True)
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
                    "accept": "<C-l>",
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
            lua_key = key if isinstance(key, str) and key.isidentifier() else f'["{key}"]'
            items.append(f"{lua_key} = {to_lua(val)}")

        return "{ " + ", ".join(items) + " }"

    raise TypeError(f"Unsupported type: {type(value)}")


def unique(values):
    seen = set()
    result = []

    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)

    return result

def generate_ai(config):
    destination = get_nvim_config_dir() / "lua" / "plugins" / "ai.lua"

    destination.parent.mkdir(parents=True, exist_ok=True)

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


def configure_neovim_to_support_languages(config):
    destination = get_nvim_config_dir() / "lua" / "config" / "languages.lua"

    treesitter = []
    lsp_servers = []
    formatters_by_ft = {}

    for language in config.languages:
        support = LANGUAGE_SUPPORT.get(language)

        if support is None:
            raise RuntimeError(f"Unsupported language selection: {language}")

        treesitter.extend(support.get("treesitter", []))
        lsp_servers.extend(support.get("lsp", []))

        for formatter in support.get("formatters", []):
            filetypes = formatters_by_ft.setdefault(language_filetype(language), [])
            if formatter not in filetypes:
                filetypes.append(formatter)

    destination.parent.mkdir(parents=True, exist_ok=True)

    with open(destination, "w") as file:
        file.write("return {\n")
        file.write(f"  treesitter = {to_lua(unique(treesitter))},\n")
        file.write(f"  lsp_servers = {to_lua(unique(lsp_servers))},\n")
        file.write(f"  formatters_by_ft = {to_lua(formatters_by_ft)},\n")
        file.write("}\n")


def language_filetype(language):
    match language:
        case "c#":
            return "cs"
        case "c++":
            return "cpp"
        case _:
            return language
