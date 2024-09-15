from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentGraphState(TypedDict):
    input_query: str
    input_directory: str
    file_tree_tool_response: Annotated[list, add_messages]
    file_system_manager_response: Annotated[list, add_messages]
    batch_script_tool_response: Annotated[list, add_messages]
    reporter_response: Annotated[list, add_messages]
    reviewer_response: Annotated[list, add_messages]
    router_response: Annotated[list, add_messages]
    final_reports: Annotated[list, add_messages]
    end_chain: Annotated[list, add_messages]

def get_agent_graph_state(state: AgentGraphState, state_key: str):
    if state_key.endswith("_all"):
        return state[state_key[:-4] + "_response"]
    elif state_key.endswith("_latest"):
        key = state_key[:-7] + "_response"
        return state[key][-1] if state[key] else None
    else:
        return None

state = {
    "input_query": "",
    "input_directory": "",
    "file_tree_tool_response": [],
    "file_system_manager_response": [],
    "batch_script_tool_response": [],
    "reporter_response": [],
    "reviewer_response": [],
    "router_response": [],
    "final_reports": [],
    "end_chain": []
}