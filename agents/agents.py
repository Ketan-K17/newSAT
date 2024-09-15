import json
from termcolor import colored
from models.openai_models import get_open_ai, get_open_ai_json
from models.ollama_models import OllamaModel, OllamaJSONModel
from models.vllm_models import VllmJSONModel, VllmModel
from models.groq_models import GroqModel, GroqJSONModel
from models.claude_models import ClaudModel, ClaudJSONModel
from models.gemini_models import GeminiModel, GeminiJSONModel
from langchain_core.messages import HumanMessage
from prompts.prompts import (
    file_system_manager_prompt_template,
)
from utils.helper_functions import get_current_utc_datetime, check_for_content
from states.state import AgentGraphState

class Agent:
    def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0, model_endpoint=None, stop=None, guided_json=None):
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json

    def get_llm(self, json_model=True):
        if self.server == 'openai':
            return get_open_ai_json(model=self.model, temperature=self.temperature) if json_model else get_open_ai(model=self.model, temperature=self.temperature)
        if self.server == 'ollama':
            return OllamaJSONModel(model=self.model, temperature=self.temperature) if json_model else OllamaModel(model=self.model, temperature=self.temperature)
        if self.server == 'vllm':
            return VllmJSONModel(
                model=self.model, 
                guided_json=self.guided_json,
                stop=self.stop,
                model_endpoint=self.model_endpoint,
                temperature=self.temperature
            ) if json_model else VllmModel(
                model=self.model,
                model_endpoint=self.model_endpoint,
                stop=self.stop,
                temperature=self.temperature
            )
        if self.server == 'groq':
            return GroqJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else GroqModel(
                model=self.model,
                temperature=self.temperature
            )
        if self.server == 'claude':
            return ClaudJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else ClaudModel(
                model=self.model,
                temperature=self.temperature
            )
        if self.server == 'gemini':
            return GeminiJSONModel(
                model=self.model,
                temperature=self.temperature
            ) if json_model else GeminiModel(
                model=self.model,
                temperature=self.temperature
            )      

    def update_state(self, key, value):
        self.state = {**self.state, key: value}

class FileSystemManagerAgent(Agent):
    def invoke(self, input_query, file_tree, prompt=file_system_manager_prompt_template):
        try:
            if isinstance(file_tree(), list) and file_tree():
                file_tree_content = file_tree()[0].content
            elif hasattr(file_tree(), 'content'):
                file_tree_content = file_tree().content
            else:
                file_tree_content = str(file_tree())

            file_system_manager_prompt = prompt.format(
                input_query=input_query,
                file_tree=file_tree_content,
                datetime=get_current_utc_datetime()
            )

            messages = [
                {"role": "system", "content": file_system_manager_prompt},
                {"role": "user", "content": f"Manage files for query: {input_query}"}
            ]

            llm = self.get_llm()
            ai_msg = llm.invoke(messages)
            response = ai_msg.content

            print(colored(f"File System Manager 📁:", 'cyan'))
            print(colored(f"  Response: {response}", 'cyan'))
            
            return {"file_system_manager_response": [HumanMessage(content=response)]}
        except Exception as e:
            error_msg = f"Error in File System Manager: {str(e)}"
            print(colored(error_msg, 'red'))
            return {"file_system_manager_response": [HumanMessage(content=error_msg)]}

class FinalReportAgent(Agent):
    def invoke(self, script_result=None):
        script_result_value = script_result() if callable(script_result) else script_result
        script_result_value = check_for_content(script_result_value)
        
        response = f"File management task completed. Result: {script_result_value}"

        print(colored(f"Final Report 📝: {response}", 'green'))
        return {"final_reports": [HumanMessage(content=response)]}

class EndNodeAgent(Agent):
    def invoke(self):
        return {"end_chain": [HumanMessage(content="end_chain")]}