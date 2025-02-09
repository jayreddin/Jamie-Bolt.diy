import pyautogui
import time

def test_pyautogui():
    # Test writing text
    pyautogui.write("Hello, World!", interval=0.1)
    time.sleep(1)
    # Test pressing a key
    pyautogui.press("enter")
    time.sleep(1)
    # Test hotkey combination
    pyautogui.hotkey("ctrl", "shift", "n")

if __name__ == "__main__":
    test_pyautogui()
