# YAML to Custom Config Language Converter

Этот инструмент предназначен для преобразования данных из формата YAML в учебный конфигурационный язык, соответствующий специфическим требованиям. Инструмент реализует командную строку для обработки входного YAML и генерации выходного файла с конфигурацией в формате, требуемом в учебных заданиях.

## Особенности

- Преобразует YAML в учебный конфигурационный язык.
- Поддерживает многострочные комментарии в формате `#[ ... ]#`.
- Преобразует массивы в формат `{ значение. значение. ... }`.
- Преобразует словари в формат `dict( имя = значение, ... )`.
- Поддерживает вычисление и подстановку констант с помощью шаблонов типа `{{имя}}`.
- Проверка правильности имён в формате `[a-zA-Z][_a-zA-Z0-9]*`.

## Установка
Установите необходимые зависимости:
```bash
pip install -r requirements.txt
```
Использование
1. Преобразование YAML в конфигурационный язык
Для преобразования файла input.yaml в конфигурационный формат, выполните команду:
```bash
python config_language.py input.yaml output.txt
```
input.yaml — путь к файлу YAML, который нужно преобразовать.
output.txt — путь к файлу, куда будет записан результат.
Чтобы запустить заготовленные тесты:
```bash
python test_config_language.py
```
2. Чтение данных из стандартного ввода
Если вы хотите использовать стандартный ввод, укажите - вместо пути к файлу:
```bash
python config_language.py - output.txt
```
Пример input.yaml
```yaml
# Пользовательские данные
user:
  name: "JohnDoe"
  age: 30
  hobbies:
    - programming
    - cycling
    - reading

# Параметры сервера
server:
  host: "localhost"
  port: 8080
  endpoints:
    - "/api/v1/users"
    - "/api/v1/orders"
  settings:
    max_connections: 100
    debug: true

# Предопределённые константы
constants:
  app_name: "MyApplication"
  version: 1.2

# Использование вычисления констант
config:
  app: "{{app_name}}"
  ver: "{{version}}"

# Сложные структуры
items:
  - 1
  - 2
  - 3
  - "four"
  - true

robot:
  name: "CleanerBot"
  battery: 95
  modes:
    - auto
    - spot
  sensors:
    lidar: true
    camera: true
    infrared: false

# Пример многострочного комментария
multiline_comment: |
  #[ 
  Это многострочный 
  комментарий для конфигурации.
  ]#
``` 
Пример результата в output.txt
```plaintext
#[ 
Это автоматически сгенерированный файл.
]#
dict(
    user = dict(
        name = @"JohnDoe",
        age = 30,
        hobbies = { @"programming". @"cycling". @"reading" }
    ),
    server = dict(
        host = @"localhost",
        port = 8080,
        endpoints = { @"/api/v1/users". @"/api/v1/orders" },
        settings = dict(
            max_connections = 100,
            debug = @"true"
        )
    ),
    constants = dict(
        app_name = @"MyApplication",
        version = 1.2
    ),
    config = dict(
        app = @"MyApplication",
        ver = 1.2
    ),
    items = { 1. 2. 3. @"four". @"true" },
    robot = dict(
        name = @"CleanerBot",
        battery = 95,
        modes = { @"auto". @"spot" },
        sensors = dict(
            lidar = @"true",
            camera = @"true",
            infrared = @"false"
        )
    ),
    multiline_comment = #[ 
Это многострочный 
комментарий для конфигурации.
]#
)
```
Как это работает
Чтение YAML: Входной YAML-файл обрабатывается с помощью библиотеки PyYAML.
Преобразование в конфигурацию: Данные из YAML преобразуются в требуемый формат конфигурационного языка с использованием стандартных Python-функций для обработки строк, списков и словарей.
Константы: Константы объявляются через def имя = значение;, и их значения могут быть вычислены через |имя|.
Комментарии: Многострочные комментарии обрабатываются в формате #[ ... ]#.
```bash
pip install pyyaml
```