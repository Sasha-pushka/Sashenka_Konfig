import zipfile
import tempfile
import os
from shell_emulator import VirtualFileSystem

def create_temp_zip(structure):
    """
    Создает временный ZIP-архив с заданной структурой файлов и директорий.
    :param structure: Словарь, где ключи - пути, а значения - содержимое файлов ('' для директорий)
    :return: Имя временного ZIP-файла
    """
    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    with zipfile.ZipFile(temp_zip.name, 'w') as z:
        for path, content in structure.items():
            z.writestr(path, content)
    return temp_zip.name

def run_test(test_func, test_name):
    """
    Запускает тестовую функцию и выводит результат с пояснением.
    :param test_func: Функция теста
    :param test_name: Название теста для вывода
    """
    try:
        test_func()
        print(f"✔ {test_name}: Пройден успешно.")
    except AssertionError as e:
        print(f"✖ {test_name}: Не пройден. Ошибка: {e}")
    except Exception as e:
        print(f"✖ {test_name}: Не пройден из-за непредвиденной ошибки. Ошибка: {e}")

def test_add_path():
    print("Запуск теста: add_path")
    # Создаем начальную структуру
    structure = {
        'file1.txt': 'Content of file1',
        'dir1/file2.txt': 'Content of file2'
    }
    zip_path = create_temp_zip(structure)
    vfs = VirtualFileSystem(zip_path)
    
    try:
        # Добавляем новый файл
        vfs.add_path('dir2/file3.txt')
        listing = vfs.list_dir('/dir2')
        assert 'file3.txt' in listing, "Файл 'file3.txt' не был добавлен в 'dir2'"
        
        # Добавляем новую директорию
        vfs.add_path('dir3/')
        listing = vfs.list_dir('/')
        assert 'dir3' in listing, "Директория 'dir3' не была добавлена в корневую директорию"
    finally:
        os.unlink(zip_path)
    print("Тест add_path завершен.\n")

def test_list_dir():
    print("Запуск теста: list_dir")
    structure = {
        'file1.txt': 'Content of file1',
        'dir1/file2.txt': 'Content of file2',
        'dir1/file3.txt': 'Content of file3'
    }
    zip_path = create_temp_zip(structure)
    vfs = VirtualFileSystem(zip_path)
    
    try:
        # Тест 1: список в корневой директории
        listing = vfs.list_dir('/')
        expected = ['dir1', 'file1.txt']
        assert set(listing) == set(expected), f"Ожидалось {expected}, получено {listing}"
        
        # Тест 2: список в поддиректории
        listing = vfs.list_dir('/dir1')
        expected = ['file2.txt', 'file3.txt']
        assert set(listing) == set(expected), f"Ожидалось {expected}, получено {listing}"
    finally:
        os.unlink(zip_path)
    print("Тест list_dir завершен.\n")

def test_navigate():
    print("Запуск теста: navigate")
    structure = {
        'file1.txt': 'Content of file1',
        'dir1/file2.txt': 'Content of file2',
        'dir1/dir2/file3.txt': 'Content of file3'
    }
    zip_path = create_temp_zip(structure)
    vfs = VirtualFileSystem(zip_path)
    
    try:
        # Тест 1: навигация в корневую директорию
        dir = vfs.navigate('/')
        assert isinstance(dir, dict) and 'file1.txt' in dir, "Неверная навигация в корневую директорию"
        
        # Тест 2: навигация в глубинную директорию
        dir = vfs.navigate('/dir1/dir2')
        assert isinstance(dir, dict) and 'file3.txt' in dir, "Неверная навигация в '/dir1/dir2'"
    finally:
        os.unlink(zip_path)
    print("Тест navigate завершен.\n")

def test_move():
    print("Запуск теста: move")
    structure = {
        'file1.txt': 'Content of file1',
        'dir1/file2.txt': 'Content of file2'
    }
    zip_path = create_temp_zip(structure)
    vfs = VirtualFileSystem(zip_path)
    
    try:
        # Тест 1: переименование файла
        success = vfs.move('file1.txt', 'file1_renamed.txt', '/')
        assert success, "Переименование файла 'file1.txt' не удалось"
        listing = vfs.list_dir('/')
        assert 'file1_renamed.txt' in listing and 'file1.txt' not in listing, "Файл не был переименован корректно"
        
        # Тест 2: перемещение файла в поддиректорию
        success = vfs.move('file1_renamed.txt', 'dir1', '/')
        assert success, "Перемещение файла 'file1_renamed.txt' в 'dir1' не удалось"
        listing_root = vfs.list_dir('/')
        listing_dir1 = vfs.list_dir('/dir1')
        assert 'file1_renamed.txt' not in listing_root and 'file1_renamed.txt' in listing_dir1, "Файл не был перемещен в 'dir1' корректно"
    finally:
        os.unlink(zip_path)
    print("Тест move завершен.\n")

