"""Conversation parser: converts raw text into structured Turn objects."""

from abc import ABC, abstractmethod
from src.models.turn import Turn


class BaseParser(ABC):
    @abstractmethod
    def parse_conversation(self, text: str) -> list[Turn]:
        """Parse a conversation transcript into Turn objects.

        Expected format: "Speaker: statement" (may span multiple lines).

        Args:
            text: Raw conversation text

        Returns:
            List of Turn objects, in order of appearance
        """
        raise NotImplementedError("Subclasses must implement parse_conversation")


class ConversationParser(BaseParser):

    def __init__(self):
        pass

    def parse_conversation(self, text: str) -> list[Turn]:
        turns = []
        line_num = 0

        for raw_line in text.split("\n"):
            line_num += 1
            stripped = raw_line.strip()

            # Skip empty lines
            if not stripped:
                continue

            # Parse "Speaker: statement" format
            if ":" not in stripped:
                # This is a continuation of the previous statement
                if turns:
                    last_turn = turns[-1]
                    last_turn.statement += " " + stripped
                    last_turn.word_count = len(last_turn.statement.split())
                continue

            # Split on first colon only
            colon_idx = stripped.find(":")
            speaker = stripped[:colon_idx].strip()
            statement = stripped[colon_idx + 1 :].strip()

            # Skip if no speaker
            if not speaker:
                continue

            # Count words (0 if statement is empty)
            word_count = len(statement.split()) if statement else 0

            turns.append(
                Turn(
                    speaker=speaker,
                    statement=statement,
                    line_num=line_num,
                    word_count=word_count,
                )
            )

        return turns
