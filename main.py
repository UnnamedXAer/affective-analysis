"""Main orchestrator for the affective analysis pipeline."""

from pathlib import Path
from src.config import must_load_config
from src.reader.parser import BaseParser, ConversationParser
from src.reader.stream import FileStreamingChunker


def main():
    """Run the affective analysis pipeline on a conversation file."""

    # Load configuration
    config = must_load_config()
    print(f"📋 Configuration loaded:")
    print(f"   - turns_per_chunk: {config.turns_per_chunk}")
    print(f"   - max_length_words: {config.max_length_words}")
    print(f"   - min_statements: {config.min_statements}")
    print(f"   - overlap_factor: {config.overlap_factor}")
    print()

    # Path to input conversation file
    input_file = Path("temp_data/temp2.txt")

    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return

    parser: BaseParser = ConversationParser()
    streamer = FileStreamingChunker(
        config=config,
        parser=parser,
        file_path=input_file,
    )

    print(f"📖 Reading conversation from: {input_file}")
    print()

    # Stream and process chunks
    chunk_count = 0
    for chunk in streamer.stream():
        chunk_count += 1
        print(f"{'='*70}")
        print(
            f"📦 Chunk #{chunk.chunk_id + 1} (turns {chunk.turn_range[0]}-{chunk.turn_range[1]})"
        )
        print(f"{'='*70}")
        print(f"Participants: {', '.join(chunk.participants)}")
        print(f"Statements: {chunk.statement_count} | Words: {chunk.word_count}")
        print(f"Turn range: {chunk.turn_range}")
        print()
        print("Content:")
        print("-" * 70)
        print(chunk.raw_text)
        print("-" * 70)
        print()

    print(f"✅ Processing complete!")
    print(f"   Total chunks: {chunk_count}")


if __name__ == "__main__":
    main()
