import requests
import json
import base64

import pyautogui
import os
os.environ["PYAUTOGUI_OS"] = "windows"


screenshot = pyautogui.screenshot()
screenshot.save('./temp/screenshots/screenshot.png')

with open("./temp/screenshots/screenshot.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

response = requests.post("http://192.168.1.98:11434/api/generate", json={"model": "llava:latest", "prompt": "Whats going on in this environment? Be brief and use a list.", "stream": False, "images": [encoded_string.decode("utf-8")]})

print(response.status_code)

print(response.text)