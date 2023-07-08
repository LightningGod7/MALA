import importlib
import inspect 
from tabulate import tabulate

import executer

#DEFINE
PROMPT = "MALA"
MODULE = ""

def initialize(loaded_modules, universal_variables, tool_paths):
    global modules, variables, tools, executed_processes
    modules = loaded_modules
    variables = universal_variables
    tools = tool_paths
    executed_processes = {}

#set variable
def set_variable(args):
    global variables
    if len(args) < 2:
        print("Usage: SET <variable> <value>")
        return
    selected_var = args[0]
    new_value = " ".join(args[1:])

    for variable_type, variable_options in variables.items():
        if selected_var in variable_options and variable_type == "common_variables":
            variable_options[selected_var]["Value"] = new_value
            print(f"[*] {selected_var} set to: {new_value}")
            return
        elif selected_var in variable_options and variable_type == "module_variables":
            if new_module.validate_input(selected_var, new_value):
                variable_options[selected_var]["Value"] = new_value
                print(f"[*] {selected_var} set to: {new_value}")
            return
    print(f"[*] {selected_var} is not a valid variable. use `variable` command to see available options")
    
#clear variable
def clear_variable(args):
    global variables
    selected_var = args[0]
    new_value = ""

    for variable_type, variable_options in variables.items():
        if selected_var in variable_options:
            variable_options[selected_var]["Value"] = new_value
            print(f"[*] {selected_var} cleared")
            return
    print(f"[*] {selected_var} does not exist, use `variables` command to see available options")

#show all variables and their values
def show_variables():
    common_vars = variables["common_variables"]
    module_vars = variables["module_variables"]

    common_table = [["Name", "Value", "Description"]]
    for var, details in common_vars.items():
        common_table.append([var, details["Value"], details["Description"], details["Required"]])

    module_table = [["Name", "Value", "Description", "Required"]]
    for var, details in module_vars.items():
        module_table.append([var, details["Value"], details["Description"], details["Required"]])

    print("\n--Common Options--\n")
    print(tabulate(common_table, headers="firstrow", tablefmt="pretty"))
    print("\n--Module Options--\n")
    print(tabulate(module_table, headers="firstrow", tablefmt="pretty"))

#show available modules
def show_modules():
    for loaded_modules in modules:
        print(loaded_modules)

#select module to use
def use_module(arg):
    global variables, MODULE, new_module, class_name
    module_path = arg[0]
    variables["module_variables"].clear()
    try:
        module = importlib.import_module(module_path)
        module_class = inspect.getmembers(module, inspect.isclass)
        if module_class:
            class_name, class_obj = module_class[-1]
            new_module = class_obj(variables)
            MODULE = "(" + class_name + ")"
            return new_module
    except ModuleNotFoundError:
        print(f"\nModule '{module_path}' not found.")

#execute the module
def execute():
    new_module.initialize_before_run(tools,variables)
    command_list = new_module.get_command_list()
    if not command_list:
        print("\nFailed to run. No module selected or compulsory options were not set.")
        return
    
    #Create the actual command from a list
    vanilla_command = " ".join(command_list)

    #attempt to execute command and get pid
    pid = executer.execute_command(vanilla_command)
    if pid:
        executed_processes[pid] = {"module":class_name, "command":vanilla_command, "status":"executed"}

#show list of executed commands
def show_executed():
    #Get status of processes
    for pid in executed_processes.keys():
        executed_processes[pid]["status"] = executer.process_check(pid)

    #Create the table of executed processes
    process_table = [["Index", "PID", "Module", "Command","Status", "Time Executed"]]
    index = 0
    for pid, pid_info in executed_processes.items():
        index += 1
        process_table.append([index, pid, pid_info["module"], pid_info["command"], pid_info["status"]])

    print("\n--Executed commands--\n")
    print(tabulate(process_table, headers="firstrow", tablefmt="pretty"))
    return 0

#check status of a running command or all running commands
def show_status(arg):
    return 0

#handle for when unknown command is given
def command_not_found(available_commands):
    print("No such command, refer to available commands: \n")
    for command, handler in available_commands.items():
        command_description = handler.get("description", "No description")
        print(f"{command} - {command_description}")

# Dictionary mapping commands to functions and their arguments
command_handlers = {
    "set": {
        "function": set_variable,
        "description": "Set a variable",
        "valid_inputs": ["set"]
    },
    "clear": {
        "function": clear_variable,
        "description": "Clear the variable value",
        "valid_inputs": ["clear"]
    },
    "variables": {
        "function": show_variables,
        "description": "Show variables",
        "valid_inputs": ["variables", "options", "vars"]
    },
    "modules": {
        "function": show_modules,
        "description": "Show all available modules",
        "valid_inputs": ["modules", "mods"]
    },
    "use": {
        "function": use_module,
        "description": "Set context to a module",
        "valid_inputs": ["use"]
    },
    "run": {
        "function": execute,
        "description": "Execute the current command built from the module",
        "valid_inputs": ["run"]
    },
    "executed": {
    "function": show_executed,
    "description": "Show running commands",
    "valid_inputs": ["executed"]
    },
    "status": {
        "function": show_status,
        "description": "show status of commands",
        "valid_inputs": ["status"]
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
            matched_command = [command_key for command_key, command_info in command_handlers.items() if command in command_info["valid_inputs"]]        
            if matched_command:
                command_function = command_handlers[matched_command[0]].get("function")
                command_function(args) if len(args) != 0 else command_function()
            else:
                command_not_found(command_handlers)
            
            # # Call the command function
            # command_function()
            
        except KeyboardInterrupt:
            print("\nCtrl+C pressed. Exiting...")
            break


