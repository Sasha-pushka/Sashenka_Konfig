from config_language import (
    parse_yaml,
    convert_to_custom_syntax,
    add_multiline_comment,
    declare_constant,
    evaluate_constant,
)


def run_test(test_name, input_data, expected_output, test_function):
    try:
        result = test_function(input_data)
        if result == expected_output:
            print(f"[PASSED] {test_name}")
        else:
            print(f"[FAILED] {test_name}")
            print("  Expected:")
            print(expected_output)
            print("  Got:")
            print(result)
    except Exception as e:
        print(f"[FAILED] {test_name}")
        print(f"  Exception: {e}")


def test_constants():
    """Тест объявления и вычисления констант."""
    # Объявляем константу
    constant_declared = declare_constant("my_constant", 123)
    if constant_declared == "def my_constant = 123;":
        print("[PASSED] Declare constant")
    else:
        print("[FAILED] Declare constant")
        print("  Got:")
        print(constant_declared)

    # Вычисляем константу
    try:
        constant_value = evaluate_constant("my_constant")
        if constant_value == 123:
            print("[PASSED] Evaluate constant")
        else:
            print("[FAILED] Evaluate constant")
            print("  Got:")
            print(constant_value)
    except Exception as e:
        print("[FAILED] Evaluate constant")
        print(f"  Exception: {e}")

    # Вычисляем несуществующую константу
    try:
        evaluate_constant("non_existent")
        print("[FAILED] Evaluate non-existent constant")
    except ValueError:
        print("[PASSED] Evaluate non-existent constant")


def main_tests():
    print("Running tests...")

    # Тест: Преобразование словаря
    run_test(
        "Test dictionary conversion",
        {"key1": "value1", "key2": 123},
        'dict(\n    key1 = @"value1",\n    key2 = 123\n)',
        lambda data: convert_to_custom_syntax(data),
    )

    # Тест: Преобразование массива
    run_test(
        "Test array conversion",
        ["item1", "item2", 42],
        '{ @"item1". @"item2". 42 }',
        lambda data: convert_to_custom_syntax(data),
    )

    # Тест: Многострочный комментарий
    run_test(
        "Test multiline comment",
        "Это многострочный комментарий",
        "#[\nЭто многострочный комментарий\n]#",
        lambda comment: add_multiline_comment(comment),
    )

    # Тест: Константы
    test_constants()


if __name__ == "__main__":
    main_tests()
