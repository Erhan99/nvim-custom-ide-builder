from pathlib import Path
import shutil
from pick import pick
from config import config
from builder import apply_theme

def main():
    print("hello")
    print("making .conf folder...")
    create_config_folder()

    theme = select_theme()

    create_config(theme)

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

def create_config(theme):
    config.theme = theme
    apply_theme(config)

if __name__=="__main__":
    main()
