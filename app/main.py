from pathlib import Path
import shutil
from pick import pick
from config import config
from builder import build

def main():
    create_config_folder()

    theme = select_theme()
    ai_tools = select_ai_tools()

    create_config(theme, ai_tools)

def create_config_folder():
    nvim_config_folder = Path.home() / '.config' / 'nvim'
    base_dir = '../base'
    if nvim_config_folder.exists() :
        print("nvim config folder exists")
        shutil.copytree(base_dir, nvim_config_folder, dirs_exist_ok=True)

    else :
        print("config folder does not exist")

def select_theme():
    themes = ["catppuccin", "tokyonight", "kanagawa", "cyberdream", "onedark"]
    title = "Select a theme:"

    theme, _ = pick(themes, title, indicator="=>", default_index=0)
    
    return theme

def select_ai_tools():
    tools = ["copilot", "codex", "claude code"]
    title = "Select your AI assistant:"

    selected = pick(tools, title, multiselect=True)

    return [tool for tool, _ in selected]

def create_config(theme, ai_tools):
    config.theme = theme
    config.ai = ai_tools
    build(config)

if __name__=="__main__":
    main()
