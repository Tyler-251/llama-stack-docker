import pyautogui
import os
os.environ["PYAUTOGUI_OS"] = "windows"


screenshot = pyautogui.screenshot()
screenshot.save('./temp/screenshots/screenshot.png')