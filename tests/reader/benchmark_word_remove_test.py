from src.reader.reader import (
    get_words_count,
    remove_excess_words,
    remove_excess_words_optimized,
)

SAMPLE_TEXT = "Python is highly performant when using C-extensions. " * 500 # 3500 words
words_count = get_words_count(SAMPLE_TEXT)

MAX_WORDS = 1000
RUNS = 3


def test_benchmark_remove_excess_words(benchmark):
    benchmark(
        run_x_times, RUNS, remove_excess_words, SAMPLE_TEXT, words_count, MAX_WORDS
    )


def test_benchmark_remove_excess_words_optimized(benchmark):
    benchmark(
        run_x_times,
        RUNS,
        remove_excess_words_optimized,
        SAMPLE_TEXT,
        words_count,
        MAX_WORDS,
    )


def run_x_times(runs, func, sample_text, words_count, max_words):
    for x in range(runs):
        current_max_words = max_words * (x + 1)
        result, result_words_count = func(sample_text, words_count, current_max_words)

        if current_max_words >= words_count:
            assert result_words_count == words_count
        else:
            assert result_words_count == current_max_words


def test_benchmark_remove_excess_words_split(benchmark):
    benchmark(
        run_x_times,
        RUNS,
        remove_excess_words_split,
        SAMPLE_TEXT,
        words_count,
        MAX_WORDS,
    )


def remove_excess_words_split(
    text: str, text_words_count: int, max_words: int
) -> tuple[str, int]:
    # this does not preserve the original separators, but is a simple implementation for benchmarking purposes

    if max_words <= 0:
        return text, text_words_count

    if max_words >= text_words_count:
        return text, text_words_count

    output_words = text.split(maxsplit=max_words)[:max_words]
    return (" ".join(output_words), len(output_words))
