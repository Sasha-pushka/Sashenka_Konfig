import os
import subprocess
import argparse
from pathlib import Path

def get_git_commits_with_file(repo_path, file_name):
    """
    Получить список коммитов, где изменялся указанный файл.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--pretty=format:%H", "--", file_name],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения git: {e}")
        return []

def get_commit_files(repo_path, commit_hash):
    """
    Получить список файлов и папок, измененных в указанном коммите.
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "show", "--pretty=format:", "--name-only", commit_hash],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        files = result.stdout.splitlines()
        return [file for file in files if file.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения git: {e}")
        return []

def build_mermaid_graph(repo_path, file_name):
    """
    Построить граф зависимостей в формате Mermaid.
    """
    commits = get_git_commits_with_file(repo_path, file_name)
    if not commits:
        return "Граф зависимостей пуст или файл не найден."

    graph = ["graph TD"]
    previous_commit = None

    for commit in commits:
        files = get_commit_files(repo_path, commit)
        node_label = f"{commit[:7]}: {'<br>'.join(files)}"
        graph.append(f"{commit[:7]}[\"{node_label}\"]")
        if previous_commit:
            graph.append(f"{previous_commit[:7]} --> {commit[:7]}")
        previous_commit = commit

    return "\n".join(graph)

def save_graph_to_file(graph, output_path):
    """
    Сохранить граф в файл.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(graph)
    except IOError as e:
        print(f"Ошибка сохранения графа: {e}")

def main():
    parser = argparse.ArgumentParser(description="Визуализация графа зависимостей для git-репозитория.")
    parser.add_argument("--repo-path", required=True, help="Путь к анализируемому репозиторию.")
    parser.add_argument("--file-name", required=True, help="Имя файла для анализа зависимостей.")
    parser.add_argument("--output-path", required=True, help="Путь к файлу-результату в формате Mermaid.")
    
    args = parser.parse_args()

    repo_path = Path(args.repo_path).resolve()
    file_name = args.file_name
    output_path = Path(args.output_path).resolve()

    if not repo_path.is_dir():
        print(f"Указанный путь к репозиторию не найден: {repo_path}")
        return

    graph = build_mermaid_graph(repo_path, file_name)
    save_graph_to_file(graph, output_path)
    print(f"Граф зависимостей сохранён в {output_path}.")

if __name__ == "__main__":
    main()
