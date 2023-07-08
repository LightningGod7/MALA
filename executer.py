import subprocess as sp
import psutil
import os

default_output_file = os.path.join(".", "output", "output.out")
default_error_file = os.path.join(".", "output", "error.out")
# vanilla_command = f'/usr/bin/wfuzz -z range,000-999 -u http://guohuaqun.mooo.com/FUZZ/login.php -b ict2206:jaimatadi > {default_output_file}'
def execute_command(vanilla_command, output_file=default_output_file):
    command = vanilla_command + " > " + output_file
    print("executing `" + command + "`")
    process = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = process.communicate()
    output = stdout.decode()
    error = stderr.decode()
    return_code = process.returncode
    return process.pid

def process_check(pid):
    try:
        process = psutil.Process(pid)
        if process.poll() is None:
            return "Running"
        elif process.returncode == 0:
            return "Completed"
        else:
            return f"Exited with error: {process.returncode}"
    except psutil.NoSuchProcess:
        return "Completed"

def get_status(index=default_output_file):
    os.run(f"tail -f {index}" )