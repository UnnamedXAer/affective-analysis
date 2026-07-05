from asyncio.log import logger
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

    def __str__(self) -> str:
        return f"Turn(\n\tid={self.id},\n\tperson_id={self.person_id},\n\ttext={self.text},\n\tline_start={self.line_start},\n\tline_end={self.line_end})"


@dataclass
class Person:
    id: str
    name: str
    total_text_length: int

    def __str__(self) -> str:
        return f"Person(\n\tid={self.id},\n\tname={self.name},\n\ttotal_text_length={self.total_text_length})"


persons: dict[str, Person] = {}


def stream(path: Path) -> Generator[Turn]:

    turns: list[Turn] = []
    current_turn: Turn | None = None
    prev_turn: Turn | None = None
    id = 0
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                if current_turn is not None:
                    current_turn.text += "\n"
                    current_turn.line_end = i
                continue

            parts = line.split(": ")
            if len(parts) > 1:
                person_name = parts[0].strip()
                text = ": ".join(parts[1:]).strip()
                existing_person = persons.get(person_name)
                if existing_person is not None:
                    existing_person.total_text_length += len(text)
                else:
                    existing_person = Person(person_name, person_name, len(text))
                persons[person_name] = existing_person

                prev_turn = current_turn
                
                current_turn = Turn(str(id), person_name, text, i, i)
                id += 1
            else:
                if current_turn is None:
                    logger.warning(f"Line {i} does not belong to any turn: {line}")
                    continue

                current_turn.text += "\n" + line
                persons[current_turn.person_id].total_text_length += len(line)
                current_turn.line_end = i

            if prev_turn is not None:
                prev_turn.text = prev_turn.text.strip()
                yield prev_turn
                prev_turn = None
                sleep(0.1)  # Simulate delay in streaming data


@dataclass
class Chunk:
    id: str
    turns: list[Turn]

    def __str__(self) -> str:
        turns_str = "\n".join(str(turn) for turn in self.turns)
        return f"Chunk(\n\tid={self.id},\n\tturns=[\n{turns_str}\n])"


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
