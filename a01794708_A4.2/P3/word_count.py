"""Este módulo cuenta las palabras en un archivo de texto."""
import sys
import time

def read_words_from_file(filename):
    """Reads words from a file, handling invalid data."""
    words = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                for word in line.strip().split():
                    word = word.lower().strip('.,!?()[]{}"\'')
                    if word:
                        words[word] = words.get(word, 0) + 1
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no existe.")
        sys.exit(1)
    return words

def main():
    """Main function that executes the program."""
    if len(sys.argv) != 2:
        print("Uso: python word_count.py fileWithData.txt")
        sys.exit(1)
    filename = sys.argv[1]
    start_time = time.time()
    words = read_words_from_file(filename)
    if not words:
        print("No hay palabras válidas para procesar.")
        sys.exit(1)
    output = "\n".join(f"{word}: {count}" for word, count in sorted(words.items()))
    end_time = time.time()
    elapsed_time = end_time - start_time
    result_output = (
        f"Word Frequency Count:\n{output}\n\n"
        f"Execution Time: {elapsed_time:.6f} seconds\n"
    )
    print(result_output)
    with open("WordCountResults.txt", "w", encoding='utf-8') as result_file:
        result_file.write(result_output)
if __name__ == "__main__":
    main()
