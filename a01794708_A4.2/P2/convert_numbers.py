"""Este módulo lee números de un archivo, los convierte a binario y
hexadecimal, y guarda los resultados."""
import sys
import time

def read_numbers_from_file(filename):
    """Reads numbers from a file, handling invalid data."""
    numbers = []
    errors = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    num = int(line.strip())
                    numbers.append(num)
                except ValueError:
                    errors.append(line.strip())
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no existe.")
        sys.exit(1)
    return numbers, errors

def convert_to_binary(number):
    """Converts a number to binary (supports negative numbers using two's complement)."""
    if number == 0:
        return "0"
    if number > 0:
        binary = ""
        n = number
        while n > 0:
            binary = str(n % 2) + binary
            n //= 2
        return binary
    # Representación en complemento a dos
    bits = max(8, (abs(number).bit_length() + 1))
    binary = bin((1 << bits) + number)[2:]  # Complemento a dos
    return binary

def convert_to_hexadecimal(number):
    """Converts a number to hexadecimal (supports negative numbers)."""
    if number == 0:
        return "0"
    if number > 0:
        hex_chars = "0123456789ABCDEF"
        hexadecimal = ""
        n = number
        while n > 0:
            remainder = n % 16
            hexadecimal = hex_chars[remainder] + hexadecimal
            n //= 16
        return hexadecimal
    # Representación hexadecimal de complemento a dos
    bits = max(8, (abs(number).bit_length() + 1))
    hex_value = hex((1 << bits) + number)[2:].upper()
    return hex_value

def main():
    """Main function that executes the program."""
    if len(sys.argv) != 2:
        print("Uso: python convertNumbers.py fileWithData.txt")
        sys.exit(1)
    filename = sys.argv[1]
    start_time = time.time()
    numbers, errors = read_numbers_from_file(filename)
    if not numbers:
        print("No hay números válidos para procesar.")
        sys.exit(1)
    results = []
    for num in numbers:
        binary = convert_to_binary(num)
        hexadecimal = convert_to_hexadecimal(num)
        results.append(f"Number: {num} | Binary: {binary} | Hexadecimal: {hexadecimal}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    output = "\n".join(results) + f"\nExecution Time: {elapsed_time:.6f} seconds\n"
    if errors:
        output += f"\nInvalid Entries: {', '.join(errors)}\n"
    print(output)
    with open("ConvertionResults.txt", "w", encoding='utf-8') as result_file:
        result_file.write(output)

if __name__ == "__main__":
    main()
