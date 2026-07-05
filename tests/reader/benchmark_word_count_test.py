from src.reader.reader import get_words_count, WORD_BREAK_CHARS, WORD_BREAK_CHARS_

sample_text = "Python is highly performant when using C-extensions. " * 500


# pytest automatically injects the 'benchmark' fixture
def test_benchmark_word_count_via_split(benchmark):

    # Pass the function and its arguments into benchmark
    result = benchmark(get_words_count, sample_text)

    # Sanity check: Ensure the function still returns correct data
    assert result == 3500


def test_benchmark_word_count_naive(benchmark):
    result = benchmark(get_words_count_naive, sample_text)
    assert result == 3500


def test_benchmark_word_count_optimized(benchmark):
    result = benchmark(get_words_count_optimized, sample_text)
    assert result == 3500


# Results
# ---------------------------------------------------------------------------------------------------- benchmark: 3 tests ---------------------------------------------------------------------------------------------------
# Name (time in us)                              Min                   Max                  Mean              StdDev                Median                 IQR            Outliers          OPS            Rounds  Iterations
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# test_benchmark_word_count_via_split        72.3000 (1.0)        321.3999 (1.0)         76.5029 (1.0)       12.6296 (1.0)         73.5000 (1.0)        1.2000 (1.0)       605;939  13,071.4052 (1.0)        6623           1
# test_benchmark_word_count_optimized       640.4000 (8.86)     1,347.9001 (4.19)       671.4938 (8.78)      44.3182 (3.51)       658.7500 (8.96)      26.0000 (21.67)       75;75   1,489.2171 (0.11)       1090           1
# test_benchmark_word_count_naive         4,397.7001 (60.83)    5,537.6000 (17.23)    4,517.2370 (59.05)    207.6459 (16.44)    4,430.4000 (60.28)    103.8502 (86.54)       20;21     221.3743 (0.02)        203           1
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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


def get_words_count_naive(text: str) -> int:
    if not text:
        return 0

    i = 0
    for i in range(0, len(text)):
        if text[i] not in WORD_BREAK_CHARS_:
            break

    if i == len(text) - 1:
        return 0 if (text[i] in WORD_BREAK_CHARS_) else 1

    is_word_break = False
    was_previous_char_word_break = False
    count = 1

    for i in range(i, len(text)):
        is_word_break = text[i] in WORD_BREAK_CHARS_

        if not was_previous_char_word_break and is_word_break:
            was_previous_char_word_break = True
            count += 1
            continue

        was_previous_char_word_break = is_word_break

    if was_previous_char_word_break:
        count -= 1

    return count


def get_words_count_optimized(text: str) -> int:
    count = 0
    in_word = False

    for ch in text:
        if ch in WORD_BREAK_CHARS:
            in_word = False
        else:
            if not in_word:
                count += 1
                in_word = True

    return count
