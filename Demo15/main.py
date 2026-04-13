import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

# New Import
from langchain_core.tools import tool

load_dotenv()

SYSTEM_PROMPT = """
You are the Simple Travel Helper Agent.

Your job is to answer travel-related questions by using the available tools. 
Always choose the right tool when the user asks about:
- popular destinations
- flight duration
- what to pack
- budget planning

TOOLS YOU CAN USE:
1. suggest_destinations(country: str)
   • Returns popular travel destinations in that country.

2. estimate_flight_time(origin: str, destination: str)
   • Returns approximate (mock) flight duration between two cities.

3. packing_list(days: int)
   • Suggests a packing checklist based on trip duration.

4. budget_estimate(destination: str, trip_type: str)
   • Returns an approximate budget range in INR (mock values).

General Rules:
- Use tools whenever the user asks for information provided by a tool.
- If the user’s question doesn’t require a tool, answer directly.
- Give friendly, helpful responses.
"""
# WHY DOCSTRING IS IMPORTANT

# @tool("destination")
# def suggest_destinations(country):
#     """Suggest places."""
#     data = {
#         "India": ["Goa", "Jaipur", "Kerala"],
#         "USA": ["New York", "LA", "Miami"],
#         "Japan": ["Tokyo", "Kyoto", "Osaka"]
#     }
#     return ", ".join(data.get(country.title(), ["No data"]))
@tool("destination_suggester")
def suggest_destinations(country: str) -> str:
    """
    Provide popular travel destinations for a given country.

    Use this tool whenever the user asks about:
    - places to visit
    - where to go
    - recommendations for cities or tourist spots
    
    The input should be the name of a country.
    """
    destinations = {
        "India": ["Goa", "Jaipur", "Kerala", "Manali", "Mumbai"],
        "USA": ["New York", "Los Angeles", "Miami", "San Francisco"],
        "Japan": ["Tokyo", "Kyoto", "Osaka", "Sapporo"],
        "France": ["Paris", "Nice", "Lyon", "Bordeaux"],
    }

    result = destinations.get(country.title(), ["No data available."])
    return ", ".join(result)



@tool("flight_duration")
def estimate_flight_time(origin: str, destination: str) -> str:
    """Give flight time."""
    times = {
        ("Delhi", "Paris"): "8h",
        ("Mumbai", "Dubai"): "3h",
        ("New York", "London"): "7h"
    }
    return times.get((origin.title(), destination.title()), "Unknown")

# WHY TYPEHINT IS IMPORTANT

@tool("packing_helper")
def packing_list(days: int) -> str:
    """
    Recommend a packing checklist based on the number of days.

    Use this tool ONLY when the user is asking about ITEMS to pack,
    not how much MONEY they need.
    """
    return (
        f"For a {days}-day trip, pack:\n"
        f"- {days} sets of clothes\n"
        f"- Toiletries\n"
        f"- Passport\n"
        f"- Chargers\n"
        f"- Essentials"
    )


@tool("total_spendings")
def budget_estimate(destination: str, trip_type: str) -> str:
    """Basic budget info."""
    amounts = {"budget": 2000, "standard": 5000, "luxury": 12000}
    amt = amounts.get(trip_type.lower(), 3000)
    return f"{destination}: {amt} INR/day"

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
memory = InMemorySaver()
thread = "travel1"

# Create a list of tools 
tools = [suggest_destinations, estimate_flight_time, packing_list, budget_estimate]

# Then pass that list as the value for tools param
agent = create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT, checkpointer=memory)

def main():
    print("TRAVEL AGENT")
    while True:
        q = input("You: ").strip()
        if q in ['exit','quit']: break
        result = agent.invoke(
            {"messages": [HumanMessage(content=q)]}, 
            {"configurable": {"thread_id": thread}}
        )
        print("Agent:", result["messages"][-1].content)

if __name__ == "__main__":
    main()