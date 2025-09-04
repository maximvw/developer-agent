import os
import shutil
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import StructuredTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, BaseMessage

# Загружаем переменные окружения
load_dotenv()


class FileWriteSpec(BaseModel):
    path: str = Field(..., description="Путь к файлу, который нужно создать или перезаписать.")
    content: str = Field(..., description="Содержимое, которое нужно записать в файл.")

def write_file(path: str, content: str) -> str:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Файл '{path}' успешно создан/перезаписан."
    except Exception as e:
        return f"Ошибка при записи файла '{path}': {e}"

class FileEditSpec(BaseModel):
    path: str = Field(..., description="Путь к файлу, который нужно отредактировать.")
    content: str = Field(..., description="Новое содержимое, которое будет добавлено в конец файла.")

def edit_file(path: str, content: str) -> str:
    try:
        if not os.path.exists(path):
            return f"Ошибка: Файл '{path}' не найден. Используйте инструмент write_file для его создания."
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Файл '{path}' успешно отредактирован."
    except Exception as e:
        return f"Ошибка при редактировании файла '{path}': {e}"

class DeletePathSpec(BaseModel):
    path: str = Field(..., description="Путь к файлу или директории, которую нужно удалить.")

def delete_file(path: str) -> str:
    try:
        if os.path.isdir(path):
            return f"Ошибка: '{path}' - это директория. Используйте инструмент DeleteDirectory."
        os.remove(path)
        return f"Файл '{path}' успешно удален."
    except FileNotFoundError:
        return f"Ошибка: Файл '{path}' не найден."
    except Exception as e:
        return f"Ошибка при удалении файла '{path}': {e}"

def delete_directory(path: str) -> str:
    try:
        if not os.path.isdir(path):
            return f"Ошибка: '{path}' - это файл. Используйте инструмент DeleteFile."
        shutil.rmtree(path)
        return f"Директория '{path}' и все ее содержимое успешно удалены."
    except FileNotFoundError:
        return f"Ошибка: Директория '{path}' не найдена."
    except Exception as e:
        return f"Ошибка при удалении директории '{path}': {e}"


class ReadFileSpec(BaseModel):
    path: str = Field(..., description="Путь к файлу, который нужно прочитать.")

def read_file(path: str) -> str:
    """Читает и возвращает содержимое файла по указанному пути."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"Содержимое файла '{path}':\n\n{content}"
    except FileNotFoundError:
        return f"Ошибка: Файл '{path}' не найден."
    except Exception as e:
        return f"Ошибка при чтении файла '{path}': {e}"

class ListDirectorySpec(BaseModel):
    path: Optional[str] = Field(default=".", description="Путь к директории, содержимое которой нужно посмотреть. По умолчанию - текущая директория.")

def list_directory(path: str = ".") -> str:
    """Возвращает список файлов и поддиректорий по указанному пути."""
    try:
        if not os.path.isdir(path):
            return f"Ошибка: '{path}' не является директорией."
        
        entries = os.listdir(path)
        if not entries:
            return f"Директория '{path}' пуста."
        
        output = f"Содержимое директории '{path}':\n"
        for entry in entries:
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                output += f"- [D] {entry}\n"
            else:
                output += f"- [F] {entry}\n"
        return output
    except FileNotFoundError:
        return f"Ошибка: Директория '{path}' не найдена."
    except Exception as e:
        return f"Ошибка при просмотре директории '{path}': {e}"

class RenameSpec(BaseModel):
    """Спецификация для переименования файла или директории."""
    source_path: str = Field(..., description="Текущий путь к файлу или директории.")
    destination_path: str = Field(..., description="Новый путь к файлу или директории.")

def rename_path(source_path: str, destination_path: str) -> str:
    """Переименовывает файл или директорию."""
    try:
        if not os.path.exists(source_path):
            return f"Ошибка: Исходный путь '{source_path}' не найден."
        if os.path.exists(destination_path):
            return f"Ошибка: Путь назначения '{destination_path}' уже существует."
        os.rename(source_path, destination_path)
        return f"Путь '{source_path}' успешно переименован в '{destination_path}'."
    except Exception as e:
        return f"Ошибка при переименовании '{source_path}': {e}"



write_file_tool = StructuredTool.from_function(func=write_file, name="WriteFile", description="Создает или полностью перезаписывает файл.", args_schema=FileWriteSpec)
edit_file_tool = StructuredTool.from_function(func=edit_file, name="EditFile", description="Редактирует существующий файл, добавляя новое содержимое в конец.", args_schema=FileEditSpec)
delete_file_tool = StructuredTool.from_function(func=delete_file, name="DeleteFile", description="Удаляет один файл.", args_schema=DeletePathSpec)
delete_directory_tool = StructuredTool.from_function(func=delete_directory, name="DeleteDirectory", description="Удаляет директорию и все ее содержимое.", args_schema=DeletePathSpec)
read_file_tool = StructuredTool.from_function(func=read_file, name="ReadFile", description="Читает содержимое файла.", args_schema=ReadFileSpec)
list_directory_tool = StructuredTool.from_function(func=list_directory, name="ListDirectory", description="Показывает содержимое директории.", args_schema=ListDirectorySpec)
rename_path_tool = StructuredTool.from_function(func=rename_path, name="RenamePath", description="Переименовывает файл или директорию.", args_schema=RenameSpec)

tools = [
    write_file_tool, edit_file_tool, delete_file_tool, 
    delete_directory_tool, read_file_tool, list_directory_tool,
    rename_path_tool
]


system_prompt_template_text = """Ты — автономный агент-программист. Твоя задача — помогать пользователю в создании, редактировании и управлении проектами.

