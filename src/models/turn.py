from dataclasses import dataclass


@dataclass
class Turn:
    """Represents a single turn in a conversation.
    
    Attributes:
        speaker: Name of the participant speaking
        statement: The content of what was said
        line_num: Original line number in source text (1-indexed)
        word_count: Number of words in the statement
    """
    speaker: str
    statement: str
    line_num: int
    word_count: int