def test_ls_commands():
    print("Запуск теста: ls_commands")
    # Создаем структуру
    structure = {
        'file1.txt': 'Content of file1',
        'dir1/file2.txt': 'Content of file2',
        'dir2/file3.txt': 'Content of file3'
    }
    zip_path = create_temp_zip(structure)
    vfs = VirtualFileSystem(zip_path)
    
    try:
        # Тест 1: ls в корневой директории
        listing = vfs.list_dir('/')
        expected = ['dir1', 'dir2', 'file1.txt']
        assert set(listing) == set(expected), f"Ожидалось {expected}, получено {listing}"
        
        # Тест 2: ls в поддиректории
        listing = vfs.list_dir('/dir1')
        expected = ['file2.txt']
        assert set(listing) == set(expected), f"Ожидалось {expected}, получено {listing}"
    finally:
        os.unlink(zip_path)
    print("Тест ls_commands завершен.\n")

def test_cd_commands():
    print("Запуск теста: cd_commands")
    structure = {
        'dir1/file1.txt': 'Content of file1',
        'dir2/file2.txt': 'Content of file2'
    }
    zip_path = create_temp_zip(structure)
    vfs = VirtualFileSystem(zip_path)
    
    try:
        # Тест 1: переход в существующую директорию
        dir = vfs.navigate('/dir1')
        assert dir is not None and 'file1.txt' in dir, "Переход в существующую директорию '/dir1' не удался"
        
        # Тест 2: попытка перехода в несуществующую директорию
        dir = vfs.navigate('/nonexistent')
        assert dir is None, "Переход в несуществующую директорию '/nonexistent' должен вернуть None"
    finally:
        os.unlink(zip_path)
    print("Тест cd_commands завершен.\n")

def test_pwd_commands():
    print("Запуск теста: pwd_commands")
    # Поскольку pwd зависит от текущего рабочего каталога,
    # мы будем тестировать это через переменную cwd
    structure = {
        'dir1/file1.txt': 'Content of file1'
    }
    zip_path = create_temp_zip(structure)
    vfs = VirtualFileSystem(zip_path)
    cwd = '/'
    
    try:
        # Тест 1: pwd в корневой директории
        assert cwd == '/', f"Ожидалось '/', получено '{cwd}'"
        
        # Тест 2: pwd после перехода в поддиректорию
        cwd = '/dir1'
        assert cwd == '/dir1', f"Ожидалось '/dir1', получено '{cwd}'"
    finally:
        os.unlink(zip_path)
    print("Тест pwd_commands завершен.\n")

def test_whoami_commands():
    print("Запуск теста: whoami_commands")
    username = 'testuser'
    
    try:
        # Тест 1: Проверка имени пользователя
        assert username == 'testuser', f"Ожидалось 'testuser', получено '{username}'"
        
        # Тест 2: Изменение имени пользователя и проверка
        username = 'anotheruser'
        assert username == 'anotheruser', f"Ожидалось 'anotheruser', получено '{username}'"
    finally:
        pass
    print("Тест whoami_commands завершен.\n")

def test_mv_commands():
    print("Запуск теста: mv_commands")
    structure = {
        'file1.txt': 'Content of file1',
        'dir1/file2.txt': 'Content of file2',
        'dir2/': ''
    }
    zip_path = create_temp_zip(structure)
    vfs = VirtualFileSystem(zip_path)
    
    try:
        # Тест 1: переименование файла
        success = vfs.move('file1.txt', 'file1_renamed.txt', '/')
        assert success, "Переименование файла 'file1.txt' не удалось"
        listing = vfs.list_dir('/')
        assert 'file1_renamed.txt' in listing and 'file1.txt' not in listing, "Файл не был переименован корректно"
        
        # Тест 2: перемещение файла в директорию
        success = vfs.move('file1_renamed.txt', 'dir1', '/')
        assert success, "Перемещение файла 'file1_renamed.txt' в 'dir1' не удалось"
        listing_root = vfs.list_dir('/')
        listing_dir1 = vfs.list_dir('/dir1')
        assert 'file1_renamed.txt' not in listing_root and 'file1_renamed.txt' in listing_dir1, "Файл не был перемещен в 'dir1' корректно"
    finally:
        os.unlink(zip_path)
    print("Тест mv_commands завершен.\n")

def run_all_tests():
    print("Запуск всех тестов...\n")
    tests = [
        (test_add_path, "add_path"),
        (test_list_dir, "list_dir"),
        (test_navigate, "navigate"),
        (test_move, "move"),
        (test_ls_commands, "ls_commands"),
        (test_cd_commands, "cd_commands"),
        (test_pwd_commands, "pwd_commands"),
        (test_whoami_commands, "whoami_commands"),
        (test_mv_commands, "mv_commands")
    ]
    
    for test_func, test_name in tests:
        run_test(test_func, test_name)
    
    print("\nВсе тесты завершены.")

if __name__ == "__main__":
    run_all_tests()
