import unittest
import py_rust_stemers

class TestRustStemmer(unittest.TestCase):

    def test_english_stemming(self):
        words = ["fruitlessly", "happiness", "computations"]
        expected = ["fruitless", "happi", "comput"]
        result = py_rust_stemers.rust_stem(words, "english")
        self.assertEqual(result, expected)

    def test_spanish_stemming(self):
        words = ["frutalmente", "felicidad", "computaciones"]
        expected = ["frutal", "felic", "comput"]
        result = py_rust_stemers.rust_stem(words, "spanish")
        self.assertEqual(result, expected)

    def test_empty_input(self):
        words = []
        expected = []
        result = py_rust_stemers.rust_stem(words, "english")
        self.assertEqual(result, expected)

    def test_invalid_language(self):
        words = ["fruitlessly", "happiness", "computations"]
        with self.assertRaises(ValueError):
            py_rust_stemers.rust_stem(words, "invalid_lang")

if __name__ == '__main__':
    unittest.main()
