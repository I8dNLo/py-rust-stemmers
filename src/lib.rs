use pyo3::prelude::*;

// Import the stemmer implementation from the rust-stemmers library
extern crate rust_stemmers;
use rust_stemmers::{Algorithm, Stemmer};

// Create a Python class to expose the stemmer functionality
#[pyclass]
pub struct StemmerWrapper {
    stemmer: Stemmer,
}

#[pymethods]
impl StemmerWrapper {
    #[new]
    fn new(lang: &str) -> Self {
        let algorithm = match lang.to_lowercase().as_str() {
            "arabic" => Algorithm::Arabic,
            // "armenian" => Algorithm::Armenian,
            "danish" => Algorithm::Danish,
            "dutch" => Algorithm::Dutch,
            "english" => Algorithm::English,
            "finnish" => Algorithm::Finnish,
            "french" => Algorithm::French,
            "german" => Algorithm::German,
            "greek" => Algorithm::Greek,
            "hungarian" => Algorithm::Hungarian,
            "italian" => Algorithm::Italian,
            "norwegian" => Algorithm::Norwegian,
            "portuguese" => Algorithm::Portuguese,
            "romanian" => Algorithm::Romanian,
            "russian" => Algorithm::Russian,
            "spanish" => Algorithm::Spanish,
            "swedish" => Algorithm::Swedish,
            "tamil" => Algorithm::Tamil,
            "turkish" => Algorithm::Turkish,
            _ => panic!("Unsupported language: {}", lang),
        };
        let stemmer = Stemmer::create(algorithm);
        StemmerWrapper { stemmer }
    }

    #[inline(always)]
    fn stem_word(&self, input: &str) -> String {
        self.stemmer.stem(input).into_owned()
    }

    #[inline(always)]
    fn stem_word_bytes(&self, input: &[u8]) -> String {
        let input_str = std::str::from_utf8(input).unwrap();
        self.stemmer.stem(input_str).into_owned()
    }

    #[inline(always)]
    pub fn stem_words_parallel(&self, inputs: Vec<&str>) -> Vec<String> {
        inputs.into_iter()
            .map(|word| self.stemmer.stem(word))
            .map(|stemmed| stemmed.into_owned())
            .collect()
    }
    #[inline(always)]
    fn stem_words(&self, words: Vec<&str>) -> Vec<String> {
        words.into_iter()
            .map(|word| self.stemmer.stem(word).into_owned())
            .collect()
    }

    #[inline(always)]
    fn stem_words_bytes(&self, words: Vec<&[u8]>) -> Vec<String> {
        words.into_iter()
            .map(|word| {
                let input_str = std::str::from_utf8(word).unwrap();
                self.stemmer.stem(input_str).into_owned()
            })
            .collect()
    }
}


/// This module is required for the Python interpreter to access the Rust functions.
#[pymodule]
fn py_rust_stemmers(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<StemmerWrapper>()?;
    Ok(())
}
