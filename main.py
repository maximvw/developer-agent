from langgraph.prebuilt import create_react_agent

from modules.utils.llm import llm
from modules.settings.developer_prompt import prompt
from modules.utils import tools
from modules.schemas import tools_schemas
from modules.utils.utils import run_chat, get_structured_tools, snake_to_pascal


tool2schema = {
    tools.write_file: tools_schemas.WriteFileSpec,
    tools.create_directory: tools_schemas.CreateDirectorySpec,
    tools.append_to_file: tools_schemas.AppendToFileSpec,
    tools.delete_file: tools_schemas.DeletePathSpec,
    tools.delete_directory: tools_schemas.DeletePathSpec,
    tools.read_file: tools_schemas.ReadFileSpec,
    tools.list_directory: tools_schemas.ListDirectorySpec,
    tools.list_directory_tree: tools_schemas.ListDirectorySpec,
    tools.rename_or_move: tools_schemas.RenameOrMoveSpec,
}

structured_tools = get_structured_tools(
    tools=tool2schema.keys(),
    names=[snake_to_pascal(tool.__name__) for tool in tool2schema.keys()],
    args_schemas=tool2schema.values(),
    descriptions=[tool.__doc__ for tool in tool2schema.keys()],
)

agent_executor = create_react_agent(model=llm, tools=structured_tools, prompt=prompt)


if __name__ == "__main__":
    run_chat(agent_executor)
