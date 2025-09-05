import os
import shutil


def write_file(path: str, content: str) -> str:
    """Создает или полностью перезаписывает файл."""
    try:
        safe_path = path
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Файл '{path}' успешно создан/перезаписан в workspace."
    except Exception as e:
        return f"Ошибка при записи файла: {e}"

def create_directory(path: str) -> str:
    """Создает новую директорию (папку) по указанному пути.
       Создает все необходимые родительские директории."""
    try:
        safe_path = path
        if os.path.exists(safe_path):
            return f"Информация: Директория '{path}' уже существует в workspace."
        os.makedirs(safe_path)
        return f"Директория '{path}' успешно создана в workspace."
    except Exception as e:
        return f"Ошибка при создании директории: {e}"


def append_to_file(path: str, content: str) -> str:
    """Добавляет содержимое в КОНЕЦ существующего файла.
       Не изменяет существующий контент."""
    try:
        safe_path = path
        if not os.path.exists(safe_path):
            return f"Ошибка: Файл '{path}' не найден в workspace."
        with open(safe_path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Файл '{path}' успешно отредактирован в workspace."
    except Exception as e:
        return f"Ошибка при редактировании файла: {e}"


def delete_file(path: str) -> str:
    """Удаляет один файл."""
    try:
        safe_path = path
        if os.path.isdir(safe_path):
            return f"Ошибка: '{path}' - это директория. Используйте DeleteDirectory."
        os.remove(safe_path)
        return f"Файл '{path}' успешно удален из workspace."
    except FileNotFoundError:
        return f"Ошибка: Файл '{path}' не найден в workspace."
    except Exception as e:
        return f"Ошибка при удалении файла: {e}"

def delete_directory(path: str) -> str:
    """Удаляет директорию и все ее содержимое."""
    try:
        safe_path = path
        if not os.path.isdir(safe_path):
            return f"Ошибка: '{path}' - это файл. Используйте DeleteFile."
        shutil.rmtree(safe_path)
        return f"Директория '{path}' и ее содержимое удалены из workspace."
    except FileNotFoundError:
        return f"Ошибка: Директория '{path}' не найдена в workspace."
    except Exception as e:
        return f"Ошибка при удалении директории: {e}"


def read_file(path: str) -> str:
    """Читает содержимое файла."""
    try:
        safe_path = path
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"Содержимое файла '{path}':\n\n{content}"
    except FileNotFoundError:
        return f"Ошибка: Файл '{path}' не найден в workspace."
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"


def list_directory(path: str = ".") -> str:
    """Показывает содержимое директории."""
    try:
        safe_path = path
        if not os.path.isdir(safe_path):
            return f"Ошибка: '{path}' не является директорией."
        entries = os.listdir(safe_path)
        if not entries:
            return f"Директория '{path}' в workspace пуста."
        output = f"Содержимое директории '{path}' в workspace:\n" + "\n".join(f"- {'[D]' if os.path.isdir(os.path.join(safe_path, entry)) else '[F]'} {entry}" for entry in entries)
        return output
    except Exception as e:
        return f"Ошибка при просмотре директории: {e}"


def rename_or_move(source_path: str, destination_path: str) -> str:
    """Переименовывает (или перемещает) файл или директорию."""
    try:
        safe_source = source_path
        safe_dest = destination_path
        if not os.path.exists(safe_source):
            return f"Ошибка: Исходный путь '{source_path}' не найден в workspace."
        if os.path.exists(safe_dest):
            return f"Ошибка: Путь назначения '{destination_path}' уже существует в workspace."
        os.rename(safe_source, safe_dest)
        return f"Путь '{source_path}' успешно переименован в '{destination_path}' в workspace."
    except Exception as e:
        return f"Ошибка при переименовании: {e}"


# import os
# import shutil

# from modules.utils.utils import _get_safe_path


# def write_file(path: str, content: str) -> str:
#     """Создает или полностью перезаписывает файл."""
#     try:
#         safe_path = _get_safe_path(path)
#         os.makedirs(os.path.dirname(safe_path), exist_ok=True)
#         with open(safe_path, "w", encoding="utf-8") as f:
#             f.write(content)
#         return f"Файл '{path}' успешно создан/перезаписан в workspace."
#     except Exception as e:
#         return f"Ошибка при записи файла: {e}"

# def create_directory(path: str) -> str:
#     """Создает новую директорию (папку) по указанному пути.
#        Создает все необходимые родительские директории."""
#     try:
#         safe_path = _get_safe_path(path)
#         if os.path.exists(safe_path):
#             return f"Информация: Директория '{path}' уже существует в workspace."
#         os.makedirs(safe_path)
#         return f"Директория '{path}' успешно создана в workspace."
#     except Exception as e:
#         return f"Ошибка при создании директории: {e}"


# def append_to_file(path: str, content: str) -> str:
#     """Добавляет содержимое в КОНЕЦ существующего файла.
#        Не изменяет существующий контент."""
#     try:
#         safe_path = _get_safe_path(path)
#         if not os.path.exists(safe_path):
#             return f"Ошибка: Файл '{path}' не найден в workspace."
#         with open(safe_path, "a", encoding="utf-8") as f:
#             f.write(content)
#         return f"Файл '{path}' успешно отредактирован в workspace."
#     except Exception as e:
#         return f"Ошибка при редактировании файла: {e}"


# def delete_file(path: str) -> str:
#     """Удаляет один файл."""
#     try:
#         safe_path = _get_safe_path(path)
#         if os.path.isdir(safe_path):
#             return f"Ошибка: '{path}' - это директория. Используйте DeleteDirectory."
#         os.remove(safe_path)
#         return f"Файл '{path}' успешно удален из workspace."
#     except FileNotFoundError:
#         return f"Ошибка: Файл '{path}' не найден в workspace."
#     except Exception as e:
#         return f"Ошибка при удалении файла: {e}"

# def delete_directory(path: str) -> str:
#     """Удаляет директорию и все ее содержимое."""
#     try:
#         safe_path = _get_safe_path(path)
#         if not os.path.isdir(safe_path):
#             return f"Ошибка: '{path}' - это файл. Используйте DeleteFile."
#         shutil.rmtree(safe_path)
#         return f"Директория '{path}' и ее содержимое удалены из workspace."
#     except FileNotFoundError:
#         return f"Ошибка: Директория '{path}' не найдена в workspace."
#     except Exception as e:
#         return f"Ошибка при удалении директории: {e}"


# def read_file(path: str) -> str:
#     """Читает содержимое файла."""
#     try:
#         safe_path = _get_safe_path(path)
#         with open(safe_path, "r", encoding="utf-8") as f:
#             content = f.read()
#         return f"Содержимое файла '{path}':\n\n{content}"
#     except FileNotFoundError:
#         return f"Ошибка: Файл '{path}' не найден в workspace."
#     except Exception as e:
#         return f"Ошибка при чтении файла: {e}"


# def list_directory(path: str = ".") -> str:
#     """Показывает содержимое директории."""
#     try:
#         safe_path = _get_safe_path(path)
#         if not os.path.isdir(safe_path):
#             return f"Ошибка: '{path}' не является директорией."
#         entries = os.listdir(safe_path)
#         if not entries:
#             return f"Директория '{path}' в workspace пуста."
#         output = f"Содержимое директории '{path}' в workspace:\n" + "\n".join(f"- {'[D]' if os.path.isdir(os.path.join(safe_path, entry)) else '[F]'} {entry}" for entry in entries)
#         return output
#     except Exception as e:
#         return f"Ошибка при просмотре директории: {e}"


# def rename_or_move(source_path: str, destination_path: str) -> str:
#     """Переименовывает (или перемещает) файл или директорию."""
#     try:
#         safe_source = _get_safe_path(source_path)
#         safe_dest = _get_safe_path(destination_path)
#         if not os.path.exists(safe_source):
#             return f"Ошибка: Исходный путь '{source_path}' не найден в workspace."
#         if os.path.exists(safe_dest):
#             return f"Ошибка: Путь назначения '{destination_path}' уже существует в workspace."
#         os.rename(safe_source, safe_dest)
#         return f"Путь '{source_path}' успешно переименован в '{destination_path}' в workspace."
#     except Exception as e:
#         return f"Ошибка при переименовании: {e}"





# # write_file_tool = StructuredTool.from_function(func=write_file, name="WriteFile",  args_schema=WriteFileSpec)


# # create_directory_tool = StructuredTool.from_function(func=create_directory, name="CreateDirectory", args_schema=CreateDirectorySpec)

# # append_to_file_tool = StructuredTool.from_function(func=append_to_file, name="AppendToFile", args_schema=FileAppendSpec)

# # delete_file_tool = StructuredTool.from_function(func=delete_file, name="DeleteFile", args_schema=DeletePathSpec)

# # delete_directory_tool = StructuredTool.from_function(func=delete_directory, name="DeleteDirectory", args_schema=DeletePathSpec)
# # read_file_tool = StructuredTool.from_function(func=read_file, name="ReadFile", args_schema=ReadFileSpec)
# # list_directory_tool = StructuredTool.from_function(func=list_directory, name="ListDirectory", args_schema=ListDirectorySpec)
# # rename_or_move_tool = StructuredTool.from_function(func=rename_or_move, name="RenameOrMove", args_schema=RenameOrMoveSpec)

# # tools_list = [
# #     write_file_tool, create_directory_tool, append_to_file_tool, delete_file_tool, 
# #     delete_directory_tool, read_file_tool, list_directory_tool, rename_or_move_tool
# # ]