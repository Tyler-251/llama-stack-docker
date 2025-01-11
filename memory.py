import os
from llama_stack_client import LlamaStackClient

client = LlamaStackClient(base_url="http://172.29.87.129:5001")

# List available models
# models = client.models.list()
# print(models)
print("Thinking...")

# Register a memory bank
bank_id = "my_documents"
response = client.memory_banks.register(
    memory_bank_id=bank_id,
    params={
        "memory_bank_type": "vector",
        "embedding_model": "all-MiniLM-L6-v2",
        "chunk_size_in_tokens": 512
    }
)

# Insert documents
# documents = [
#     {
#         "document_id": "doc1",
#         "content": "The banks name is LlamaBank Inc",
#         "mime_type": "text/plain"
#     },
#     {
#         "document_id": "doc2",
#         "content": "Bank earnings are $150k",
#         "mime_type": "text/plain"
#     },
#     {
#         "document_id": "doc3",
#         "content": "Bank owner is John Doe",
#         "mime_type": "text/plain"
#     }
# ]
# client.memory.insert(
#     bank_id=bank_id,
#     documents=documents
# )

# Query documents
results = client.memory.query(
    bank_id="my_documents",
    query="bank owner",
)

# client.memory_banks.unregister(memory_bank_id="my_documents")

print ("\033[A                             \033[A") # Clear the "Thinking..." message
print(results.chunks[0].content)