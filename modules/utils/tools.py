import os
import shutil

from modules.settings.agent_config import settings

REAL_WORKSPACE_PATH = os.path.realpath(settings.WORKSPACE_DIR)
os.makedirs(REAL_WORKSPACE_PATH, exist_ok=True)

def _get_safe_path(path: str) -> str:
    """
    "Страж": преобразует относительный путь в безопасный абсолютный путь внутри settings.WORKSPACE_DIR.
    Предотвращает выход за пределы песочницы (атаки типа Path Traversal).
    """
    absolute_path = os.path.join(REAL_WORKSPACE_PATH, path)

    real_path = os.path.realpath(absolute_path)
    
    if not real_path.startswith(REAL_WORKSPACE_PATH):
        raise ValueError(f"Попытка доступа за пределы рабочей директории ('{settings.WORKSPACE_DIR}') запрещена.")

    return real_path

def write_file(path: str, content: str) -> str:
    """Создает или полностью перезаписывает файл по пути path."""
    
    try:
        safe_path = _get_safe_path(path)
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Файл '{path}' успешно создан/перезаписан."
    except Exception as e:
        return f"Ошибка при записи файла: {e}"

def create_directory(path: str) -> str:
    """
        Создает новую директорию (папку) по указанному пути path.
        Создает все необходимые родительские директории.
    """
    try:
        safe_path = _get_safe_path(path)
        if os.path.exists(safe_path):
            return f"Информация: Директория '{path}' уже существует."
        os.makedirs(safe_path)
        return f"Директория '{path}' успешно создана."
    except Exception as e:
        return f"Ошибка при создании директории: {e}"


def append_to_file(path: str, content: str) -> str:
    """
        Добавляет содержимое в КОНЕЦ существующего файла по пути path.
        Не изменяет существующий контент.
    """
    try:
        safe_path = _get_safe_path(path)
        if not os.path.exists(safe_path):
            return f"Ошибка: Файл '{path}' не найден."
        with open(safe_path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Файл '{path}' успешно отредактирован."
    except Exception as e:
        return f"Ошибка при редактировании файла: {e}"


def delete_file(path: str) -> str:
    """Удаляет один файл по пути path."""
    try:
        safe_path = _get_safe_path(path)
        if os.path.isdir(safe_path):
            return f"Ошибка: '{path}' - это директория. Используйте DeleteDirectory."
        os.remove(safe_path)
        return f"Файл '{path}' успешно удален."
    except FileNotFoundError:
        return f"Ошибка: Файл '{path}' не найден."
    except Exception as e:
        return f"Ошибка при удалении файла: {e}"


def delete_directory(path: str) -> str:
    """Удаляет директорию по пути path и все ее содержимое."""
    try:
        safe_path = _get_safe_path(path)
        if not os.path.isdir(safe_path):
            return f"Ошибка: '{path}' - это файл. Используйте DeleteFile."
        shutil.rmtree(safe_path)
        return f"Директория '{path}' и ее содержимое удалены."
    except FileNotFoundError:
        return f"Ошибка: Директория '{path}' не найдена."
    except Exception as e:
        return f"Ошибка при удалении директории: {e}"


def read_file(path: str) -> str:
    """Читает содержимое файла по пути path."""
    try:
        safe_path = _get_safe_path(path)
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"Содержимое файла '{path}':\n\n{content}"
    except FileNotFoundError:
        return f"Ошибка: Файл '{path}' не найден."
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"


def list_directory(path: str = ".") -> str:
    """
        Показывает содержимое директории по пути path.
        Чтобы посмотреть корневую директорию, используйте параметр пустым.
    """
    try:
        safe_path = _get_safe_path(path)
        if not os.path.isdir(safe_path):
            return f"Ошибка: '{path}' не является директорией."
        entries = os.listdir(safe_path)
        if not entries:
            return f"Директория '{path}' пуста."
        output = f"Содержимое директории '{path}':\n" + "\n".join(f"- {'[D]' if os.path.isdir(os.path.join(safe_path, entry)) else '[F]'} {entry}" for entry in entries)
        return output
    except Exception as e:
        return f"Ошибка при просмотре директории: {e}"


def list_directory_tree(path: str = ".", prefix: str = "") -> str:
    """
        Показывает дерево директорий и файлов по пути path.
    """
    try:
        safe_path = _get_safe_path(path)  # ваша функция для безопасного пути
        if not os.path.isdir(safe_path):
            return f"Ошибка: '{path}' не является директорией."
        
        entries = sorted(os.listdir(safe_path))
        if not entries:
            return f"{prefix}[Пусто] {path}"
        
        lines = [f"{prefix}{os.path.basename(safe_path) or path}/"]
        for index, entry in enumerate(entries):
            full_path = os.path.join(safe_path, entry)
            connector = "└── " if index == len(entries) - 1 else "├── "
            if os.path.isdir(full_path):
                lines.append(f"{prefix}{connector}{entry}/")
                extension = "    " if index == len(entries) - 1 else "│   "
                lines.append(list_directory_tree(full_path, prefix + extension))
            else:
                lines.append(f"{prefix}{connector}{entry}")
        
        return "\n".join(lines)
    
    except Exception as e:
        return f"Ошибка при просмотре директории: {e}"


def rename_or_move(source_path: str, destination_path: str) -> str:
    """
        Переименовывает (или перемещает) файл или директорию 
        по пути path -> destination_path.
    """
    try:
        safe_source = _get_safe_path(source_path)
        safe_dest = _get_safe_path(destination_path)
        if not os.path.exists(safe_source):
            return f"Ошибка: Исходный путь '{source_path}' не найден."
        if os.path.exists(safe_dest):
            return f"Ошибка: Путь назначения '{destination_path}' уже существует."
        os.rename(safe_source, safe_dest)
        return f"Путь '{source_path}' успешно переименован в '{destination_path}'."
    except Exception as e:
        return f"Ошибка при переименовании: {e}"
