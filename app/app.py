from agent_graph.graph import create_graph, compile_workflow
import os
import traceback

server = 'groq'
model = 'llama3-groq-70b-8192-tool-use-preview'
model_endpoint = None

# server = 'ollama'
# model = 'llama3:instruct'
# model_endpoint = None

# server = 'openai'
# model = 'gpt-4o'
# model_endpoint = None

# server = 'vllm'
# model = 'meta-llama/Meta-Llama-3-70B-Instruct' # full HF path
# model_endpoint = 'https://kcpqoqtjz0ufjw-8000.proxy.runpod.net/' 
# #model_endpoint = runpod_endpoint + 'v1/chat/completions'
# stop = "<|end_of_text|>"


iterations = 40

print("Creating graph and compiling workflow...")
graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)
workflow = compile_workflow(graph)
print("Graph and workflow created.")

if __name__ == "__main__":
    verbose = False # Set to True for debugging

    while True:
        query = input("Please enter your file management query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break

        directory = input("Please enter the directory to manage: ")
        
        if not os.path.isdir(directory):
            print(f"Error: '{directory}' is not a valid directory. Please try again.")
            continue

        dict_inputs = {
            "input_query": query,
            "input_directory": directory
        }
        limit = {"recursion_limit": iterations}

        print(f"\nProcessing query: '{query}' for directory: '{directory}'")
        print("File management task in progress. This may take a moment...")

        try:
            for event in workflow.stream(dict_inputs, limit):
                if verbose:
                    print("\nState Dictionary:", event)
                else:
                    print(".", end="", flush=True)  # Progress indicator
            
            print("\n\nFile management task completed.")
            
            # Display final report
            final_report = event.get("final_reports", ["No final report generated."])[-1]
            print("\nFinal Report:")
            print(final_report)
        
        except Exception as e:
            print(f"\nAn error occurred during the file management task:")
            print(traceback.format_exc())  # This will print the full stack trace

        print("\nEnter a new query or type 'exit' to quit.")