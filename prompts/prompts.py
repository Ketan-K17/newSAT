file_system_manager_prompt_template = """
You are a file system manager. Analyze the given file tree and decide on appropriate file management actions.
Generate a batch script to perform these actions.

File Tree:
{file_tree}

User Query:
{input_query}

Current date and time:
{datetime}

Your response must take the following json format:

    "analysis": "Your analysis of the file system and required actions"
    "script": "The batch script to perform the actions"

"""

file_system_manager_guided_json = {
    "type": "object",
    "properties": {
        "analysis": {
            "type": "string",
            "description": "Your analysis of the file system and required actions"
        },
        "script": {
            "type": "string",
            "description": "The batch script to perform the actions"
        }
    },
    "required": ["analysis", "script"]
}