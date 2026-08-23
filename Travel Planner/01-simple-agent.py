import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from dotenv import load_dotenv

load_dotenv()

flight_agent= Agent(
    model= "gemini-3-flash-preview",
    name="FlightAgent",
    description="Tell me about optiomal route between the flights."
)

async def main():
    runner= InMemoryRunner(agent=flight_agent)
    events= await runner.run_debug("How many layovers are there between NewYork and Tokyo?")

if __name__ == "__main__":
    asyncio.run(main())