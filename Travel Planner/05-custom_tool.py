import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
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

flight_agent= Agent(
    model= "gemini-3-flash-preview",
    name="FlightAgent",
    description="You are a flight assistant. Get weather tool for fetching weather information.",
    instruction="""You are a travel assistant.
    - If the user asks for weather information, use the provided weather tool to fetch the weather data.
    - Otherwise respond appropriately to the user's query.
    When returning weather, report temperature, wind speed and other available data.""",
    tools=[weather_tool]
)

async def main():
    runner= InMemoryRunner(agent=flight_agent)
    user_query= "Get weather for Dubai. Latitude: 25.276987, Longitude: 55.296249"
    events= await runner.run_debug(user_query)

if __name__ == "__main__":
    asyncio.run(main())