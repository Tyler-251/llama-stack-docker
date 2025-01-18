import asyncio
import os
import json

from llama_stack_client.lib.agents.event_logger import EventLogger

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.types import ToolResponseMessage
from story_teller import StoryTeller
from terminal_tool import TerminalTool
from llava_tool import VisualTool

LLAMA_STACK_HOST = "192.168.1.98"
LLAMA_STACK_PORT = 5001
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL", "meta-llama/Llama-3.2-3B-Instruct")

story_teller = StoryTeller()
terminal_tool = TerminalTool()
visual_tool = VisualTool()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
messages = [
    {
        "role": "user",
        "content": "Hello, who are you?",
    }
]

def create_agent(client: LlamaStackClient, model: str) -> Agent:
    """Creates and returns an agent with the given client and model."""
    
    with open("./agent/system_instructions.txt", "r") as file:
        system_instructions = file.read()
    
    agent_config = AgentConfig(
        model=model,
        instructions=system_instructions,
        enable_session_persistence=False,
        streaming=False,
        tool_choice="required",
        tools=[
            visual_tool.get_tool_definition(),
            {
                "type": "brave_search",
                "engine": "brave",
                "api_key": "BSA1ivyQ7ZtlrAUbE5uJH4sM4YGgKPH",
            },
        ],
        tool_prompt_format="python_list",
    )
    return Agent(client, agent_config, [visual_tool])

async def handle_responses(agent: Agent, session_id: str) -> None:
    """Handles the responses from the agent for the given user prompts."""
    while True:
        prompt = input("Enter your prompt (or 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break 
        
        response = agent.create_turn(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            session_id=session_id,
        )
        for res in response:
            tool_response = None
            if isinstance(res, ToolResponseMessage): 
                print(f"{bcolors.HEADER}Tool Response:{bcolors.ENDC}")
                print(f"{bcolors.OKGREEN}{res.content.text}{bcolors.ENDC}")
                tool_response = agent.create_turn( #reroute input to model
                    messages=[{
                        "role": "user",
                        "content": res.content.__str__(),    
                    }],
                    session_id=session_id,
                )
            else: # if regular message
                if hasattr(res, "event"):
                    if hasattr(res.event.payload, "text_delta"):
                        print(f"{bcolors.OKCYAN}{res.event.payload.text_delta}{bcolors.ENDC}", end="", flush=True)
                    elif hasattr(res.event.payload, "event_type"):
                        if res.event.payload.event_type == "step_complete":
                            print()
                    
                
            if tool_response:
                for res in tool_response:
                    if hasattr(res, "event"):
                        if hasattr(res.event.payload, "text_delta"):
                            print(f"{bcolors.OKCYAN}{res.event.payload.text_delta}{bcolors.ENDC}", end="", flush=True)
                        elif hasattr(res.event.payload, "event_type"):
                            if res.event.payload.event_type == "step_complete":
                                print()
            

        # tool_response = None
        # loop = asyncio.get_running_loop()
        # logs = await loop.run_in_executor(None, EventLogger().log, response)
        # for log in logs:
        #     if log.role == "CustomTool":
        #         print("Tool recieved...")
        #         print(log.content)
        #         tool_response = agent.create_turn(
        #             messages=[{"Tool response: " + log.content.__str__()}],
        #             session_id=session_id,
        #         )
        #     else: 
        #         log.print()

async def agent_test() -> None:
    """Tests the agent by creating a session and handling responses."""
    client = LlamaStackClient(
        base_url=f"http://{LLAMA_STACK_HOST}:{LLAMA_STACK_PORT}",
    )

    agent = create_agent(client, INFERENCE_MODEL)

    session_id = agent.create_session("test-session")
    await handle_responses(agent, session_id)

asyncio.run(agent_test())