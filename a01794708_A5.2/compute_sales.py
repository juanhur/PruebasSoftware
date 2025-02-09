"""
Compute Sales Script
This script calculates total sales from a given sales record JSON file
using a price catalogue JSON file.
It handles errors gracefully and outputs the results
to both the console and a file.
"""
import json
import sys
import time
import csv


def load_json_file(file_path):
    """Carga un archivo JSON y maneja errores de lectura."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
    except json.JSONDecodeError:
        print(f"Error: El archivo {file_path} no tiene un formato JSON válido")
    except OSError as e:
        print(f"Error de sistema al leer {file_path}: {e}")
    return None


def compute_total_sales(prices, sales):
    """Calcula el costo total de las ventas basado en los precios
      y guarda en un archivo txt"""
    total_cost = 0
    errors = []
    alert = []

    output = []  # Lista para almacenar todos los mensajes de salida
    output.append(
        f"{'Producto':<32} "
        f"{'Cantidad':<12} "
        f"{'Precio Unidad':<18} "
        f"{'Costo Total':<18}"
    )
    output.append("-" * 85)
    for sale in sales:
        if not any(
            price["Product"] == sale.get("Product") for price in prices
        ):
            errors.append(
                "Producto no encontrado en el catálogo: "
                + sale.get("Product")
                )
        result = process_sale(prices, sale, total_cost)
        if result:
            total_cost, rows, alert_msg = result
            output.extend(rows)
            alert.extend(alert_msg)
    write_to_csv(output)
    # Al final, imprimimos todo el contenido almacenado en 'output'
    output.append("-" * 85)
    # Guardar el contenido en un archivo de texto
    return total_cost, errors, alert, output


def process_sale(prices, sale, total_cost):
    """Realiza el calculo del costo total """
    product = sale.get("Product")
    quantity = sale.get("Quantity")
    rows = []
    alert_msg = []
    if not any(price["Product"] == product for price in prices):
        return None
    if not isinstance(quantity, (int, float)) or quantity < 0:
        alert_msg.append(
            f"Cantidad negativa para el producto {product}: {quantity}"
            ",se va a restar del total"
            )
    for item in prices:
        if item["Product"] == product:
            if quantity < 0:  # Si la cantidad es negativa, restamos
                total_cost -= item["price"] * abs(quantity)
            else:  # Si es positiva, sumamos
                total_cost += item["price"] * quantity
            product_str = f"{product:<35}"
            quantity_str = f"{quantity:<12}"
            price_str = f"{item['price']:<18.2f}"
            total_item_str = f"{item['price'] * quantity:<18.2f}"
            rows.append(
                product_str + quantity_str + price_str + total_item_str
            )
    return total_cost, rows, alert_msg


def write_to_csv(rows_to_write):
    "guarda el producto,cantidad y precio en un csv"
    with open(
        "ProductList.csv", mode="w", newline="", encoding='utf-8'
    ) as file:
        writer = csv.writer(file)
        for index, data_string in enumerate(rows_to_write):
            if index == 1:
                continue
            data = data_string.split()
            writer.writerow(data)


def main():
    """Función principal para ejecutar el programa."""
    if len(sys.argv) != 3:
        print(
            "Uso: python computeSales.py priceCatalogue.json "
            "salesRecord.json"
        )
        sys.exit(1)
    price_file = sys.argv[1]
    sales_file = sys.argv[2]
    start_time = time.time()
    price_data = load_json_file(price_file)
    sales_data = load_json_file(sales_file)
    for product in price_data:
        if "title" in product:
            product["Product"] = product.pop("title")
    result = compute_total_sales(price_data, sales_data)
    total_sales, error_list, alert_list, output = result
    for line in output:
        print(line)

    elapsed_time = time.time() - start_time
    result_text = (
        f"Total de ventas calculado: ${total_sales:.2f}\n"
        f"Tiempo de ejecución: {elapsed_time:.4f} segundos\n"
    )
    if error_list:
        result_text += "Errores encontrados:\n" + "\n".join(error_list) + "\n"
    if alert_list:
        result_text += "Alertas encontradas:\n" + "\n".join(alert_list) + "\n"
    print(result_text)
    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        result_file.write("\n".join(output))
        result_file.write("\n" + result_text)


if __name__ == "__main__":
    main()
