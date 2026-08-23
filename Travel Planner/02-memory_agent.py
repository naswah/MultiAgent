from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai.types import Content, Part
import asyncio
from dotenv import load_dotenv

load_dotenv()

agent= LlmAgent(
    model= "gemini-3-flash-preview",
    name="FlightAgent",
    description="Your departure city is {departure}." 
    "This agent can remember the information you provide and recall it later.",
    tools= [PreloadMemoryTool()]
)

#create runner
runner= InMemoryRunner(agent=agent, app_name= "agents")

async def run_dialogue():
    #First session, user gives some info
    session_id= "session_1"

    # Create session
    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id= "user1",
        session_id= session_id
    )

    print("I am travelling to Tokyo.")

    content= Content(role= "user", parts= [Part(text= "I am travelling to Tokyo.")])

    async for event in runner.run_async(user_id= "user1", session_id= session_id, new_message= content):
        #Check if the event has content and parts, and the author is not the user
        if event.content and event.content.parts and event.author != 'user':
            for part in event.content.parts:
                if part.text:
                    print(f"Agent: {part.text}")

    #After the conversation, we can retrieve the session and add it to memory
    session= await runner.session_service.get_session(
        app_name=runner.app_name,
        user_id= "user1",
        session_id= session_id
    )
    await runner.memory_service.add_session_to_memory(session)

    print("\n")
    print("User: Where am I travelling?")
    content= Content(role= "user", parts= [Part(text= "Where am I travelling?")])

    async for event in runner.run_async(user_id= "user1", session_id= session_id, new_message= content):
        #Check if the event has content and parts, and the author is not the user
        if event.content and event.content.parts and event.author != 'user':
            for part in event.content.parts:
                if part.text:
                    print(f"Agent: {part.text}")

asyncio.run(run_dialogue())