import llama_stack_client
import csv

client = llama_stack_client.LlamaStackClient(base_url="http://192.168.1.98:5001")

pairs = []

with open('1429_1.csv', 'r') as file:
    reader = csv.reader(file)
    index = 0
    for row in reader:
        result = client.inference.chat_completion(
            model_id="meta-llama/Llama-3.2-3B-Instruct",
            messages=[
                {"role": "system", "content": "You are a sentiment analyzer for reviews. You will give a response of 1-5 stars based on the sentiment of the review. Only respond with the number"},
                {"role": "user", "content": row[16]},
            ]
        )
        try:
            pairs.append([int(result.completion_message.content), int(row[14])])
        except:
            pass
        index += 1
        
        print(row[16])
        print("Model response: " + result.completion_message.content)
        print("Actual rating: " + row[14])
        print("")
        
        if index == 10:
            break

difference = []
for pair in pairs:
    difference.append(abs(pair[0] - pair[1]))

print(pairs)
print("Average inaccuracy: " +  (sum(difference) / len(difference)).__str__())