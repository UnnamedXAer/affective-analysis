# from now on use `pytest` for testing, but keep `unittest` for now to avoid breaking existing tests
import unittest

from src.reader.reader import get_words_count, get_words_count,remove_excess_words, remove_excess_words_optimized


class TestGetWordsCount(unittest.TestCase):
    def test_many(self):
        tests_table: list[tuple[str, int]] = [
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

        for text, expected_count in tests_table:
            with self.subTest(text=f"for text '{text}' expected count is {expected_count}"):
                result = get_words_count(text)
                self.assertEqual(result, expected_count)


class TestRemoveExcessWords(unittest.TestCase):
    def test_remove_excess_words(self):
        test_table = [
            ("This is a sample line with seven words", 5),
            ("Short text", 5),
            ("A Short text", 2),
            ("A Short text", 3),
            ("A Short text", 4),
            ("One two three", 0),
            ("", 0),
            ("", 3),
            ("    ", 3),
            ("  ddd  ", 3),
            ("  d a  ", 1),
            ("  ddd al\n\n uuu ", 3),
            ("  ddd al\n\n uuu ", 2),
        ]
        
        for text, max_words in test_table:
            with self.subTest(text=text, max_words=max_words):
                input_words_count = get_words_count(text)
                result, result_words_count = remove_excess_words(text, input_words_count, max_words)
                output_words_count = get_words_count(result)

                self.assertEqual(output_words_count, result_words_count)
                
                if max_words <= 0 or max_words >= input_words_count:
                    self.assertEqual(output_words_count, input_words_count)
                else:
                    self.assertEqual(output_words_count, max_words)


                result2, result2_words_count = remove_excess_words_optimized(text, input_words_count, max_words)
                output_words_count2 = get_words_count(result2)

                self.assertEqual(output_words_count2, output_words_count)
                self.assertEqual(result2_words_count, output_words_count)


    def test_remove_excess_words_preserves_original_separators(self):
        test_cases = [
            ("Alpha   beta gamma", 2, "Alpha   beta"),
            ("Alpha\nBeta\tGamma", 2, "Alpha\nBeta"),
            ("  Alpha beta", 1, "  Alpha"),
        ]

        for text, max_words, expected in test_cases:
            with self.subTest(text=text, max_words=max_words):
                (result, result_words_count) = remove_excess_words(text, get_words_count(text), max_words)
                self.assertEqual(result, expected)
                self.assertEqual(result_words_count, get_words_count(expected))

                (result2, result2_words_count) = remove_excess_words_optimized(text, get_words_count(text), max_words)
                self.assertEqual(result2, expected)
                self.assertEqual(result2_words_count, get_words_count(expected))


if __name__ == "__main__":
    unittest.main()
