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
    word_count: int
    line_start: int
    line_end: int

    def __str__(self) -> str:
        return f"Turn(\n\tid={self.id},\n\tperson_id={self.person_id},\n\ttext={self.text},\n\tword_count={self.word_count},\n\tline_start={self.line_start},\n\tline_end={self.line_end})"


@dataclass
class Person:
    id: str
    name: str
    total_text_length: int

    def __str__(self) -> str:
        return f"Person(\n\tid={self.id},\n\tname={self.name},\n\ttotal_text_length={self.total_text_length})"


persons: dict[str, Person] = {}


def stream(config: ChunkingConfig, path: Path) -> Generator[Turn]:

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

                current_turn = Turn(
                    str(id), person_name, text, get_words_count(text), i, i
                )
                id += 1
            else:
                if current_turn is None:
                    logger.warning(f"Line {i} does not belong to any turn: {line}")
                    continue

                line_words_count = get_words_count(line)

                turn_word_count = current_turn.word_count + line_words_count

                if (
                    config.max_turn_length_words
                    and turn_word_count > config.max_turn_length_words
                ):
                    remaining_words = (
                        config.max_turn_length_words - current_turn.word_count
                    )
                    line = remove_excess_words(line, line_words_count, remaining_words)

                current_turn.text += "\n" + line
                current_turn.word_count += line_words_count
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
    for t in stream(chunking_config, data_file_path):
        turns.append(t)
        if len(turns) >= chunking_config.turns_per_chunk:
            yield Chunk(i.__str__(), turns)
            i += 1
            turns = list()

    if len(turns) > 0:
        yield Chunk(i.__str__(), turns)


def get_words_count(text: str) -> int:
    return len(text.split())

WORD_BREAK_CHARS_ = [
    " ",
    "\n",
    "\r",
    "\t",
    "\v",
    "\f",
    "\u00a0",
    "\u1680",
    "\u2000",
    "\u2001",
    "\u2002",
    "\u2003",
    "\u2004",
    "\u2005",
    "\u2006",
    "\u2007",
    "\u2008",
    "\u2009",
    "\u200a",
    "\u202f",
    "\u205f",
    "\u3000",
]

WORD_BREAK_CHARS = set(WORD_BREAK_CHARS_)



def remove_excess_words(text: str, text_words_count: int, max_words: int) -> str:

    current_words_count = text_words_count
    position = len(text)
    was_previous_char_word_break = False
    while position > 0 and current_words_count > max_words:
        position -= 1
        if not was_previous_char_word_break and text[position] in WORD_BREAK_CHARS:
            was_previous_char_word_break = True
            current_words_count -= 1

    return text[:position]
