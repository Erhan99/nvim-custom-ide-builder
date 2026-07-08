from pathlib import Path
import shutil
from pick import pick
from config import config, get_nvim_config_dir
from builder import build

def main():
    create_config_folder()

    theme = select_theme()
    languages = select_languages()
    ai_tools = select_ai_tools()
    
    create_config(theme, languages, ai_tools)

def create_config_folder():
    nvim_config_folder = get_nvim_config_dir(config.os)
    base_dir = Path(__file__).resolve().parent.parent / "base"
    shutil.copytree(base_dir, nvim_config_folder, dirs_exist_ok=True)
        
def select_theme():
    themes = ["catppuccin", "tokyonight", "kanagawa", "cyberdream", "onedark"]
    title = "Select a theme:"

    theme, _ = pick(themes, title, indicator="=>", default_index=0)
    
    return theme

def select_languages():
    languages = ["python", "javascript", "typescript", "java", "c#", "c++", "c", "php", "go", "rust"]
    title = (
        "Select your preferred programming languages:\n\n"
        "Note: Language support (LSP, Treesitter, etc.) will be configured.\n"
        "SDKs, compilers, runtimes, and toolchains are NOT installed."
    )

    selected = pick(languages, title, multiselect=True)

    return [language for language, _ in selected]

def select_ai_tools():
    tools = ["copilot", "codex", "claude code"]
    title = "Select your AI tools:"

    selected = pick(tools, title, multiselect=True)

    return [tool for tool, _ in selected]

def create_config(theme, languages, ai_tools):
    config.theme = theme
    config.languages = languages
    config.ai = ai_tools
    build(config)

if __name__=="__main__":
    main()
