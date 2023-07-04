import subprocess  # For executing shell commands
import importlib
import inspect 
from tabulate import tabulate

import executer

#DEFINE
PROMPT = "MALA"
MODULE = ""

def initialize(loaded_modules, universal_variables, tool_paths):
    global modules, variables, tools
    modules = loaded_modules
    variables = universal_variables
    tools = tool_paths

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
    selected_var = args[0]
    new_value = " ".join(args[1:])

    for key1, nested_dict in variables.items():
        if selected_var in nested_dict:
            nested_dict[selected_var]["Value"] = new_value

    print(f"[*] {selected_var} set to: {new_value}")

# Function to handle the SHOW command
def show_variables():
    common_vars = variables["common_variables"]
    module_vars = variables["module_variables"]

    common_table = [["Name", "Value", "Description"]]
    for var, details in common_vars.items():
        common_table.append([var, details["Value"], details["Description"]])

    module_table = [["Name", "Value", "Description"]]
    for var, details in module_vars.items():
        module_table.append([var, details["Value"], details["Description"]])

    print("\n--Common Options--\n")
    print(tabulate(common_table, headers="firstrow", tablefmt="pretty"))
    print("\n--Module Options--\n")
    print(tabulate(module_table, headers="firstrow", tablefmt="pretty"))

# Function to handle executing modules
def use_module(arg):
    global variables, MODULE, new_module
    module_path = arg[0]
    variables["module_variables"].clear()
    try:
        module = importlib.import_module(module_path)
        module_class = inspect.getmembers(module, inspect.isclass)
        if module_class:
            class_name, class_obj = module_class[0]
            new_module = class_obj(tools, variables)
            MODULE = "(" + class_name + ")"
            new_module.test()
            return new_module
    except ModuleNotFoundError:
        print(f"Module '{module_path}' not found.")

# Function to show modules loaded
def show_modules():
    for loaded_modules in modules:
        print(loaded_modules)

def execute():
    command_list = new_module.get_command_list()
    if not command_list:
        print("Nothing to run. No module selected or compulsory options are not set.")
    executer.execute_command(command_list)

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
        "modules": {
        "function": show_modules,
        "description": "show all available modules"
    },
    "use": {
        "function": use_module,
        "description": "set context to a module"
    },
    "run": {
        "function": execute,
        "description": "execute the current command built from the module"
    } 
}

# Main
def main():
    while True:
        try:
            user_input = input("\n" + PROMPT + MODULE + " > ").strip()
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


