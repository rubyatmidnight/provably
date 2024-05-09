import keyboard
import pyautogui

print("Working...")

## change keybinds and the coordinates here. 
## I used this script to set crash to a spot on my screen and I just have to hit a keybind/combination to cash out instead of having to click, so I can do it without latency while multitasking. its not efficient but it works.

key_combination = ['ctrl', 'q']
click_x = 320
click_y = 570

def perform_click():
    pyautogui.click(click_x, click_y)

def key_pressed(event):
    if all(keyboard.is_pressed(key) for key in key_combination):
        perform_click()

keyboard.hook(key_pressed)

keyboard.wait('esc') 
