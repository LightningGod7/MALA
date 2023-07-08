import subprocess as sp
import psutil
import os


default_error_file = os.path.join(".", "output", "error.out")
# vanilla_command = f'/usr/bin/wfuzz -z range,000-999 -u http://guohuaqun.mooo.com/FUZZ/login.php -b ict2206:jaimatadi > {default_output_file}'
def execute_command(vanilla_command, mala_output_file):
    command = vanilla_command + " > " + mala_output_file
    print("executing `" + command + "`")
    process = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    # stdout, stderr = process.communicate()
    # output = stdout.decode()
    # error = stderr.decode()
    return process.pid

def process_check(pid):
    try:
        process = psutil.Process(pid)
        if process.is_running():
            return "Running"
        else:
            return f"Exited with code: {process.returncode}"
    except psutil.NoSuchProcess:
        return "Completed"

def get_status(file_to_read):
    print(file_to_read)
    try:
        sp.run(["tail", file_to_read])
    except FileNotFoundError:
        sp.run(['powershell', 'Get-Content', '-Path', file_to_read, '-Tail', '10'])
    except KeyboardInterrupt:
        return 
