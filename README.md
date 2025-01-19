# Llama Docker

```serve.bash``` hosts a local ollama runtime with a running model as well as a docker container hosting llama-stack. Python scripts can interact with the ollama model via the llama-stack-client library.  

## Python Dependencies
- python 3.13
- libs via reqs.txt
- WSL specific
    - python installed on windows for custom tool runtimes
    - pyautogui (windows pip)
- Install Tesseract on your local machine

## Server Dependencies
- Ollama 
- Docker 
- Machine Requirements
    - Linux OS
    - GPU (recommended)
