from pathlib import Path
import shutil

def main():
    print("hello")
    print("making .conf folder...")
    create_config_folder()


def create_config_folder():
    nvim_config_folder = Path.home() / '.config' / 'nvim'
    base_dir = '../base'
    if nvim_config_folder.exists() :
        print("nvim config folder exists")
        shutil.copytree(base_dir, nvim_config_folder, dirs_exist_ok=True)

    else :
        print("config folder does not exist")

if __name__=="__main__":
    main()