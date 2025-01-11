#!/bin/bash

export INFERENCE_MODEL="meta-llama/Llama-3.2-1B-Instruct"
# ollama names this model differently, and we must use the ollama name when loading the model
export OLLAMA_INFERENCE_MODEL="llama3.2:1b-instruct-fp16"
export LLAMA_STACK_PORT=5001

# Find IP Address
export IP_ADDRESS=$(hostname -I | cut -d' ' -f1)

# Ensure dockerd is running
if pgrep -x "dockerd" > /dev/null
then
    echo "Docker is already running"
else
    echo "Starting Docker daemon..."
    sudo dockerd &
fi

while [ true ]
do
    if pgrep -x "dockerd" > /dev/null
    then
        echo "Docker daemon is running"
        break
    else
        echo "Docker daemon is not running... retrying in 5 seconds"
        sleep 5
    fi
done

# Serve ollama if not already running
if pgrep -x "ollama" > /dev/null
then
    ollama_pid=$(pgrep -x "ollama")
    echo "ollama is already running with PID $ollama_pid, launching model"
else
    echo "Starting ollama..."
    OLLAMA_HOST=$IP_ADDRESS ollama serve &
fi

echo "Running model $INFERENCE_MODEL..."
echo "Ollama model name: $OLLAMA_INFERENCE_MODEL"
echo "Ollama stack port: $LLAMA_STACK_PORT"

OLLAMA_HOST=$IP_ADDRESS ollama list
OLLAMA_HOST=$IP_ADDRESS ollama run $OLLAMA_INFERENCE_MODEL --keepalive 60m &


sudo docker run -it \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  -v ~/.llama:/root/.llama \
  llamastack/distribution-ollama \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env OLLAMA_URL=http://$IP_ADDRESS:11434/
