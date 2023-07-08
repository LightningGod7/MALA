import subprocess

vanilla_command = ls

def execute_command(vanilla_command, output_file):
    command = "nohup " + vanilla_command + " > " + output_file + "&"
    print("executing `" + command + "`")
    try:
        subprocess.run(vanilla_command, shell=True)
    except:
        print()
        return None

# def check_status(command_to_check):

#     output_file = command_to_check

#     command = "tail -f " + output_file
#     # subprocess.run(command, shell=True)