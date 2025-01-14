import asyncio
import os


from llama_stack_client.lib.agents.event_logger import EventLogger

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.types import ToolResponseMessage
from story_teller import StoryTeller
from terminal_tool import TerminalTool

LLAMA_STACK_HOST = "192.168.1.98"
LLAMA_STACK_PORT = 5001
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL", "meta-llama/Llama-3.2-3B-Instruct")

story_teller = StoryTeller()
terminal_tool = TerminalTool()

def create_agent(client: LlamaStackClient, model: str) -> Agent:
    """Creates and returns an agent with the given client and model."""
    agent_config = AgentConfig(
        model=model,
        instructions="You are a helpful assistant. You will chat with the user. When the user asks, call tools like this: [open_terminal_tool(parameters={'command': 'echo \"Hello, World!\"'})].",
        enable_session_persistence=False,
        streaming=False,
        tool_choice="required",
        tools=[
            story_teller.get_tool_definition(),
            terminal_tool.get_tool_definition()
        ],
        tool_prompt_format="python_list",
    )
    return Agent(client, agent_config, [story_teller, terminal_tool])

async def handle_responses(agent: Agent, session_id: str, user_prompts: list[str]) -> None:
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
        
        loop = asyncio.get_running_loop()
        logs = await loop.run_in_executor(None, EventLogger().log, response)
        for log in logs:
            log.print()
        
        # for res in response:
        #     print(res)
        #     if hasattr(res, 'event') and hasattr(res.event, 'payload') and hasattr(res.event.payload, 'event_type') and res.event.payload.event_type == 'step_complete':
        #         step_details = res.event.payload.step_details
        #         print(step_details.inference_model_response.content)
        #     elif isinstance(res, ToolResponseMessage):
        #         print(res.content.text)

async def agent_test() -> None:
    """Tests the agent by creating a session and handling responses."""
    client = LlamaStackClient(
        base_url=f"http://{LLAMA_STACK_HOST}:{LLAMA_STACK_PORT}",
    )

    agent = create_agent(client, INFERENCE_MODEL)
    user_prompts = [
        "PLEASE USER 'story_teller' TOOL TO GENERATE A STORY with name 'test_story'.",
    ]

    session_id = agent.create_session("test-session")
    await handle_responses(agent, session_id, user_prompts)

asyncio.run(agent_test())