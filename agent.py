import os
import asyncio
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types.agent_create_params import AgentConfig

async def agent_example():
    client = LlamaStackClient(base_url=f"http://192.168.1.98:5001")
    agent_config = AgentConfig(
        model="meta-llama/Llama-3.2-1B-Instruct",
        instructions="You are a helpful assistant! If you call builtin tools like brave search, follow the syntax brave_search.call(…)",
        sampling_params={
            "strategy": "greedy",
            "temperature": 1.0,
            "top_p": 0.9,
        },
        tools=[
            {
                "type": "brave_search",
                "engine": "brave",
                "api_key": "BSA1ivyQ7ZtlrAUbE5uJH4sM4YGgKPH",
            }
        ],
        tool_choice="auto",
        tool_prompt_format="function_tag",
        input_shields=[],
        output_shields=[],
        enable_session_persistence=False,
    )

    agent = Agent(client, agent_config)
    session_id = agent.create_session("test-session")
    print(f"Created session_id={session_id} for Agent({agent.agent_id})")

    loop = asyncio.get_running_loop()
    while True:
        prompt = await loop.run_in_executor(None, input, "Enter your prompt (or 'exit' to quit): ")
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

        logs = await loop.run_in_executor(None, EventLogger().log, response)
        for log in logs:
            log.print()

if __name__ == "__main__":
    asyncio.run(agent_example())