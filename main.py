import os
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url="http://192.168.1.98:5001")

# List available models
# models = client.models.list()
# print(models)
print("Thinking...")

# response = client.inference.with_streaming_response.chat_completion(
response = client.inference.chat_completion(
    model_id="meta-llama/Llama-3.2-3B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "write a 3 sentence short poem on docker containers"},
    ]
)

print ("\033[A                             \033[A") # Clear the "Thinking..." message
print(response.completion_message.content)