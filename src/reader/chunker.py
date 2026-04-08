"""Conversation chunking: splits turns into semantically coherent chunks."""

from src.models.chunk import Chunk
from src.models.chunk_config import ChunkConfig

from .parser import Turn


def chunk_stream(turns: list[Turn], config: ChunkConfig) -> list[Chunk]:
    """Split turns into chunks based on configuration.

    Algorithm:
    1. Start at index 0
    2. Collect turns up to turns_per_chunk
    3. If max_length_words set: keep adding turns until word limit, BUT enforce min_statements
    4. Create chunk after collecting enough statements
    5. Roll window forward by (turns_per_chunk - overlap_turns)

    Args:
        turns: List of Turn objects
        config: ChunkConfig with chunking parameters

    Returns:
        List of Chunk objects
    """
    if not turns:
        return []

    chunks = []
    chunk_id = 0

    # Calculate overlap in turn count
    overlap_turns = max(0, int(config.turns_per_chunk * config.overlap_factor))
    step_size = max(1, config.turns_per_chunk - overlap_turns)

    start_idx = 0

    while start_idx < len(turns):
        # Collect turns for this chunk
        end_idx = start_idx
        chunk_turns = []
        chunk_words = 0

        # First pass: try to reach turns_per_chunk
        while end_idx < len(turns) and len(chunk_turns) < config.turns_per_chunk:
            turn = turns[end_idx]
            chunk_turns.append(turn)
            chunk_words += turn.word_count
            end_idx += 1

        # Second pass: if max_length_words set, add more turns until hitting limit
        # BUT enforce that we have at least min_statements
        if config.max_length_words is not None:
            # If we haven't hit the word limit and have fewer than min_statements, keep adding
            while end_idx < len(turns) and chunk_words < config.max_length_words:
                turn = turns[end_idx]
                chunk_turns.append(turn)
                chunk_words += turn.word_count
                end_idx += 1

            # If we exceeded word limit, back off until we have at least min_statements
            while (
                len(chunk_turns) > config.min_statements
                and chunk_words > config.max_length_words
            ):
                last_turn = chunk_turns.pop()
                chunk_words -= last_turn.word_count
                end_idx -= 1

        # Ensure minimum statements (requirement: enforce even if exceeding word limit)
        if len(chunk_turns) < config.min_statements and end_idx < len(turns):
            while end_idx < len(turns) and len(chunk_turns) < config.min_statements:
                turn = turns[end_idx]
                chunk_turns.append(turn)
                chunk_words += turn.word_count
                end_idx += 1

        # Create chunk if we have turns
        if chunk_turns:
            # Extract unique speakers in order
            seen_speakers = set()
            participants = []
            for turn in chunk_turns:
                if turn.speaker not in seen_speakers:
                    seen_speakers.add(turn.speaker)
                    participants.append(turn.speaker)

            # Build raw text
            raw_text = "\n".join(
                [f"{turn.speaker}: {turn.statement}" for turn in chunk_turns]
            )

            chunk = Chunk(
                chunk_id=chunk_id,
                participants=participants,
                raw_text=raw_text,
                word_count=chunk_words,
                statement_count=len(chunk_turns),
                turn_range=(start_idx, end_idx - 1),
                metadata={
                    "first_speaker": chunk_turns[0].speaker,
                    "last_speaker": chunk_turns[-1].speaker,
                },
            )
            chunks.append(chunk)
            chunk_id += 1

        # Move to next chunk start (with overlap)
        start_idx = end_idx - overlap_turns

        # Stop if we're at the end
        if end_idx >= len(turns):
            break

    return chunks
