import os
import platform
from langchain.tools import Tool
from pydantic.v1 import BaseModel

def get_file_tree(directory):
    def tree(dir_path, level=0, is_last=False, prefix=""):
        output = []
        entries = sorted(os.scandir(dir_path), key=lambda e: e.name.lower())
        entries = list(entries)
        for i, entry in enumerate(entries):
            is_last_entry = i == len(entries) - 1
            marker = "└── " if is_last_entry else "├── "
            output.append(f"{prefix}{marker}{entry.name}")
            if entry.is_dir():
                extension = "    " if is_last_entry else "│   "
                output.extend(tree(entry.path, level + 1, is_last_entry, prefix + extension))
        return output

    try:
        if not os.path.isdir(directory):
            return f"Error: {directory} is not a valid directory."
        
        result = "\n".join(tree(directory))
        return result
    except Exception as e:
        return f"Error occurred: {str(e)}"

class GetFileTreeArgsSchema(BaseModel):
    directory: str

get_file_tree_tool = Tool.from_function(
    name="get_file_tree",
    description="Returns the file structure of the specified directory",
    func=get_file_tree,
    args_schema=GetFileTreeArgsSchema
)