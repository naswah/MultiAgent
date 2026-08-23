import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.code_executors import BuiltInCodeExecutor
from dotenv import load_dotenv

load_dotenv()

flight_agent= Agent(
    model= "gemini-3-flash-preview",
    name="FlightAgent",
    description="Find flight options or compute flight related data using code execution.",
    instruction="""
      You are a flight-helper agent.
      If the users want to perform calculation (Eg, calculate the fligh durations, cosrs, time differeces, pricr conversions, etc),
      generate a python code snippet inside ```python ``` blocks to perform the calculation.
      The code will be executed automatically and the result will be returned to the user.
""",
    tools= BuiltInCodeExecutor()
)

async def main():
    runner= InMemoryRunner(agent=flight_agent)
    user_query= "Calculate how many hourse beteween 2026-08-23 10:00 UTC and 2026-10-24 02:00 UTC?"
    events= await runner.run_debug(user_query)

if __name__ == "__main__":
    asyncio.run(main())