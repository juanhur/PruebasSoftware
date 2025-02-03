"""Module to compute descriptive statistics from a file with numbers."""
# pylint: disable=invalid-name

import sys
import time

def read_data(filename):
    """Read and validate data from the file."""
    numbers = []
    invalid_lines = 0

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    print(f"Error in line {line_num}: Empty line")
                    invalid_lines += 1
                    continue
                try:
                    num = float(line)
                    numbers.append(num)
                except ValueError:
                    print(f"Error in line {line_num}: Invalid data '{line}'")
                    invalid_lines += 1
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: File '{filename}' not found.") from e
    except Exception as e:  # pylint: disable=broad-except
        raise RuntimeError(f"Error reading file: {e}") from e

    return numbers, invalid_lines


def calculate_median(sorted_numbers, total_count):
    """Calculate the median from sorted data."""
    if total_count % 2 == 1:
        return sorted_numbers[total_count // 2]
    return (sorted_numbers[total_count // 2 - 1] + sorted_numbers[total_count // 2]) / 2


def calculate_mode(numbers):
    """Computes the mode of a list of numbers and returns a single value."""
    if not numbers:
        raise ValueError("No se puede calcular la moda de una lista vacía.")
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values(), default=0)
    if max_freq == 0:
        raise ValueError("No hay valores repetidos para calcular la moda.")
    mode_candidates = [num for num, freq in frequency.items() if freq == max_freq]
    return max(mode_candidates)  # Devuelve el menor en caso de empate

def calculate_variance_std(numbers, mean, total_count, sample=True):
    """Calculate variance and standard deviation."""
    if total_count == 0 or (sample and total_count == 1):
        return None, None  # Evitar división por cero

    squared_diffs = [(x - mean) ** 2 for x in numbers]
    # Si es una muestra, dividir por (N-1), si es población, dividir por N
    divisor = total_count - 1 if sample else total_count
    variance = sum(squared_diffs) / divisor

    return variance, variance ** 0.5



def main():
    """Main function to orchestrate the statistical calculations."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments. Usage: "
              "python computeStatistics.py fileWithData.txt")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        numbers, invalid_lines = read_data(filename)
    except (FileNotFoundError, RuntimeError) as e:
        print(str(e))
        sys.exit(1)

    if not numbers:
        print("No valid numbers found in the file.")
        sys.exit(1)

    total_count = len(numbers)
    mean = sum(numbers) / total_count
    sorted_numbers = sorted(numbers)
    median = calculate_median(sorted_numbers, total_count)
    modes = calculate_mode(sorted_numbers)
    variance, std_dev = calculate_variance_std(numbers, mean, total_count)
    elapsed_time = time.time() - start_time

    results = f"""Descriptive Statistics Results:
- Mean: {mean:.2f}
- Median: {median:.2f}
- Mode: {modes:.2f}
- Standard Deviation: {std_dev:.2f}
- Variance: {variance:.2f}
- Invalid lines: {invalid_lines}
- Time elapsed: {elapsed_time:.4f} seconds
"""

    print(results)
    with open('StatisticsResults.txt', 'w', encoding='utf-8') as out_file:
        out_file.write(results)


if __name__ == "__main__":
    main()
