# from now on use `pytest` for testing, but keep `unittest` for now to avoid breaking existing tests
import unittest

from src.reader.reader import get_words_count, get_words_count,remove_excess_words


class TestGetWordsCount(unittest.TestCase):
    def test_many(self):
        texts: list[tuple[str, int]] = [
            ("This is a sample line", 5),
            ("", 0),
            ("Hello", 1),
            ("Hello ", 1),
            (" Hello", 1),
            (" Hello ", 1),
            ("word1\nword2\tword3 word4", 4),
            ("word1   word2", 2),
            ("   ", 0),
            (" 1", 1),
            (" 12", 1),
            ("\t a", 1),
            ("\t abc", 1),
            ("  ", 0),
            (" a", 1),
        ]

        for text, expected_count in texts:
            with self.subTest(text=f"for text '{text}' expected count is {expected_count}"):
                result = get_words_count(text)
                self.assertEqual(result, expected_count)


class TestRemoveExcessWords(unittest.TestCase):
    def test_trims_to_max_words(self):
        text = "This is a sample line with seven words"
        result = remove_excess_words(text, get_words_count(text), 5)
        self.assertEqual(result, "This is a sample line")

    def test_leaves_short_text_unchanged(self):
        text = "Short text"
        result = remove_excess_words(text, get_words_count(text), 5)
        self.assertEqual(result, text)

    def test_returns_empty_when_max_words_is_zero(self):
        text = "One two three"
        result = remove_excess_words(text, get_words_count(text), 0)
        self.assertEqual(result, "")

    def test_handles_empty_string(self):
        text = ""
        result = remove_excess_words(text, get_words_count(text), 0)
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
