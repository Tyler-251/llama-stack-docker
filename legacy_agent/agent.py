import os
import asyncio
import json

from typing import TypedDict, Optional, Dict, Any, List

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types.agent_create_params import AgentConfig

from llama_stack_client.types.tool_param_definition_param import ToolParamDefinitionParam
from llama_stack_client.types import CompletionMessage,ToolResponseMessage, UserMessage
from llama_stack_client.lib.agents.custom_tool import CustomTool
from llama_stack_client.types import FunctionCallToolDefinition

class TerminalTool(CustomTool):
    def get_name(self) -> str:
        return "terminal_tool"
    
    def get_description(self) -> str:
        return "Opens a terminal window"
    
    def get_params_definition(self) -> dict:
        return {
        }
        
    def run(self, messages: List[CompletionMessage]) -> List[ToolResponseMessage]:
        
        print("Made it here")
        
        tool_call = messages[0].tool_calls[0]

        message = ToolResponseMessage(
            call_id=tool_call.call_id,
            tool_name=self.get_name(),
            content="terminal opened",
            role="ipython",
        )
        return [message]
    
    async def run_impl(self, messages: List[CompletionMessage]) -> List[ToolResponseMessage]:
        return await self.run(messages)

async def agent_example():
    
    date = os.popen('date').read()
    
    terminal_tool = TerminalTool()

    client = LlamaStackClient(base_url=f"http://192.168.1.98:5001")
    agent_config = AgentConfig(
        model="meta-llama/Llama-3.2-1B-Instruct",
        instructions="You are a helpful assistant named Llarvis! You may respond to the user, but make sure to call tools when you are able to. Today's date is " + date + ". Call tools like this: [open_terminal_tool(parameters={'command': 'echo \"Hello, World!\"'})].",
        sampling_params={
            "strategy": "greedy",
            "temperature": 1.0,
            "top_p": 0.9,
        },
        tools= [
            {
                "type": "brave_search",
                "engine": "brave",
                "api_key": "BSA1ivyQ7ZtlrAUbE5uJH4sM4YGgKPH",
            },
            {
                "type": "code_interpreter",
                "enable_inline_code_execution": True
            },
            terminal_tool.get_tool_definition(),
        ],
        tool_choice="auto",
        tool_prompt_format="python_list",
        input_shields=[],
        output_shields=[],
        enable_session_persistence=False,
    )

    agent = Agent(client, agent_config, [terminal_tool])
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