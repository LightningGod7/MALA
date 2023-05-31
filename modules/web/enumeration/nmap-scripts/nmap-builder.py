import subprocess

script_list = [
    "http-config-backup",
    "http-drupal-enum-users",
    "http-drupal-enum",
    "http-enum",
    "http-fileupload-exploiter",
    "http-form-brute",
    "http-form-fuzzer",
    "http-waf-detect",
    "http-waf-fingerprint",
    "http-webdav-scan",
    "http-joomla-brute",
    "http-phpmyadmin-dir-traversal",
    "http-wordpress-brute",
    "http-wordpress-enum",
    "http-wordpress-users"
]

scripts_with_additional_args = [
    "http-fileupload-exploiter.nse",
    "http-form-brute.nse",
    "http-form-fuzzer.nse",
    "http-waf-fingerprint.nse",
    "http-joomla-brute.nse",
    "http-phpmyadmin-dir-traversal.nse",
    "http-wordpress-brute.nse",
    "http-wordpress-enum.nse",
]


script_name = ""

def nmap_script_choice(choice):
    script_name = script_list[choice]

def build_nmap_command(target, port, script_name, script_args=None):
    command = ['nmap', '-p', '80,443', '-sV', '--script', script_name, target]
    
    if script_args:
        command.extend(['--script-args', script_args])
    
    return command

def execute_nmap_command(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Command execution failed with return code {e.returncode}: {e.output}"

# Example usage
target = 'example.com'
script_name = 'http-vuln-cve2014-3704'
script_args = 'targeturi=/admin'

command = build_nmap_command(target, script_name, script_args)
output = execute_nmap_command(command)
print(output)
