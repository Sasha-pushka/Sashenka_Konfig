import argparse

# Логирование операций
def log_operation(log_path, operation_code, *args):
    if log_path is not None:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"Operation={operation_code},B={args[0]},C={args[1]}\n")

# Сериализация команды в бинарный формат
def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd  # Код операции
    for value, offset in fields:
        bits |= (value << offset)  # Установка значения в определённое смещение
    return bits.to_bytes(size, byteorder='little')  # Преобразование в байты

# Ассемблер
def assembler(instructions, log_path=None):
    byte_code = []
    for operation, *args in instructions:
        if operation == "load":
            B, C = args
            byte_code += serializer(5, [(B, 4), (C, 32)], 7)  # Загрузка константы
            log_operation(log_path, 5, B, C)
        elif operation == "read":
            B, C, D = args
            byte_code += serializer(2, [(B, 4), (C, 32), (D, 41)], 9)  # Чтение значения из памяти
            log_operation(log_path, 2, B, C)
        elif operation == "write":
            B, C = args
            byte_code += serializer(6, [(B, 4), (C, 32)], 8)  # Запись значения в память
            log_operation(log_path, 6, B, C)
        elif operation == "abs":
            B, C, D = args
            byte_code += serializer(10, [(B, 4), (C, 13), (D, 41)], 9)  # Унарная операция: abs()
            log_operation(log_path, 10, B, C)
    return byte_code

# Чтение инструкций из файла
def assemble(instructions_path: str, log_path=None):
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = [[int(j) if j.isdigit() else j for j in i.split()] for i in f.readlines()]
    return assembler(instructions, log_path)

# Сохранение бинарных инструкций в файл
def save_to_bin(assembled_instructions, binary_path):
    with open(binary_path, "wb") as binary_file:
        binary_file.write(bytes(assembled_instructions))

# Основная логика
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembling the instructions file to the byte-code.")
    parser.add_argument("instructions_path", help="Path to the instructions file (txt)")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("log_path", help="Path to the log file (csv)")
    args = parser.parse_args()
    
    with open(args.log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"Operation,B (Address),C (Constant/Address)\n")
    
    assembled_instructions = assemble(args.instructions_path, args.log_path)
    save_to_bin(assembled_instructions, args.binary_path)
