import os
import json
import controller
import importlib.util #Dynamically load modules


###DECLARE
config_file_path = r"./configs/universal-configs.json"
modules_folder_path = r"./modules"
TOOLS_PATH = r"./configs/toolpath.json"

#Load all modules into dictionary
def module_load(modules_folder):
    modules = []

    #Search through module directory for all python files (modules)
    for root, dirs, files in os.walk(modules_folder):
        for file in files:
            if file.endswith(".py"):
                module_path = os.path.join(root, file)
                modules.append(module_path)
    return modules

#Load json configs
def initialize_configs(config_file):
    with open(config_file) as default_configs:
        configs = json.load(default_configs)
    return configs

def startup_message():
    #Color Coding
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    print(bcolors.WARNING + """
Initialising MALA : Modularised Attack Landscape Analyser""" + bcolors.ENDC)
    print(bcolors.FAIL + """
 ███▄ ▄███▓ ▄▄▄       ██▓    ▄▄▄         
▓██▒▀█▀ ██▒▒████▄    ▓██▒   ▒████▄       
▓██    ▓██░▒██  ▀█▄  ▒██░   ▒██  ▀█▄     
▒██    ▒██ ░██▄▄▄▄██ ▒██░   ░██▄▄▄▄██    
▒██▒   ░██▒ ▓█   ▓██▒░██████▒▓█   ▓██▒   
░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░▓  ░▒▒   ▓▒█░   
░  ░      ░  ▒   ▒▒ ░░ ░ ▒  ░ ▒   ▒▒ ░   
░      ░     ░   ▒     ░ ░    ░   ▒      
       ░         ░  ░    ░  ░     ░  ░  
    """ + bcolors.ENDC)
    print(bcolors.WARNING + """Rights and Licensing:
This project, including all its code, documentation, and associated resources, is the intellectual property of TEAMFOURTEEN. All rights are reserved unless otherwise stated.

License:
Unless explicitly mentioned in individual files or directories within this repository, the project is licensed under Singapore Institute of Technology. The licensing information can be found in the LICENSE file included in this repository.\n""" + bcolors.ENDC)

    print(bcolors.OKBLUE + """Disclaimer: This tool is intended for educational and authorized testing purposes only.
By accessing and using this tool, you acknowledge that you are solely responsible for your actions and agree to use it strictly within the boundaries of applicable laws and regulations.
The developer of this tool assumes no liability for any unauthorized or malicious use. 
Users are advised to seek appropriate permissions and authorization before conducting any tests on networks, systems, or applications. 
Any actions performed using this tool without proper consent are strictly prohibited.\n""" + bcolors.ENDC)
    return

if __name__ == "__main__":
    modules = module_load(modules_folder_path)
    variables = initialize_configs(config_file_path)
    tool_paths = initialize_configs(TOOLS_PATH)
    startup_message()
    controller.initialize(modules, variables, tool_paths)
    controller.main()
