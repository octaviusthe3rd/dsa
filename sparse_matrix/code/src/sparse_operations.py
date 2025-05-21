import json
import random
import os
import time
import sys

def read_data(data_file):
    csr_entries = []
    with open(data_file, 'r') as file:
        lines = file.readlines()
        
        for line_num in range(2, len(lines)):
            line = lines[line_num].strip()
            if not line:
                continue
                
            try:
                line = line.replace('(', '').replace(')', '')
                
                if ',' in line:
                    elements_str = [x.strip() for x in line.split(',')]
                else:
                    elements_str = [x.strip() for x in line.split()]
                
                elements = [int(x) for x in elements_str if x]
                
                if len(elements) == 3:
                    csr_entries.append(elements)
                else:
                    print(f"Line {line_num + 1} has {len(elements)} elements instead of 3")
            except ValueError as e:
                print(f"Error extracting line {line_num + 1}, {str(e)}")
                continue
    
    return csr_entries

def save_to_json(csr_entries, output_file="csr_matrices.json"):
    matrices_dict = {}
    for idx, entry in enumerate(csr_entries):
        key = str(idx + 1)
        matrices_dict[key] = [entry]
    
    with open(output_file, 'w') as f:
        json.dump(matrices_dict, f, indent=2)
    return matrices_dict

def load_json(json_file="csr_matrices.json"):
    with open(json_file, 'r') as f:
        matrices_dict = json.load(f)
    
    return matrices_dict

def transpose(matrix):
    transposed = []
    for entry in matrix:
        row, col, value = entry
        transposed.append([col, row, value])
    return transposed

def multiply(matrix_a, matrix_b):
    b_dict = {}
    for row, col, val in matrix_b:
        if col not in b_dict:
            b_dict[col] = []
        b_dict[col].append((row, val))
    
    result = {}
    
    for a_row, a_col, a_val in matrix_a:
        for b_col, b_entries in b_dict.items():
            for b_row, b_val in b_entries:
                if a_col == b_row:
                    product = a_val * b_val
                    if product != 0:
                        key = (a_row, b_col)
                        if key in result:
                            result[key] += product
                        else:
                            result[key] = product
    
    return [[row, col, val] for (row, col), val in result.items() if val != 0]

def add(matrix_a, matrix_b):
    result = {}
    
    for row, col, val in matrix_a:
        result[(row, col)] = val
    
    for row, col, val in matrix_b:
        if (row, col) in result:
            result[(row, col)] += val
        else:
            result[(row, col)] = val
    
    return [[row, col, val] for (row, col), val in result.items() if val != 0]

def subtract(matrix_a, matrix_b):
    result = {}
    
    for row, col, val in matrix_a:
        result[(row, col)] = val
    
    for row, col, val in matrix_b:
        if (row, col) in result:
            result[(row, col)] -= val
        else:
            result[(row, col)] = -val

    return [[row, col, val] for (row, col), val in result.items() if val != 0]

def display(matrix, label="Matrix"):
    print("-" * 40)
    for entry in matrix:
        print(f"  [{entry[0]}, {entry[1]}] = {entry[2]}")
    print("-" * 40)

def process_matrices(file_path, json_file="csr_matrices.json", force_rebuild=False):
    if not os.path.exists(json_file) or force_rebuild:
        print(f"Reading CSR entries")
        csr_entries = read_data(file_path)
        if len(csr_entries) < 2:
            return "No CSR entries found"
        matrices_dict = save_to_json(csr_entries, json_file)
    else:
        print(f"Loading matrices from JSON file")
        matrices_dict = load_json(json_file)

    operations = ["multiply", "add", "subtract"]
    matrix_ids = list(matrices_dict.keys())

    if len(matrix_ids) < 2:
        return "Not enough matrices"

    for i in range(len(matrix_ids) // 2):
        if len(matrix_ids) < 2:
            print("Not enough matrices for operation")
            break

        id_a, id_b = random.sample(matrix_ids, 2)
        matrix_a = matrices_dict[id_a]
        matrix_b = matrices_dict[id_b]

        operation = random.choice(operations)
        print(f"\n\nOperation {i+1}: {operation.upper()}")
        print("=" * 60)
        display(matrix_a, f"Matrix A (ID: {id_a})")
        display(matrix_b, f"Matrix B (ID: {id_b})")

        if operation == "multiply":
            result = multiply(matrix_a, matrix_b)
            op_symbol = "×"
        elif operation == "add":
            result = add(matrix_a, matrix_b)
            op_symbol = "+"
        else:
            result = subtract(matrix_a, matrix_b)
            op_symbol = "-"

        display(result, f"Result of A {op_symbol} B")

        matrix_ids.remove(id_a)
        matrix_ids.remove(id_b)

    return "Operations completed"

if __name__ == "__main__":
    file_path = "../../sample_inputs/easy_sample_01_3.txt"
    json_file = "csr_matrices.json"
    force_rebuild = "--force" in sys.argv

    try:
        result = process_matrices(file_path, json_file, force_rebuild)
        print(f"\nFinal result: {result}")
    except FileNotFoundError:
        print(f"File {file_path} not found. Please specify path to file.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()