import subprocess
from pydantic.v1 import BaseModel
from langchain.tools import Tool
from states.state import AgentGraphState

def run_batch_script(state: AgentGraphState, script):
    try:
        script_content = script() if callable(script) else script
        script_content = script_content.content if hasattr(script_content, 'content') else script_content
        
        if not script_content:
            raise ValueError("Script content cannot be empty or None")
    
        
        if isinstance(script_content, dict) and 'batch_script' in script_content:
            script_content = script_content['batch_script']
        
        result = subprocess.run(script_content, shell=True, check=True, text=True, capture_output=True)
        state["batch_script_tool_response"].append(result.stdout)
        return {"batch_script_tool_response": state["batch_script_tool_response"]}
    except subprocess.CalledProcessError as err:
        error_message = f"Error occurred: {str(err)}"
        state["batch_script_tool_response"].append(error_message)
        return {"batch_script_tool_response": state["batch_script_tool_response"]}

class RunBatchScriptArgsSchema(BaseModel):
    script: str

run_batch_script_tool = Tool.from_function(
    name="run_batch_script",
    description="Run a batch script in the integrated terminal.",
    func=run_batch_script,
    args_schema=RunBatchScriptArgsSchema
)
