"""Main orchestrator for the affective analysis pipeline."""

from pathlib import Path
from src.reader.reader import next_chunk
from src.config import must_load_config
import sys


for output in [sys.stdout, sys.stderr]:
    if hasattr(output, "reconfigure"):
        # powershell falls back to cp1252 when redirecting output to a file, so we need to reconfigure it to utf-8
        output.reconfigure(encoding="utf-8", errors="replace") # type: ignore



def main():
    """Run the affective analysis pipeline on a conversation file."""

    # Load configuration
    config = must_load_config("config.yaml")
    config_chunking = config.chunking_config
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

    for ch in next_chunk(input_file, config_chunking):
        print()
        print(ch)

    print(f"✅ Processing complete!")


if __name__ == "__main__":
    main()
