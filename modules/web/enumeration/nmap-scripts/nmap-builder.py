import subprocess

nmap_variables = {"script": [], "args":""}

def set_nmap_variables(args):
    if len(args) < 2:
        print("Usage: SET <variable> <value>")
        return
    variable = args[0].lower()
    value = " ".join(args[1:])
    nmap_variables[variable] = value
    print(f"[*] {variable} set to: {value}")

scripts_noargs = {
    "backup-config-enum": "http-config-backup",
    "drupal-users-enum": "http-drupal-enum-users",
    "drupal-enum": "http-drupal-enum",
    "enum": "http-enum",
    "waf-detect": "http-waf-detect",
    "webdav-scan": "http-webdav-scan",
    "wordpress-users": "http-wordpress-users"
}

scripts_withargs = {
    "uploads-exploit": "http-fileupload-exploiter",
    "form-brute": "http-form-brute",
    "form-fuzz": "http-form-fuzzer",
    "waf-fingerprint": "http-waf-fingerprint",
    "joomla-brute": "http-joomla-brute",
    "phpmyadmin-dir-traversal": "http-phpmyadmin-dir-traversal",
    "wordpress-brute": "http-wordpress-brute",
    "wordpress-enum": "http-wordpress-enum"
}

script_options = ""
def nmap_script_option(option):
    for script in option:
        if script in scripts_withargs and not nmap_variables["args"]:
            print("script selected require arguments but none were given")
            return
        
        script_options += script + ","
    script_options.chop()

def build_nmap_command(target, port, script_options, script_args=None):
    command = ['nmap', '-p', port, '-sV', '--script', script_options, target]
    
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
