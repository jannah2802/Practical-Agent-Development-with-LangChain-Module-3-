# Guide for Demo15: Creating Tools with @tool

Till now we have been easily working with the tools that are basically python fuctions. 
We can use @tool decorator to turn a normal Python function into a well-defined tool object.
Adding a @tool decorator automatically extracts:
- the function name
- the type hints → input schema
- the docstring → tool description

## New Import 
To use the tool decorator you need to have the proper module imported.
**from langchain_core.tools import tool**

## How to Declare a tool using @tool
Just before the function def add the @tool decorator.... This way th eLLM will automatically treat this function as tool without you telling it to. 

## TypeHints
"How much should I pack for Tokyo?"
pack could mean anything (money or packing list) which will make LLM confused. This is where TypeHints help.

Every tool has parameters. The model must know:
- how many inputs a tool needs
- what types they are

1. **days:int** - forces the model to extract a number from the user query.To the packing_list function we gave the typehint as int so that the model is forced to extract number from the query
2. **-> str** - This makes sure that the tool always returns a string. This makes sure the agent knows how to handle the output properly.


## DocString
A docstring is not for humans alone, it is sent to the LLM as the tool description. It is important that it is descriptive...


## Adding Custom names
You can also add custom names by adding the namein bracket just after @tool

## Passing tools to create_agent Framework

Only the tools you pass to the model become available to the LLM. Once you pass the tools LLM will know:
- What each tool does (from docstring)
- What input each tool expects (from type hints)
- When to use each tool (from the system prompt + docstrings)

## How the Agent Chooses Which Tool to Use
The agent uses a reasoning process:
1. Reads the user's question
2. Checks descriptions of all tools
3. Decides which tool matches the intention
4. Calls that tool
5. Returns the tool’s output to the user

## Why Better Tool Descriptions Improve Results

If a tool’s docstring is vague, the LLM might:
- call the wrong tool
- avoid calling a tool at all
- ask the user again

**For Example:**  take “Tell me something about travel options for France.” for example..... Ideally this should output the destinations you can take... Instead it is saying "Agent: I am sorry, I do not have any travel options for France."
*After better docstring*: Agent: France is a beautiful country with many travel options. Popular destinations include Paris, Nice, Lyon, and Bordeaux. Each city offers a unique experience, from historical landmarks to culinary delights.
