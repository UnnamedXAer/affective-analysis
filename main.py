"""Main orchestrator for the affective analysis pipeline."""

from pathlib import Path
from src.config import must_load_config


def main():
    """Run the affective analysis pipeline on a conversation file."""

    # Load configuration
    config = must_load_config("config.yaml")
    config_chunking= config.chunking_config
    print(f"📋 Configuration loaded:")
    print(f"   - turns_per_chunk: {config_chunking.turns_per_chunk}")
    print(f"   - max_turn_length_words: {config_chunking.max_turn_length_words}")
    print(f"   - max_length_words: {config_chunking.max_length_words}")
    print(f"   - min_statements: {config_chunking.min_statements}")
    print(f"   - overlap_factor: {config_chunking.overlap_factor}")
    print()

    # Path to input conversation file
    input_file = Path("temp_data/temp2.txt")

    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return

    print(f"✅ Processing complete!")


if __name__ == "__main__":
    main()
