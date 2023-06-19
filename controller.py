import subprocess  # For executing shell commands
import json # Read the config file for options

variables = {}  # Dictionary to store variables
modules = []

def initialize(loaded_modules, universal_variables):
    global modules, variables
    modules = loaded_modules
    variables = universal_variables

def command_not_found(available_commands):
    print("No such command, refer to available commands: \n")
    for command, handler in available_commands.items():
        command_description = handler.get("description", "No description")
        print(f"{command} - {command_description}")

# Function to handle the SET command
def set_variable(args):
    global variables
    if len(args) < 2:
        print("Usage: SET <variable> <value>")
        return
    variable = args[0]
    value = " ".join(args[1:])
    variables[variable] = value
    print(f"[*] {variable} set to: {value}")

# Function to handle the SHOW command
def show_variables():
    for variable, value in variables.items():
        print(f"{variable}: {value}")

# Function to handle executing other commands
def use_module(command):
    subprocess.call(command, shell=True)

# Dictionary mapping commands to functions and their arguments
command_handlers = {
    "set": {
        "function": set_variable,
        "description": "Set a variable"
    },
    "variables": {
        "function": show_variables,
        "description": "Show variables"
    },
    "use": {
        "function": use_module,
        "description": "set context to a module"
    }
}

# Main
def main():
    while True:
        try:
            user_input = input("wst > ").strip()
            if user_input.lower() == "exit":
                break
            command = user_input.split()[0].lower()
            args = user_input.split()[1:]

            if command in command_handlers:
                command_function = command_handlers[command].get("function")
                command_function(args) if len(args) != 0 else command_function()
            else:
                command_not_found(command_handlers)
            
            # # Call the command function
            # command_function()
            
        except KeyboardInterrupt:
            print("\nCtrl+C pressed. Exiting...")
            break


