from src.reader.reader import (
    get_words_count,
    remove_excess_words,
    WORD_BREAK_CHARS,
)

SAMPLE_TEXT = (
    "Python is highly performant when using C-extensions. " * 500
)  # 3500 words
words_count = get_words_count(SAMPLE_TEXT)

MAX_WORDS = 1000
RUNS = 3


def test_benchmark_remove_excess_words(benchmark):
    benchmark(
        run_x_times, RUNS, remove_excess_words, SAMPLE_TEXT, words_count, MAX_WORDS
    )


def test_benchmark_remove_excess_words_naive(benchmark):
    benchmark(
        run_x_times,
        RUNS,
        remove_excess_words_naive,
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


# Results
# ----------------------------------------------------------------------------------------------------- benchmark: 3 tests -----------------------------------------------------------------------------------------------------
# Name (time in us)                                   Min                   Max                  Mean              StdDev                Median                IQR            Outliers         OPS            Rounds  Iterations
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# test_benchmark_remove_excess_words_split       198.7999 (1.0)        399.5001 (1.0)        207.7718 (1.0)       16.2032 (1.0)        203.3000 (1.0)       1.4000 (1.0)       197;679  4,812.9727 (1.0)        3149           1
# test_benchmark_remove_excess_words           1,848.5999 (9.30)     2,661.8000 (6.66)     1,932.3949 (9.30)      89.1150 (5.50)     1,913.3000 (9.41)     56.1249 (40.09)       42;42    517.4926 (0.11)        511           1
# test_benchmark_remove_excess_words_naive     2,215.7999 (11.15)    3,550.2000 (8.89)     2,344.9607 (11.29)    145.4482 (8.98)     2,309.9000 (11.36)    55.2501 (39.46)       34;41    426.4464 (0.09)        433           1
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def remove_excess_words_naive(
    text: str, text_words_count: int, max_words: int
) -> tuple[str, int]:
    if max_words <= 0:
        return text, text_words_count

    if max_words >= text_words_count:
        return text, text_words_count

    current_words_count = text_words_count
    position = len(text)
    in_word = False
    while position > 0 and current_words_count > max_words:
        position -= 1
        ch = text[position]
        if ch in WORD_BREAK_CHARS:
            if in_word:
                current_words_count -= 1
                in_word = False
        else:
            if not in_word:
                in_word = True

    return text[:position], current_words_count


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
