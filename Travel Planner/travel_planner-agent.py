import asyncio
from google.adk.agents import Agent, LlmAgent, ParallelAgent, SequentialAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool, google_search
from dotenv import load_dotenv
import requests

load_dotenv()

def get_weather(coords:dict)-> dict:
    lat= coords.get("latitude")
    lon= coords.get("longitude")
    if lat is None or lon is None:
       return {"error": "Missing latitude or longitude."}
    
    url= "https://api.open-meteo.com/v1/forecast"

    params={
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    resp= requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data= resp.json()
    return data

weather_tool = FunctionTool(func=get_weather)


flight_agent= LlmAgent(
    model= "gemini-3-flash-preview",
    name="FlightAgent",
    description="You are a flight assistant. Get weather tool for fetching weather information.",
    instruction="""You are a travel assistant.
    - If the user asks for weather information, use the provided weather tool to fetch the weather data.
    - For flight details, respond based on your general knowledge; do not call external tools.
    - Otherwise respond appropriately to the user's query.
    When returning weather, report temperature, wind speed and other available data.""",
    tools=[weather_tool]
)


sight_seeing_agent= LlmAgent(
    model= "gemini-3-flash-preview",
    name="SightSeeingAgent",
    description="Find sightseeing options for destination.",
    tools=[google_search]
)


hotel_agent= LlmAgent(
    model= "gemini-3-flash-preview",
    name="HotelAgent",
    description="Find hotel options for destination.",
    tools=[google_search]
)


parallel_agent= ParallelAgent(
    name= "TravelPlannerAgent",
    sub_agents= [flight_agent, sight_seeing_agent, hotel_agent],
    description= "This agent can help you plan your travel by providing flight details, sightseeing options, and hotel recommendations."
)

travel_planner_agent= SequentialAgent(
    name= "TravelPlannerAgent",
    sub_agents= [parallel_agent],
    description= "Plan your trip by gathering flight details, sightseeing options, weather information, and hotel recommendations. Summarize the findings to the user."
)

#Setup runner and test

async def main():
    runner= InMemoryRunner(agent= travel_planner_agent)
    user_query= """Plan a trip to Paris.
    What is the current weather at lalitude 48.8566 and longitude 2.3522?
    Also, find sightseeing options and hotel recommendations.   """
    events= await runner.run_debug(user_query)

if __name__ == "__main__":
    asyncio.run(main())