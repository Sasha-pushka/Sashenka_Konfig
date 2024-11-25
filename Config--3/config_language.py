import yaml
import re
import argparse
import sys

constants = {}

def parse_yaml(input_text):
    """Парсинг YAML текста."""
    try:
        return yaml.safe_load(input_text)
    except yaml.YAMLError as e:
        raise ValueError(f"Ошибка синтаксиса YAML: {e}")


def is_valid_name(name):
    """Проверяет, соответствует ли имя формату [a-zA-Z][_a-zA-Z0-9]*."""
    return re.match(r"^[a-zA-Z][_a-zA-Z0-9]*$", name)


def declare_constant(name, value):
    """Объявляет константу."""
    if not is_valid_name(name):
        raise ValueError(f"Недопустимое имя для константы: '{name}'")
    constants[name] = value
    return f"def {name} = {convert_to_custom_syntax(value)};"


def evaluate_constant(name):
    """Вычисляет значение константы."""
    if name not in constants:
        raise ValueError(f"Константа '{name}' не определена")
    return constants[name]


def add_multiline_comment(comment):
    """Добавляет многострочный комментарий."""
    return f"#[\n{comment}\n]#"


def convert_to_custom_syntax(data, indent=0):
    """Преобразование данных в учебный конфигурационный язык."""
    indent_str = "    " * indent
    next_indent_str = "    " * (indent + 1)

    if isinstance(data, dict):
        entries = []
        for key, value in data.items():
            if not is_valid_name(key):
                raise ValueError(f"Недопустимое имя: '{key}'")
            entries.append(
                f"{next_indent_str}{key} = {convert_to_custom_syntax(value, indent + 1)}"
            )
        return f"dict(\n{',\n'.join(entries)}\n{indent_str})"
    elif isinstance(data, list):
        elements = [convert_to_custom_syntax(item, indent + 1) for item in data]
        return f"{{ {'. '.join(elements)} }}"
    elif isinstance(data, str):
        return f'@"{data}"'
    elif isinstance(data, (int, float)):
        return str(data)
    else:
        raise ValueError(f"Неизвестный тип данных: {type(data)}")


def main():
    """Главная функция для обработки аргументов командной строки и запуска преобразования."""
    parser = argparse.ArgumentParser(description="YAML to custom config language converter")
    parser.add_argument(
        "input_file",
        type=str,
        help="Путь к входному YAML-файлу (или '-' для стандартного ввода)",
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Путь к выходному файлу для записи преобразованного текста",
    )
    args = parser.parse_args()

    try:
        # Чтение входного файла или стандартного ввода
        if args.input_file == "-":
            input_text = sys.stdin.read()
        else:
            with open(args.input_file, "r", encoding="utf-8") as f:
                input_text = f.read()

        yaml_data = parse_yaml(input_text)

        # Преобразование данных
        custom_syntax = add_multiline_comment("Это автоматически сгенерированный файл.") + "\n"
        custom_syntax += convert_to_custom_syntax(yaml_data)

        # Запись в выходной файл
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(custom_syntax)

        print(f"Преобразование завершено успешно. Результат записан в {args.output_file}")
    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
