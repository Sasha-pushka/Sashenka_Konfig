import argparse

def interpreter(binary_path, result_path, memory_range):
    memory = [0] * (2**10)  # Увеличиваем размер памяти до 1 МБ
    # Чтение бинарного файла
    with open(binary_path, "rb") as binary_file:
        byte_code = binary_file.read()
    memory[5]=970
    # Декодирование и исполнение команд
    i = 0
    while i < len(byte_code):
        command = byte_code[i] & 0x0F  # Биты 0-3 для команды
        print(f"Reading byte {i}: Command code {command}, byte value {byte_code[i]}")  # Логирование команды

        if command == 5:  # load (Загрузка константы)
            data = int.from_bytes(byte_code[i:i+7], "little")
            B = (data >> 4) & 0x1FFFFFF  # Биты 4-31 (адрес)
            C = (data >> 32) & 0x7FFFF   # Биты 32-50 (константа)
            if B < len(memory):  # Проверка на выход за границы памяти
                memory[B] = C
            i += 7

        elif command == 2:  # read (Чтение значения из памяти)
            data = int.from_bytes(byte_code[i:i+9], "little")
            B = (data >> 4) & 0x1FFFFFF  # Биты 4-31 (адрес, куда)
            C = (data >> 32) & 0x1FF     # Биты 32-40 (смещение)
            D = (data >> 41) & 0x1FFFFFF  # Биты 41-68 (адрес, откуда)
            if B < len(memory) and D < len(memory):  # Проверка на выход за границы памяти
                effective_address = memory[D] + C
                if effective_address < len(memory):  # Проверка на выход за границы памяти
                    memory[B] = memory[effective_address]
                i += 9
            else:
                i += 9  # Пропускаем обработку этой команды, если адрес вне диапазона

        elif command == 6:  # write (Запись значения в память)
            data = int.from_bytes(byte_code[i:i+8], "little")
            B = (data >> 4) & 0x1FFFFFF  # Биты 4-31 (адрес, куда)
            C = (data >> 32) & 0xFFFFFFFF  # Биты 32-59 (адрес, откуда)
            if B < len(memory) and C < len(memory):  # Проверка на выход за границы памяти
                memory[B] = memory[C]
            i += 8

        elif command == 10:  # abs (Унарная операция)
            data = int.from_bytes(byte_code[i:i+9], "little")
            B = (data >> 4) & 0x1FF       # Биты 4-12 (смещение)
            C = (data >> 13) & 0x7FFFFF   # Биты 13-40 (адрес, куда)
            D = (data >> 41) & 0x1FFFFFF  # Биты 41-68 (адрес, откуда)
            if C < len(memory) and D < len(memory):  # Проверка на выход за границы памяти
                effective_address = memory[D] + B
                if effective_address < len(memory):  # Проверка на выход за границы памяти
                    memory[C] = abs(memory[effective_address])
                i += 9
            else:
                i += 9  # Пропускаем обработку этой команды, если адрес вне диапазона

        else:
            i += 1  # Пропуск неизвестной команды для продолжения анализа

    # Сохранение памяти в CSV файл
    with open(result_path, "w", encoding="utf-8") as result_file:
        result_file.write("Address,Value\n")
        for address in range(memory_range[0], memory_range[1] + 1):
            result_file.write(f"{address},{memory[address]}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for the binary commands of a virtual machine.")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("result_path", help="Path to the result file (csv)")
    parser.add_argument("first_index", type=int, help="First index of memory range")
    parser.add_argument("last_index", type=int, help="Last index of memory range")
    args = parser.parse_args()

    interpreter(args.binary_path, args.result_path, (args.first_index, args.last_index))
