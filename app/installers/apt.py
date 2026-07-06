import subprocess

class AptInstaller:
    PACKAGES = {
        "neovim": "neovim",
        "git": "git",
        "node": "nodejs",
        "npm": "npm",
        "ripgrep": "ripgrep",
        "fd": "fd-find",
    }

    def install(self, package):
        package_name = self.PACKAGES[package]
        subprocess.run(
            ["sudo", "apt", "install", "-y", package_name],
            check = True,
        )
