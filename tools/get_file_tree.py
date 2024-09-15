from langchain.tools import Tool
from pydantic.v1 import BaseModel
from states.state import AgentGraphState
import subprocess
    
def get_file_tree(state: AgentGraphState, directory): 
    try:
        result = subprocess.run(f"tree {directory} /F", shell=True, check=True, text=True, capture_output=True)  
        state["file_tree_tool_response"].append(result.stdout)
        return {"file_tree_tool_response": state["file_tree_tool_response"]}
    except subprocess.CalledProcessError as err:
        error_message = f"Error occurred: {str(err)}"
        state["file_tree_tool_response"].append(error_message)
        return {"file_tree_tool_response": state["file_tree_tool_response"]}

class GetFileTreeArgsSchema(BaseModel):
    directory: str

get_file_tree_tool = Tool.from_function(
    name = "get_file_tree",
    description="Returns the file structure of the file system",
    func = get_file_tree,
    args_schema=GetFileTreeArgsSchema
)

