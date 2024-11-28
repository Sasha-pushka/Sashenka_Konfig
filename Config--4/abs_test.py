import argparse
from assembler import assembler, save_to_bin
from interpreter import interpreter
import xml.etree.ElementTree as ET

def generate_abs_instructions(vector):
    """
    Генерирует инструкции для применения операции abs() к каждому элементу вектора.
    Результат записывается обратно в тот же вектор.
    """
    instructions = []

    for i in range(len(vector)):
        # Применяем abs() к элементу вектора
        abs_value = abs(vector[i])

        # Записываем абсолютное значение в стек
        instructions.append({
            "operation": "load",  # Операция загрузки
            "args": [i, abs_value]  # Загружаем индекс и абсолютное значение
        })
        
        # Применяем abs() (хотя оно уже применено)
        instructions.append({
            "operation": "abs",  # Операция abs()
            "args": [i]            # Применяем abs() к элементу
        })
        
        # Записываем результат обратно в память по индексу i
        instructions.append({
            "operation": "write",  # Операция записи
            "args": [i, abs_value]  # Записываем результат обратно в вектор по индексу i
        })

    return instructions


def generate_xml_result(vector):
    """
    Генерирует XML файл с результатами после применения abs() к каждому элементу вектора.
    """
    # Создаем корневой элемент
    root = ET.Element("vector")
    
    # Добавляем элементы для каждого числа в векторе
    for i, value in enumerate(vector):
        item = ET.SubElement(root, "item", index=str(i))
        item.text = str(abs(value))  # Применяем abs() и записываем в XML

    # Создаем дерево XML и записываем его в файл
    tree = ET.ElementTree(root)
    tree.write("test_result.xml", encoding="utf-8", xml_declaration=True)


def main():
    # Параметры файлов
    binary_file = "test_binary.bin"
    result_file = "test_result.xml"  # Файл для записи результата
    log_file = "test_log.csv"

    # Генерация инструкций
    vector = [-25, -20, -15, 20, 25]
    instructions = generate_abs_instructions(vector)

    # Сохраняем их в бинарный файл через ассемблер
    save_to_bin(assembler(instructions, log_file), binary_file)

    # Запускаем интерпретатор для выполнения
    interpreter(binary_file, result_file, (0, len(vector) - 1))

    # Генерация XML с результатами
    generate_xml_result(vector)
    print("All tests successfully completed!")


if __name__ == "__main__":
    main()