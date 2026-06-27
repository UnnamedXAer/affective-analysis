from pathlib import Path
import warnings

from pydantic import BaseModel, model_validator
import yaml


class Config:
    def __init__(self, chunking_config: ChunkingConfig):
        self.chunking_config: ChunkingConfig = chunking_config


class ChunkingConfig(BaseModel):
    turns_per_chunk: int = 5
    max_turn_length_words: int = 0
    max_length_words: int = 0
    min_statements: int = 2
    overlap_factor: float = 0.2

    @model_validator(mode="after")
    def check_soundness(self):
        if self.max_turn_length_words and self.max_length_words < (
            self.turns_per_chunk * self.max_turn_length_words // 2
        ):
            warnings.warn(
                "`max_length_words` seems low, see also `turns_per_chunk` and `max_turn_length_words`",
                category=UserWarning,
                stacklevel=2,
            )
        return self


def must_load_config(path: str) -> Config:
    path_path = Path(path)
    chunking_config = ChunkingConfig.model_validate(
        yaml.safe_load(path_path.read_bytes())["chunking"]
    )
    return Config(chunking_config)
