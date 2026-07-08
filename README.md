# Nvim Custom IDE Builder

This project helps you quickly install Neovim and generate a starter configuration with a few basic choices:

- Theme
- Language support
- AI tools

It is meant to get you from a clean machine to a usable Neovim setup with minimal manual editing.

## What It Does

When you run the script, it:

1. Creates or updates the Neovim config folder for your operating system
2. Prompts you to choose a theme
3. Prompts you to choose one or more programming languages
4. Prompts you to choose one or more AI tools
5. Writes the selected settings into your Neovim config
6. Installs missing dependencies through the available package manager or built-in install flow

## Supported Platforms

- Linux
- Windows
- macOS

Neovim config files are written to the standard config location for each platform:

- Linux: `~/.config/nvim`
- Windows: `%LOCALAPPDATA%\nvim`
- macOS: `~/Library/Application Support/nvim`

## Configuration Choices

### Themes

Available themes:

- catppuccin
- tokyonight
- kanagawa
- cyberdream
- onedark

### Language Support

You can select from:

- Python
- JavaScript
- TypeScript
- Java
- C#
- C++
- C
- PHP
- Go
- Rust

The generator configures:

- Treesitter parsers
- LSP servers
- Formatters

### AI Tools

Available AI integrations:

- Copilot
- Claude Code
- Codex

## How To Run

From the project root:

```bash
python3 app/main.py
```

NOTE: Execute in a venv with pick installed using pip

## Project Layout

- `app/main.py` - interactive entrypoint
- `app/builder.py` - installs tools and writes generated config files
- `app/config.py` - runtime config and OS-aware Neovim path detection
- `base/` - starter Neovim configuration copied into the target config directory
- `themes/` - theme templates

## Notes

- The script expects a working terminal environment for the TUI prompts.
- On Linux, Neovim and Node.js may be installed automatically if they are missing.
- On Windows, package installation is handled through `winget` when available.
- On Debian/Ubuntu-based Linux systems, package installation is handled through `apt` when available.

