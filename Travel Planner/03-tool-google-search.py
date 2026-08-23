import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from dotenv import load_dotenv

load_dotenv()

flight_agent= Agent(
    model= "gemini-3-flash-preview",
    name="FlightAgent",
    description="Finds flight options for destination and date",
    tools= [google_search]
)

#Run async_def
async def main():
    runner= InMemoryRunner(agent=flight_agent)
    events= await runner.run_debug("Find me a flight to Paris next month under $500")

if __name__ == "__main__":
    asyncio.run(main())