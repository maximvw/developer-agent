from langgraph.prebuilt import create_react_agent

from modules.settings.developer_prompt import prompt
from modules.utils.utils import run_chat, get_structured_tools, snake_to_pascal, with_safe_path
from modules.utils.tools import *
from modules.schemas.tools_schemas import *
from modules.utils.llm import llm


tool2schema = {
    write_file: WriteFileSpec,
    create_directory: CreateDirectorySpec,
    append_to_file: AppendToFileSpec,
    delete_file: DeletePathSpec,
    delete_directory: DeletePathSpec,
    read_file: ReadFileSpec,
    list_directory: ListDirectorySpec,
    rename_or_move: RenameOrMoveSpec
}
tool2schema = {with_safe_path()(tool): schema for tool, schema in tool2schema.items()}

structured_tools = get_structured_tools(
    tools=tool2schema.keys(),
    names=[snake_to_pascal(tool.__name__) for tool in tool2schema.keys()],
    args_schemas=tool2schema.values(),
    descriptions=[tool.__doc__ for tool in tool2schema.keys()]
    )

agent_executor = create_react_agent(llm, structured_tools, prompt=prompt)


if __name__ == "__main__":
    run_chat(agent_executor)