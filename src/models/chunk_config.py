from dataclasses import dataclass
from typing import Optional

@dataclass
class ChunkConfig:
    """Configuration for chunking behavior.

    Attributes:
        turns_per_chunk: Target number of turns per chunk (X total exchanges)
        max_length_words: Maximum words per chunk (None = unlimited)
        min_statements: Minimum statements required per chunk (enforced even if exceeding word limit)
        overlap_factor: Fraction of chunk to overlap with next chunk (0.0 to 1.0)
    """

    turns_per_chunk: int = 5
    max_length_words: Optional[int] = None
    min_statements: int = 2
    overlap_factor: float = 0.2

    def __post_init__(self):
        """Validate configuration values."""
        if self.turns_per_chunk < 1:
            raise ValueError("turns_per_chunk must be >= 1")
        if self.min_statements < 1:
            raise ValueError("min_statements must be >= 1")
        if not (0.0 <= self.overlap_factor < 1.0):
            raise ValueError("overlap_factor must be in [0.0, 1.0)")
        if self.max_length_words is not None and self.max_length_words < 1:
            raise ValueError("max_length_words must be None or >= 1")