Тебе доступны следующие инструменты:
- ListDirectory: Показывает содержимое директории.
- ReadFile: Читает содержимое файла.
- WriteFile: Создает или полностью перезаписывает файл.
- EditFile: Добавляет новый контент в конец существующего файла.
- DeleteFile: Удаляет один конкретный файл.
- DeleteDirectory: Удаляет целую директорию со всем ее содержимым.
- RenamePath: Переименовывает файл или директорию.


Стратегия работы:
1.  Исследуй. Прежде чем вносить какие-либо изменения, всегда изучай текущую структуру проекта. Используй `ListDirectory`, чтобы увидеть файлы и папки.
2.  Анализируй. Прежде чем редактировать файл, всегда читай его содержимое с помощью `ReadFile`. Это поможет тебе понять контекст и избежать ошибок.
3.  Действуй. После анализа используй `WriteFile`, `EditFile`, `RenamePath`, `DeleteFile` или `DeleteDirectory` для выполнения запроса пользователя.
4.  Сообщай. После выполнения операции всегда сообщай пользователю, что именно ты сделал.

Всегда создавай файлы в папке с названием проекта, которое ты должен придумать из контекста задачи, если пользователь не указал иное.
Внимательно читай запрос пользователя. Если он просит "отредактировать" или "добавить" в файл, используй EditFile. Если просит "создать" или "записать", используй WriteFile.
Если нужно переименовать файл или папку, используй RenamePath.
Если нужно удалить папку, используй DeleteDirectory. Если нужно удалить файл - DeleteFile.
Если нужно посмотреть содержимое папки - ListDirectory. Если нужно посмотреть содержимое файла - ReadFile.

Начинай работу. Если ты можешь ответить сразу без инструментов, сделай это.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_template_text),
        ("placeholder", "{messages}"),
    ]
)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, max_tokens=4096, transport="rest")
agent_executor = create_react_agent(llm, tools, prompt=prompt)


CONTEXT_WINDOW_SIZE = 50

def manage_context(messages: List[BaseMessage]) -> List[BaseMessage]:
    """Управляет размером контекста, сохраняя системное сообщение и последние K сообщений."""
    if len(messages) <= CONTEXT_WINDOW_SIZE:
        return messages

    system_message = messages[0]
    recent_messages = messages[-CONTEXT_WINDOW_SIZE:]

    trimmed_messages = [system_message] + recent_messages
    print(f"\n[DEBUG: Контекст был урезан. Сохранено {len(trimmed_messages)} из {len(messages)} сообщений.]\n")
    return trimmed_messages


def run_chat():
    messages_history: List[BaseMessage] = []
    print("Агент-программист готов к работе. Введите 'выход', чтобы завершить.")

    while True:
        user_input = input("Вы: ")
        if user_input.lower() == 'выход':
            print("Агент завершает работу. До свидания!")
            break

        messages_history.append(HumanMessage(content=user_input))

        messages_to_send = manage_context(messages_history)

        response = agent_executor.invoke({"messages": messages_to_send})
        agent_response = response['messages'][-1]
        messages_history.append(agent_response)

        # print(f"Агент: {agent_response.content}")
        agent_response.pretty_print()

if __name__ == "__main__":
    run_chat()