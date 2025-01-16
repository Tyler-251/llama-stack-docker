import os
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types.agent_create_params import AgentConfig
from termcolor import colored

client = LlamaStackClient(base_url="http://172.29.87.129:5001")

available_models = [
    model.identifier for model in client.models.list()
]

print(available_models)