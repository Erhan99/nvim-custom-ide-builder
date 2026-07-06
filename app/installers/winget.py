import subprocess

class WingetInstaller:
    PACKAGES = {
        "neovim": "Neovim.Neovim",
        "git": "Git.Git",
        "node": "OpenJS.NodeJS",
        "npm": "OpenJS.NodeJS",  # Comes with Node.js
        "ripgrep": "BurntSushi.ripgrep.MSVC",
        "fd": "sharkdp.fd",
    }

    def install(self, package):
        package_name = self.PACKAGES[package]
        subprocess.run(
            ["winget", "install", package_name], 
            check = True,
        )
