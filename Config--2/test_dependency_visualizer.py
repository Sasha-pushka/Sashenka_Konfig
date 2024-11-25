import os
from pathlib import Path
from subprocess import run, CalledProcessError
from dependency_visualizer import (
    get_git_commits_with_file,
    get_commit_files,
    build_mermaid_graph,
    save_graph_to_file,
)

# Путь для тестирования (создаётся временный Git-репозиторий)
TEST_REPO_PATH = Path("test_repo")
TARGET_FILE = "target_file.txt"
OUTPUT_FILE = Path("output.mmd")

def run_command(command, cwd=None):
    """Выполняет команду в терминале."""
    try:
        result = run(command, shell=True, cwd=cwd, check=True, text=True)
        return result.returncode == 0
    except CalledProcessError:
        return False

def setup_test_repo():
    """Создаёт тестовый Git-репозиторий с данными."""
    if TEST_REPO_PATH.exists():
        run_command(f"rm -rf {TEST_REPO_PATH}")
    TEST_REPO_PATH.mkdir()

    # Инициализация Git-репозитория
    run_command("git init", cwd=TEST_REPO_PATH)

    # Создание целевого файла и нескольких коммитов
    file_path = TEST_REPO_PATH / TARGET_FILE
    with open(file_path, "w") as f:
        f.write("Initial content")
    run_command("git add .", cwd=TEST_REPO_PATH)
    run_command('git commit -m "Initial commit"', cwd=TEST_REPO_PATH)

    with open(file_path, "a") as f:
        f.write("\nSecond change")
    run_command("git add .", cwd=TEST_REPO_PATH)
    run_command('git commit -m "Second commit"', cwd=TEST_REPO_PATH)

    with open(file_path, "a") as f:
        f.write("\nThird change")
    run_command("git add .", cwd=TEST_REPO_PATH)
    run_command('git commit -m "Third commit"', cwd=TEST_REPO_PATH)

def test_get_git_commits_with_file():
    """Тест для get_git_commits_with_file."""
    print("Running test_get_git_commits_with_file...")
    commits = get_git_commits_with_file(TEST_REPO_PATH, TARGET_FILE)
    assert len(commits) == 3, "Должно быть три коммита"
    print("✅ Passed")

def test_get_commit_files():
    """Тест для get_commit_files."""
    print("Running test_get_commit_files...")
    commits = get_git_commits_with_file(TEST_REPO_PATH, TARGET_FILE)
    first_commit_files = get_commit_files(TEST_REPO_PATH, commits[0])
    assert TARGET_FILE in first_commit_files, f"Файл {TARGET_FILE} должен быть в первом коммите"
    print("✅ Passed")

def test_build_mermaid_graph():
    """Тест для build_mermaid_graph."""
    print("Running test_build_mermaid_graph...")
    graph = build_mermaid_graph(TEST_REPO_PATH, TARGET_FILE)
    assert "graph TD" in graph, "Граф должен начинаться с 'graph TD'"
    assert len(graph.splitlines()) >= 4, "Граф должен содержать узлы и рёбра"
    print("✅ Passed")

def test_save_graph_to_file():
    """Тест для save_graph_to_file."""
    print("Running test_save_graph_to_file...")
    graph = "graph TD\nA --> B"
    save_graph_to_file(graph, OUTPUT_FILE)
    assert OUTPUT_FILE.exists(), "Файл с графом должен быть создан"
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert "A --> B" in content, "Файл должен содержать граф"
    print("✅ Passed")

def cleanup():
    """Удаляет временные файлы и директории, кроме output.mmd."""
    if TEST_REPO_PATH.exists():
        run_command(f"rm -rf {TEST_REPO_PATH}")
        print(f"Удалён временный тестовый репозиторий: {TEST_REPO_PATH}")
    if OUTPUT_FILE.exists():
        print(f"Файл графа сохранён и не будет удалён: {OUTPUT_FILE}")

def main():
    try:
        print("Setting up test repository...")
        setup_test_repo()
        print("Test repository set up.")

        # Запуск тестов
        test_get_git_commits_with_file()
        test_get_commit_files()
        test_build_mermaid_graph()
        test_save_graph_to_file()

        print("✅ Все тесты прошли успешно!")
    except AssertionError as e:
        print(f"❌ Ошибка теста: {e}")
    finally:
        print("Cleaning up...")
        cleanup()

if __name__ == "__main__":
    main()
