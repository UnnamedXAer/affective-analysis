"""Streaming chunks from conversation data."""

from pathlib import Path
from typing import Generator

from .parser import BaseParser
from .chunker import chunk_stream, Chunk, ChunkConfig


class FileStreamingChunker:
    """Provides generator functions to stream chunks from conversation data."""

    def __init__(self, config: ChunkConfig, parser: BaseParser, file_path: Path):
        self.config: ChunkConfig = config
        self.parser: BaseParser = parser
        self.file_path: Path = file_path

    def _stream_chunks_from_text(
        self,
        text: str,
    ) -> Generator[Chunk, None, None]:
        """Stream chunks from conversation text.

        Parses the text, chunks it, and yields chunks one at a time.
        Simulates real-time arrival for processing.

        Args:
            text: Raw conversation text
            config: ChunkConfig (uses defaults if None)

        Yields:
            Chunk objects one at a time
        """
        turns = self.parser.parse_conversation(text)
        chunks = chunk_stream(turns, self.config)

        for chunk in chunks:
            yield chunk

    def stream(self) -> Generator[Chunk, None, None]:
        """Stream chunks from a conversation file.

        Reads the file, parses it, chunks it, and yields chunks one at a time.

        Yields:
            Chunk objects one at a time

        Raises:
            FileNotFoundError: If file_path doesn't exist
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Conversation file not found: {self.file_path}")

        text = self.file_path.read_text(encoding="utf-8")

        yield from self._stream_chunks_from_text(text)
