from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Generator

from src.config import ChunkingConfig


@dataclass
class Turn:
    id: str
    person_id: str
    text: str
    line_start: int
    line_end: int


@dataclass
class Person:
    id: str
    name: str
    total_text_length: int


persons = dict[str, Person]


def stream(path: Path) -> Generator[Turn]:

    turns = [
        Turn("t1", "1", "first", 0, 0),
        Turn("t2", "2", "first", 1, 2),
        Turn("t3", "3", "first", 3, 3),
        Turn("t4", "4", "first", 4, 4),
        Turn("t5", "4", "first", 4, 4),
        Turn("t6", "4", "first", 4, 4),
        Turn("t7", "4", "first", 4, 4),
        Turn("t9", "4", "first", 4, 4),
        Turn("t10", "4", "first", 4, 4),
        Turn("t11", "4", "first", 4, 4),
    ]

    for t in turns:
        yield t
        sleep(0.1)  # Simulate delay in streaming data


@dataclass
class Chunk:
    id: str
    turns: list[Turn]


def next_chunk(
    data_file_path: Path, chunking_config: ChunkingConfig
) -> Generator[Chunk]:

    i = 0
    turns: list[Turn] = list()
    for t in stream(data_file_path):
        turns.append(t)
        if len(turns) >= chunking_config.turns_per_chunk:
            yield Chunk(i.__str__(), turns)
            i += 1
            turns = list()

    yield Chunk(i.__str__(), turns)
