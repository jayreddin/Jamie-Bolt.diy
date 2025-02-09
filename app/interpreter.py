import json
from multiprocessing import Queue
from time import sleep
from typing import Any
import pyautogui
import subprocess
import logging

# Configure logging settings
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Interpreter:
    def __init__(self, status_queue: Queue):
        self.status_queue = status_queue
        logging.debug("Interpreter initialized")

    def process_commands(self, json_commands: list[dict[str, Any]]) -> bool:
        for command in json_commands:
            success = self.process_command(command)
            if not success:
                logging.error("Failed to process command: %s", command)
                return False
        return True

    def process_command(self, json_command: dict[str, Any]) -> bool:
        function_name = json_command['function']
        parameters = json_command.get('parameters', {})
        human_readable_justification = json_command.get('human_readable_justification')
        logging.debug("Now performing - %s - %s - %s", function_name, parameters, human_readable_justification)
        self.status_queue.put(human_readable_justification)
        try:
            self.execute_function(function_name, parameters)
            return True
        except Exception as e:
            logging.error("Error executing command: %s", e)
            logging.error("Received JSON: %s", json.dumps(json_command, indent=2))
            logging.error("Extracted function_name: %s, parameters: %s", function_name, parameters)
            return False

    def execute_function(self, function_name: str, parameters: dict[str, Any]) -> None:
        pyautogui.press("command", interval=0.2)
        logging.debug("Executing function: %s with parameters: %s", function_name, parameters)

        if function_name == "sleep" and parameters.get("secs"):
            sleep(parameters.get("secs"))
        elif function_name == "screenshot" and parameters.get("output_file"):
            take_screenshot(parameters.get("output_file"))
        elif hasattr(pyautogui, function_name):
            function_to_call = getattr(pyautogui, function_name)
            try:
                if function_name == 'write' and ('string' in parameters or 'text'):
                    string_to_write = parameters.get('string') or parameters.get('text')
                    interval = parameters.get('interval', 0.1)
                    function_to_call(string_to_write, interval=interval)
                elif function_name == 'press' and ('keys' in parameters or 'key'):
                    keys_to_press = parameters.get('keys') or parameters.get('key')
                    presses = parameters.get('presses', 1)
                    interval = parameters.get('interval', 0.2)
                    function_to_call(keys_to_press, presses=presses, interval=interval)
                elif function_name == 'hotkey':
                    function_to_call(*parameters['keys'])
                else:
                    function_to_call(**parameters)
                logging.debug("Successfully executed function: %s", function_name)
            except Exception as e:
                logging.error("Error executing pyautogui function: %s", e)
        else:
            logging.error("No such function %s in our interface's interpreter", function_name)

def take_screenshot(output_file):
    try:
        subprocess.run(['mate-screenshot', '--file', output_file], check=True)
        logging.debug("Screenshot saved to %s", output_file)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to take screenshot: %s", e)
