# import libraries
from typing import Annotated, NamedTuple
from fastmcp import FastMCP
from todo_db import TodoDB

# Load the database
todo_db = TodoDB()
# todo_db.sample_data()

# Create the MCP server
mcp = FastMCP("TODO MCP")

# class todo
class Todo(NamedTuple):
    filename:Annotated[str, "source file containing the #TODO"] 
    lineNumber:Annotated[int, "Line number to add the #TODO"]
    text:Annotated[str, "Description of the #TODO"] 

# tools
@mcp.tool(
    name="tool_addtodos",
    description="Add mulitple todos from a list of todos"
)

def add_todo(todos: list[Todo]) -> int:
    for todo in todos:
        todo_db.add(filename=todo[0], line_num=todo[1], text=todo[2])
    return len(todos)

@mcp.tool(
    name="tool_addtodo",
    description="Add a single #TODO text from a source file"
)

def add_todo(filename:Annotated[str, "source file containing the #TODO"], 
    lineNumber:Annotated[int, "Line number to add the #TODO"],
    text:Annotated[str, "Description of the #TODO"]):
    return todo_db.add(filename=filename, line_num=lineNumber, text=text)

# resources
# uri is required in a resource
@mcp.resource(
    name="resource_todos",
    description="returns a list of todos or an empty array if there is no todo present",
    uri="todo://{filename}/todos"
)
def get_todos_for_file(
        filename: Annotated[str, "Source file containing #TODO"]):
    todos = todo_db.get(filename=filename)
    return [ text for text in todos.values()]


# Start the MCP
def main():
    mcp.run()

if __name__ == "__main__":
    main()