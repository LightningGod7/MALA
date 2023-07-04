import subprocess

def execute_command(command_list):
    command = " ".join(command_list)
    print("executing `" + command + "`")
    # subprocess.run(command, shell=True)
