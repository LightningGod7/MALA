import readline  # For improved command-line input
import subprocess  # For executing shell commands

variables = {}  # Dictionary to store variables

# Function to handle the SET command
def set_variable(args):
    if len(args) < 2:
        print("Usage: SET <variable> <value>")
        return
    variable = args[0].lower()
    value = " ".join(args[1:])
    variables[variable] = value
    print(f"[*] {variable} set to: {value}")

# Function to handle the SHOW command
def show_variables(args):
    for variable, value in variables.items():
        print(f"{variable}: {value}")

# Function to handle executing other commands
def execute_command(command):
    subprocess.call(command, shell=True)

# Main loop
while True:
    try:
        user_input = input("wst > ").strip()
        user_input = input("wst > ").strip()
        if user_input.lower() == "exit":
            break
        elif user_input.lower().startswith("set"):
            args = user_input.split()[1:]
            set_variable(args)
        elif user_input.lower() == "show variables":
            show_variables()
        else:
            execute_command(user_input)
    except KeyboardInterrupt:
        print("\nCtrl+C pressed. Exiting...")
        break
