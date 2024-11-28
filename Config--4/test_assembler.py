from assembler import assembler, serializer, log_operation

# Тестирование функции assembler
def test_load():
    bytes = assembler([("load", 229, 979)])
    assert bytes == [0x55, 0x0E, 0x00, 0x00, 0xD3, 0x03, 0x00]
    print("test_load passed")

def test_read():
    bytes = assembler([("read", 92, 4, 106)])
    assert bytes == [0xC2, 0x05, 0x00, 0x00, 0x04, 0xD4, 0x00, 0x00, 0x00]
    print("test_read passed")

def test_write():
    bytes = assembler([("write", 970, 629)])
    assert bytes == [0xA6, 0x3C, 0x00, 0x00, 0x75, 0x02, 0x00, 0x00]
    print("test_write passed")

def test_abs():
    bytes = assembler([("abs", 226, 178, 487)])
    assert bytes == [0x2A, 0x4E, 0x16, 0x00, 0x00, 0xCE, 0x03, 0x00, 0x00]
    print("test_abs passed")

# Тестирование функции serializer
def test_serializer_load():
    cmd = 5
    fields = ((229, 4), (979, 32))
    size = 7
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\x55\x0E\x00\x00\xD3\x03\x00'
    print("test_serializer_load passed")

def test_serializer_read():
    cmd = 2
    fields = ((92, 4), (4, 32), (106, 41))
    size = 9
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\xC2\x05\x00\x00\x04\xD4\x00\x00\x00'
    print("test_serializer_read passed")
    
def test_serializer_write():
    cmd = 6
    fields = ((970, 4), (629, 32))
    size = 8
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\xA6\x3C\x00\x00\x75\x02\x00\x00'
    print("test_serializer_write passed")
    
def test_serializer_abs():
    cmd = 10
    fields = ((226, 4), (178, 13), (487, 41))
    size = 9
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\x2A\x4E\x16\x00\x00\xCE\x03\x00\x00'
    print("test_serializer_abs passed")

# Запуск всех тестов и вывод финального отчета
def run_tests():
    try:
        test_load()
        test_read()
        test_write()
        test_abs()
        test_serializer_load()
        test_serializer_read()
        test_serializer_write()
        test_serializer_abs()
        print("\nAll tests passed successfully!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")

# Запуск тестов
run_tests()
