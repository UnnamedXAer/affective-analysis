"""Configuration loading and validation."""

import os
from pathlib import Path
from typing import Optional

import yaml

from .reader.chunker import ChunkConfig


def load_config(config_path: Optional[str] = None) -> ChunkConfig:
    """Load chunking configuration from YAML file.

    If config_path is not provided, looks for 'config.yaml' in:
    1. Current working directory
    2. Project root (parent of src/)

    Falls back to ChunkConfig defaults if file not found.

    Args:
        config_path: Path to config.yaml file (optional)

    Returns:
        ChunkConfig with loaded or default values

    Raises:
        ValueError: If config file exists but contains invalid values
        yaml.YAMLError: If config file is malformed YAML
    """
    if config_path is None:
        # Try to find config.yaml in standard locations
        possible_paths = [
            Path("config.yaml"),
            Path(__file__).parent.parent / "config.yaml",  # project root
        ]
        config_path = None
        for path in possible_paths:
            if path.exists():
                config_path = str(path)
                break

    # If no config file found, use defaults
    if config_path is None or not Path(config_path).exists():
        return ChunkConfig()

    # Load and parse YAML
    with open(config_path, "r") as f:
        data = yaml.safe_load(f) or {}

    # Extract chunking section
    chunking_config = data.get("chunking", {})

    # Validate and create ChunkConfig
    try:
        config = ChunkConfig(
            turns_per_chunk=chunking_config.get("turns_per_chunk", 5),
            max_length_words=chunking_config.get("max_length_words", None),
            min_statements=chunking_config.get("min_statements", 2),
            overlap_factor=chunking_config.get("overlap_factor", 0.2),
        )
    except ValueError as e:
        raise ValueError(f"Invalid configuration in {config_path}: {e}")

    return config
