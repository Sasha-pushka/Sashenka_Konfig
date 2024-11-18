import sys
import zipfile
import argparse
import posixpath

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.fs = {}
        self.load_zip()

    def load_zip(self):
        with zipfile.ZipFile(self.zip_path, 'r') as z:
            for file in z.namelist():
                self.add_path(file)

    def add_path(self, path):
        parts = path.strip('/').split('/')
        current = self.fs
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def save_zip(self):
        with zipfile.ZipFile(self.zip_path, 'w') as z:
            self.write_fs(z, self.fs, "")

    def write_fs(self, z, current, path):
        for name, content in current.items():
            current_path = posixpath.join(path, name)
            if isinstance(content, dict):
                # Добавляем директорию (заканчивается слешем)
                z.writestr(current_path + '/', '')
                self.write_fs(z, content, current_path)
            else:
                # Добавляем файл
                z.writestr(current_path, content)

    def list_dir(self, path):
        dir = self.navigate(path)
        if dir is None:
            return None
        return sorted(dir.keys())

    def navigate(self, path):
        if path.startswith('/'):
            parts = path.strip('/').split('/')
            current = self.fs
        else:
            parts = path.split('/')
            current = self.fs
        for part in parts:
            if part == '..':
                # Для простоты не реализуем переход вверх
                return None
            elif part == '.' or part == '':
                continue
            elif part in current and isinstance(current[part], dict):
                current = current[part]
            else:
                return None
        return current

    def move(self, src, dest, cwd):
        # Определяем абсолютные пути
        src_path = posixpath.join(cwd, src) if not posixpath.isabs(src) else src
        dest_path = posixpath.join(cwd, dest) if not posixpath.isabs(dest) else dest

        # Нормализуем пути
        src_path = posixpath.normpath(src_path)
        dest_path = posixpath.normpath(dest_path)

        src_parts = src_path.strip('/').split('/')
        dest_parts = dest_path.strip('/').split('/')

        # Находим родительскую директорию источника
        src_parent = self.fs
        for part in src_parts[:-1]:
            if part in src_parent and isinstance(src_parent[part], dict):
                src_parent = src_parent[part]
            else:
                return False  # Источник не найден

        # Извлекаем элемент для перемещения
        item = src_parent.pop(src_parts[-1], None)
        if item is None:
            return False  # Элемент для перемещения не найден

        # Определяем, является ли назначение существующей директорией
        dest_dir = self.navigate(dest_path)
        if dest_dir is not None and isinstance(dest_dir, dict):
            # Перемещение внутрь существующей директории
            if src_parts[-1] in dest_dir:
                # Имя уже существует в целевой директории
                return False
            dest_dir[src_parts[-1]] = item
        else:
            # Переименование или перемещение с новым именем
            dest_parent = self.fs
            for part in dest_parts[:-1]:
                if part not in dest_parent:
                    dest_parent[part] = {}
                elif not isinstance(dest_parent[part], dict):
                    return False  # Некорректный путь назначения
                dest_parent = dest_parent[part]
            if dest_parts[-1] in dest_parent:
                # Имя уже существует в целевой директории
                return False
            dest_parent[dest_parts[-1]] = item

        return True

def parse_args():
    parser = argparse.ArgumentParser(description='Эмулятор оболочки ОС с виртуальной файловой системой.')
    parser.add_argument('username', help='Имя пользователя для приглашения к вводу.')
    parser.add_argument('zip_path', help='Путь к архиву виртуальной файловой системы (zip).')
    return parser.parse_args()

def main():
    args = parse_args()
    username = args.username
    zip_path = args.zip_path

    if not zip_path.endswith('.zip'):
        print(f"Ошибка: Файл {zip_path} не является zip-архивом.")
        sys.exit(1)

    try:
        vfs = VirtualFileSystem(zip_path)
    except zipfile.BadZipFile:
        print(f"Ошибка: Файл {zip_path} не является корректным zip-архивом.")
        sys.exit(1)

    cwd = '/'

    while True:
        prompt = f"{username}@emulator:{cwd}$ "
        try:
            command = input(prompt).strip()
        except EOFError:
            print()
            break

        if not command:
            continue

        parts = command.split()
        cmd = parts[0]
        args_cmd = parts[1:]

        if cmd == 'exit':
            break
        elif cmd == 'ls':
            target = args_cmd[0] if args_cmd else cwd
            target_path = posixpath.join(cwd, target) if not posixpath.isabs(target) else target
            target_path = posixpath.normpath(target_path)
            listing = vfs.list_dir(target_path)
            if listing is None:
                print(f"ls: cannot access '{target}': No such file or directory")
            else:
                print('  '.join(listing))
        elif cmd == 'cd':
            if not args_cmd:
                cwd = '/'
                continue
            target = args_cmd[0]
            if target == '/':
                cwd = '/'
                continue
            target_path = posixpath.join(cwd, target) if not posixpath.isabs(target) else target
            target_path = posixpath.normpath(target_path)
            dir = vfs.navigate(target_path)
            if dir is not None:
                cwd = target_path
            else:
                print(f"cd: no such file or directory: {target}")
        elif cmd == 'pwd':
            print(cwd)
        elif cmd == 'whoami':
            print(username)
        elif cmd == 'mv':
            if len(args_cmd) != 2:
                print("Использование: mv <источник> <назначение>")
                continue
            src, dest = args_cmd
            success = vfs.move(src, dest, cwd)
            if not success:
                print(f"mv: cannot move '{src}' to '{dest}': Operation failed")
        else:
            print(f"{cmd}: команда не найдена")

    try:
        vfs.save_zip()
        print("Выход из эмулятора. Изменения сохранены.")
    except Exception as e:
        print(f"Ошибка при сохранении архива: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
