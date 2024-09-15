import json
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from agents.agents import (
    FileSystemManagerAgent,
    FinalReportAgent,
    EndNodeAgent
)
from prompts.prompts import (
    file_system_manager_prompt_template,
    file_system_manager_guided_json,
)
from tools.get_file_tree import get_file_tree_tool
from tools.run_batch_script import run_batch_script_tool
from states.state import AgentGraphState, get_agent_graph_state, state

def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0):
    graph = StateGraph(AgentGraphState)

    graph.add_node("file_tree_tool", lambda state: {
        "file_tree_tool_response": [HumanMessage(content=get_file_tree_tool.invoke({"directory": state["input_directory"]}))]
    })

    graph.add_node(
        "file_system_manager", 
        lambda state: FileSystemManagerAgent(
            state=state,
            model=model,
            server=server,
            guided_json=file_system_manager_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            input_query=state["input_query"],
            file_tree=lambda: get_agent_graph_state(state=state, state_key="file_tree_tool_latest"),
            prompt=file_system_manager_prompt_template
        )
    )

    graph.add_node(
        "batch_script_tool",
        lambda state: {
            "batch_script_tool_response": [HumanMessage(content=run_batch_script_tool.invoke({
                "script": extract_script_from_response(get_agent_graph_state(state=state, state_key="file_system_manager_latest"))
            }))]
        }
    )

    graph.add_node(
        "final_report", 
        lambda state: FinalReportAgent(
            state=state
        ).invoke(
            script_result=lambda: get_agent_graph_state(state=state, state_key="batch_script_tool_latest")
        )
    )

    graph.add_node("end", lambda state: EndNodeAgent(state).invoke())

    # Add edges to the graph
    graph.set_entry_point("file_tree_tool")
    graph.set_finish_point("end")
    graph.add_edge("file_tree_tool", "file_system_manager")
    graph.add_edge("file_system_manager", "batch_script_tool")
    graph.add_edge("batch_script_tool", "final_report")
    graph.add_edge("final_report", "end")

    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    return workflow

def extract_script_from_response(response):
    if isinstance(response, list) and response:
        content = response[0].content
    elif hasattr(response, 'content'):
        content = response.content
    else:
        content = str(response)
    
    try:
        parsed = json.loads(content)
        return parsed.get("script", "echo No script found in response")
    except json.JSONDecodeError:
        return f"echo Error parsing response: {content[:100]}..."  # Return first 100 chars for debugging