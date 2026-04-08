from dataclasses import dataclass, field


@dataclass
class Chunk:
    """Represents a chunk of conversation.

    Attributes:
        chunk_id: Unique identifier for this chunk
        participants: List of unique speakers in this chunk
        raw_text: Concatenated conversation text
        word_count: Total words in the chunk
        statement_count: Number of turns/statements in the chunk
        turn_range: (start_idx, end_idx) - indices into original turns list
        metadata: Extensible dict for additional info
    """

    chunk_id: int
    participants: list[str]
    raw_text: str
    word_count: int
    statement_count: int
    turn_range: tuple[int, int]
    metadata: dict = field(default_factory=dict)
