import subprocess as sp
import psutil
import os
import signal
import time

default_error_file = os.path.join(".", "output", "error.out")

def execute_command(vanilla_command, mala_output_file):
    if not os.path.exists(mala_output_file):
        os.makedirs(os.path.dirname(mala_output_file), exist_ok=True)
    command = vanilla_command + " > " + mala_output_file + " 2>&1 &"
    print("executing `" + vanilla_command + "`")
    print("saving output to: " + mala_output_file)
    #process = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    # stdout, stderr = process.communicate()
    # output = stdout.decode()
    # error = stderr.decode()
    #return process.pid

def get_process_status(pid):
    try:
        process = psutil.Process(pid)
        if process.is_running():
            return "Running"
        else:
            return f"Exited with code: {process.returncode}"
    except psutil.NoSuchProcess:
        return "Completed"

def get_command_output(file_to_read):
    print(file_to_read)
    try:
       tail_process = sp.Popen(["tail","+1f", file_to_read])
       input("\n==============================================PRESS ENTER TO STOP DISPLAYING OUTPUT==============================================\n")
       tail_process.terminate()
    except KeyboardInterrupt:
        return


    # except FileNotFoundError:
    #     sp.Popen(['powershell', 'Get-Content', '-Path', file_to_read, '-Tail', '10'])
def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait(timeout=5)
        while get_process_status(pid) == "Running":
            process.kill()
            process.wait()
            continue
        print(get_process_status(pid))
        return True
    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}")
        return False
