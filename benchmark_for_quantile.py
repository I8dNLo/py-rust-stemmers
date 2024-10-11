import time
import csv
import statistics
from py_rust_stemmers import SnowballStemmer
from tqdm import tqdm
# Initialize the stemmer
s = SnowballStemmer('english')

# Text to split into words for testing
text = """This stem form is often a word itself, but this is not always the case as this is not a requirement for text search systems, which are the intended field of use. We also aim to conflate words with the same meaning, rather than all words with a common linguistic root (so awe and awful don't have the same stem), and over-stemming is more problematic than under-stemming so we tend not to stem in cases that are hard to resolve. If you want to always reduce words to a root form and/or get a root form which is itself a word then Snowball's stemming algorithms likely aren't the right answer."""
words = text.split()

# Configurations for the benchmark
loops = [2 ** i for i in range(20)]  # Different number of words to test with
iterations = 1000  # Run each test 10 times for statistical significance
csv_file = "benchmark_results.csv"  # Output file for CSV

# Function to run a benchmark
def run_benchmark(func, input_data, loops):
    timings = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        for _ in range(loops):
            func(input_data)
        end_time = time.perf_counter()
        timings.append(end_time - start_time)
    return timings

# Prepare benchmark tests
def benchmark_stem_words():
    results = []
    for word_count in tqdm(loops):
        input_data = words * (word_count // len(words))  # Scale input based on word count
        timings_seq = run_benchmark(lambda w: s.stem_words(w), input_data, 1)
        timings_par = run_benchmark(lambda w: s.stem_words_parallel(w), input_data, 1)

        # Compute stats
        mean_seq = statistics.mean(timings_seq)
        std_seq = statistics.stdev(timings_seq)
        mean_par = statistics.mean(timings_par)
        std_par = statistics.stdev(timings_par)

        # Append results
        results.append([word_count, mean_seq, std_seq, mean_par, std_par])

    return results

# Write results to CSV
def write_csv(results):
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Word Count", "Mean Time (Sequential)", "Std Dev (Sequential)", "Mean Time (Parallel)", "Std Dev (Parallel)"])
        writer.writerows(results)

# Run benchmarks and save results
benchmark_results = benchmark_stem_words()
write_csv(benchmark_results)
print(f"Benchmark complete. Results saved to {csv_file}.")
