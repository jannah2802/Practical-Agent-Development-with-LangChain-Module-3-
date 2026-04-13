import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

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

def suggest_destinations(country):
    """Return 3–5 well-known travel destinations for the given country."""
    destinations = {
        "India": ["Goa", "Jaipur", "Kerala", "Manali", "Mumbai"],
        "USA": ["New York", "Los Angeles", "San Francisco", "Miami"],
        "Japan": ["Tokyo", "Kyoto", "Osaka", "Sapporo"],
        "France": ["Paris", "Nice", "Lyon", "Bordeaux"],
    }
    result = destinations.get(country.title(), ["No data available. Try another country."])
    return ", ".join(result)

def estimate_flight_time(origin: str, destination: str):
    """Return a rough mock flight duration between two major cities."""
    mock_times = {
        ("Delhi", "Paris"): "8h 30m",
        ("Mumbai", "Dubai"): "3h 15m",
        ("Bangalore", "Singapore"): "4h 45m",
        ("New York", "London"): "7h 00m",
    }
    key = (origin.title(), destination.title())
    duration = mock_times.get(key, "Approx. 3–10 hours depending on distance.")
    return f"Estimated flight time from {origin} to {destination}: {duration}"

def packing_list(days):
    """Recommend a practical packing list for a trip of the given duration."""
    base_items = ["Passport", "Phone + Charger", "Travel-size toiletries", "Light jacket"]
    clothing = [f"{days} sets of comfortable clothes", f"{days//2} pairs of socks"]
    extras = ["Reusable water bottle", "Power adapter", "Medications"]

    items = base_items + clothing + extras
    return "Recommended packing list:\n- " + "\n- ".join(items)

def budget_estimate(destination, trip_type):
    """Return an estimated daily travel budget in INR based on trip type."""
    base_budgets = {
        "budget": 2500,
        "standard": 5000,
        "luxury": 12000,
    }

    amount = base_budgets.get(trip_type.lower(), 4000)
    return f"Estimated daily budget for {destination} ({trip_type} trip): ₹{amount} per day"

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
memory = InMemorySaver()
thread = "travel1"

tools = [suggest_destinations, estimate_flight_time, packing_list, budget_estimate]
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