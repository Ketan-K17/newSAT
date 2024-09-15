from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# Define the state object for the agent graph
class AgentGraphState(TypedDict):
    user_query: str # prompt sent by user
    file_sys_path: str # path to the file system
    file_system_manager_response: Annotated[list, add_messages]
    file_tree_tool_response: Annotated[list, add_messages]
    run_batch_script_tool_response: Annotated[list, add_messages]

    selector_response: Annotated[list, add_messages]
    reporter_response: Annotated[list, add_messages]
    reviewer_response: Annotated[list, add_messages]
    router_response: Annotated[list, add_messages]
    final_reports: Annotated[list, add_messages]
    end_chain: Annotated[list, add_messages]

# Define the nodes in the agent graph
def get_agent_graph_state(state:AgentGraphState, state_key:str):
    if state_key == "file_system_manager_all":
        return state["file_system_manager_response"]
    elif state_key == "file_system_manager_latest":
        if state["file_system_manager_response"]:
            return state["file_system_manager_response"][-1]
        else:
            return state["file_system_manager_response"]
    
    
    elif state_key == "reporter_all":
        return state["reporter_response"]
    elif state_key == "reporter_latest":
        if state["reporter_response"]:
            return state["reporter_response"][-1]
        else:
            return state["reporter_response"]
    
    elif state_key == "reviewer_all":
        return state["reviewer_response"]
    elif state_key == "reviewer_latest":
        if state["reviewer_response"]:
            return state["reviewer_response"][-1]
        else:
            return state["reviewer_response"]
        
    elif state_key == "file_tree_tool_all":
        return state["file_tree_tool_response"]
    elif state_key == "file_tree_tool_latest":
        if state["file_tree_tool_response"]:
            return state["file_tree_tool_response"][-1]
        else:
            return state["file_tree_tool_response"]
    
    elif state_key == "batch_script_tool_all":
        return state["batch_script_tool_response"]
    elif state_key == "batch_script_tool_latest":
        if state["batch_script_tool_response"]:
            return state["batch_script_tool_response"][-1]
        else:
            return state["batch_script_tool_response"]
        
    else:
        return None
    
state = {
    "user_query":"",
    "file_sys_path":"c:\\Users\\ketan\\Desktop\\SPAIDER-SPACE\\graph_websearch_agent\\testfolder",
    "file_system_manager_response": [],
    "file_tree_tool_response": [],
    "batch_script_tool_response": [],
    "reporter_response": [],
    "reviewer_response": [],
    "router_response": [],
    "final_reports": [],
    "end_chain": []
}