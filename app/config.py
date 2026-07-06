from dataclasses import dataclass

@dataclass
class BuilderConfig:
    theme:str

config = BuilderConfig(
        theme = "tokyonight"
        )
