from typing import List
from langchain_core.tools import StructuredTool
from langchain_core.messages import HumanMessage, BaseMessage

from modules.settings.agent_config import settings


def snake_to_pascal(name: str) -> str:
    return ''.join(word.capitalize() for word in name.split('_'))


def get_structured_tools(tools, names, args_schemas, descriptions) -> List[StructuredTool]:
    """Возвращает список инструментов StructuredTool."""

    if not (len(tools) == len(names) == len(args_schemas) == len(descriptions)):
        raise ValueError("Длины списков tools, names, args_schemas и descriptions должны быть одинаковыми.")
    
    structured_tools = []
    for func, name, schema, descr in zip(tools, names, args_schemas, descriptions):
        structured_tool = StructuredTool.from_function(func=func, name=name, args_schema=schema, description=descr)
        structured_tools.append(structured_tool)   

    return structured_tools


def manage_context(messages: List[BaseMessage], content_window_size: int) -> List[BaseMessage]:
    """Управляет размером контекста, сохраняя системное сообщение и последние K сообщений."""
    if len(messages) <= content_window_size:
        return messages

    system_message = messages[0]
    recent_messages = messages[-content_window_size:]

    trimmed_messages = [system_message] + recent_messages
    print(f"\n[DEBUG: Контекст был урезан. Сохранено {len(trimmed_messages)} из {len(messages)} сообщений.]\n")
    return trimmed_messages


def run_chat(agent_executor):
    messages_history: List[BaseMessage] = []
    print(f"Агент-программист готов к работе. Все проекты будут созданы в директории '{settings.WORKSPACE_DIR}'. Введите 'выход', чтобы завершить.")

    while True:
        user_input = input("Вы: ")

        if user_input.lower() == 'restart':
            messages_history = []
            print("Контекст чата был сброшен.")
            continue

        if user_input.lower() in ['выход', 'exit']:
            print("Агент завершает работу. До свидания!")
            break

        messages_history.append(HumanMessage(content=user_input))

        messages_to_send = manage_context(messages_history, settings.CONTEXT_WINDOW_SIZE)

        response = agent_executor.invoke({"messages": messages_to_send})
        agent_response = response['messages'][-1]
        messages_history.append(agent_response)

        agent_response.pretty_print()