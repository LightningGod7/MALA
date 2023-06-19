import os
import json
import controller

###DECLARE
config_file_path = r".\configs\universal-configs.json"
modules_folder_path = r".\modules"

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

#Load default configs
def initialize_defaults(config_file):
    with open(config_file) as default_configs:
        universal_variables = json.load(default_configs)
    return universal_variables


if __name__ == "__main__":
    modules = module_load(modules_folder_path)
    variables = initialize_defaults(config_file_path)
    controller.initialize(modules, variables)
    controller.main()
