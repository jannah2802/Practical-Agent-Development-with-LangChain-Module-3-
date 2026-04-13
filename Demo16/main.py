import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import tool

# New Import
import requests


load_dotenv()

# Update System Prompt
SYSTEM_PROMPT = """
You are the Simple Travel Helper Agent.

Your job is to answer travel-related questions by using the available tools. 
Always choose the right tool when the user asks about:
- popular destinations
- flight duration
- what to pack
- budget planning
- weather information (using live_weather tool)

TOOLS YOU CAN USE:
1. suggest_destinations(country: str)
   • Returns popular travel destinations in that country.

2. estimate_flight_time(origin: str, destination: str)
   • Returns approximate (mock) flight duration between two cities.

3. packing_list(days: int)
   • Suggests a packing checklist based on trip duration.

4. budget_estimate(destination: str, trip_type: str)
   • Returns an approximate budget range in INR (mock values).

5. get_live_weather(city)
   • Fetches real-time weather information for any city.

General Rules:
- Use tools whenever the user asks for information provided by a tool.
- If the user’s question doesn’t require a tool, answer directly.
- Give friendly, helpful responses.
"""
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
def estimate_flight_time(origin, destination):
    """Give flight time."""
    times = {
        ("Delhi", "Paris"): "8h",
        ("Mumbai", "Dubai"): "3h",
        ("New York", "London"): "7h"
    }
    return times.get((origin.title(), destination.title()), "Unknown")

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
def budget_estimate(destination, trip_type):
    """Basic budget info."""
    amounts = {"budget": 2000, "standard": 5000, "luxury": 12000}
    amt = amounts.get(trip_type.lower(), 3000)
    return f"{destination}: {amt} INR/day"

# EXTERNAL TOOL ADDITION
@tool("live_weather")
def get_live_weather(city: str) -> str:
    """
    Fetch real-time weather information using WeatherAPI.com.
    Use this tool when the user asks about:
    - current weather
    - temperature
    - conditions in a city
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key not found. Please set WEATHER_API_KEY in the .env file."

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "error" in data:
            return f"Could not fetch weather info: {data['error'].get('message', 'Unknown error')}"

        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]

        return f"Weather in {city.title()}: {temp_c}°C, {condition}"

    except requests.exceptions.Timeout:
        return "Request timed out. Try again."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
memory = InMemorySaver()
thread = "travel1"

# Add in the tool box
tools = [suggest_destinations, estimate_flight_time, packing_list, budget_estimate, get_live_weather]

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