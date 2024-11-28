import yaml
import argparse
import re
import sys

# Поддержка операций для вычисления константных выражений
def eval_expression(expr, constants):
    """Вычисление константного выражения."""
    # Заменяем имена на соответствующие значения констант
    for name, value in constants.items():
        expr = expr.replace(name, str(value))
    
    # Заменяем операции и функции на аналоги Python
    expr = expr.replace('mod', '%').replace('chr', 'chr')
    
    try:
        # Возвращаем результат выполнения выражения
        return eval(expr)
    except Exception as e:
        raise ValueError(f"Error evaluating expression '{expr}': {e}")

def parse_arguments():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(description="YAML to UCL Translator")
    parser.add_argument("input", help="Path to input YAML file")
    parser.add_argument("output", help="Path to output UCL file")
    return parser.parse_args()

def validate_name(name):
    """Проверяет, соответствует ли имя синтаксису [a-zA-Z_][a-zA-Z0-9_]*."""
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
        raise ValueError(f"Invalid name syntax: {name}")

def validate_value(value):
    """Проверяет значение на соответствие числам, строкам или массивам."""
    if isinstance(value, bool):  # Приводим True/False к true/false
        return str(value).lower()
    elif isinstance(value, int) or isinstance(value, float):
        return str(value)
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, list):
        return f"( {', '.join(map(validate_value, value))} )"
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")

def process_item(key, value, constants, indent=0):
    """Обрабатывает отдельный элемент, поддерживает вложенность и комментарии."""
    validate_name(key)
    indent_space = "  " * indent
    result = []

    if isinstance(value, dict):
        # Если значение — словарь, обрабатываем его как блок
        result.append(f"{indent_space}{key} {{")
        for subkey, subvalue in value.items():
            result.extend(process_item(subkey, subvalue, constants, indent + 1))
        result.append(f"{indent_space}}}")
    elif isinstance(value, list):
        # Если значение — массив
        array_value = validate_value(value)
        result.append(f"{indent_space}{key} is {array_value}")
    elif isinstance(value, str) and value.startswith('?[') and value.endswith(']'):
        # Если значение — выражение
        expression = value[2:-1]  # Убираем "?[" и "]"
        evaluated_value = eval_expression(expression, constants)
        result.append(f"{indent_space}{key} is {evaluated_value}")
        constants[key] = evaluated_value
    elif isinstance(value, str) and value.startswith('*'):
        # Однострочный комментарий
        result.append(f"{indent_space}{value}")
    elif isinstance(value, str) and value.startswith('#|') and value.endswith('|#'):
        # Многострочный комментарий
        comment_lines = value.splitlines()
        result.append(f"{indent_space}#|")
        for line in comment_lines[1:-1]:
            result.append(f"{indent_space}  {line.strip()}")
        result.append(f"{indent_space}|#")
    else:
        # Простое значение
        result.append(f"{indent_space}{key} is {validate_value(value)}")
        constants[key] = value

    return result

def process_yaml(yaml_data, indent=0):
    """Преобразует YAML в UCL с поддержкой вложенности и комментариев."""
    if not isinstance(yaml_data, dict):
        raise ValueError("Root of YAML file must be a dictionary.")
    constants = {}
    result = []
    for key, value in yaml_data.items():
        result.extend(process_item(key, value, constants, indent))
    return result

def read_yaml(input_path):
    """Считывает YAML файл."""
    with open(input_path, "r", encoding="utf-8") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML: {e}")

def write_ucl(output_path, ucl_lines):
    """Записывает результат в UCL файл."""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(ucl_lines))

def main():
    """Главная функция."""
    args = parse_arguments()

    # Чтение и обработка YAML
    try:
        yaml_data = read_yaml(args.input)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    # Преобразование в UCL
    try:
        ucl_lines = process_yaml(yaml_data)
    except ValueError as e:
        print(f"Error processing YAML: {e}")
        sys.exit(1)

    # Запись в выходной файл
    try:
        write_ucl(args.output, ucl_lines)
        print(f"Translation completed successfully. Output saved to {args.output}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
