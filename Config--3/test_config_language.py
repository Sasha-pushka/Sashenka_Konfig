from config_language import process_yaml

def test_case(description, yaml_input, expected_ucl):
    """Функция для выполнения одного тестового случая."""
    print(f"Running test: {description}")
    try:
        result = process_yaml(yaml_input)
        if result == expected_ucl:
            print("✅ Test passed")
        else:
            print("❌ Test failed")
            print("Expected:")
            print("\n".join(expected_ucl))
            print("Got:")
            print("\n".join(result))
    except Exception as e:
        print(f"❌ Test raised an exception: {e}")

def run_tests():
    """Запуск всех тестов."""
    test_case(
        "Web server config",
        {
            "host": "localhost",
            "port": 8080,
            "ssl_enabled": False
        },
        [
            "host is \"localhost\"",
            "port is 8080",
            "ssl_enabled is false"
        ]
    )

    test_case(
        "IoT device config",
        {
            "id": "sensor_01",
            "location": "warehouse",
            "temperature_threshold": "?[20 + 5]",
            "humidity_threshold": "?[60 - 10]"
        },
        [
            "id is \"sensor_01\"",
            "location is \"warehouse\"",
            "temperature_threshold is 25",
            "humidity_threshold is 50"
        ]
    )

    test_case(
        "Game config",
        {
            "title": "Adventure Quest",
            "version": 1.2,
            "fullscreen": True
        },
        [
            "title is \"Adventure Quest\"",
            "version is 1.2",
            "fullscreen is true"
        ]
    )

if __name__ == "__main__":
    run_tests()
