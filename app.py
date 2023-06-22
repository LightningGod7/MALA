import os
import json
import controller
import importlib.util #Dynamically load modules

###DECLARE
config_file_path = r".\configs\universal-configs.json"
modules_folder_path = r".\modules"

# #Load all modules into dictionary
# def module_load(modules_folder):
#     modules = []

#     #Search through module directory for all python files (modules)
#     for root, dirs, files in os.walk(modules_folder):
#         for file in files:
#             if file.endswith(".py"):
#                 module_path = os.path.join(root, file)
#                 modules.append(module_path)
#     return modules

def module_load(modules_folder):
    modules = {}

    # Search through module directory for all python files (modules)
    for root, dirs, files in os.walk(modules_folder):
        for file in files:
            if file.endswith(".py"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]

                # Load the module dynamically
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Retrieve module metadata
                module_data = {
                    'name': module.__name__,
                    'description': module.__description__
                }

                # Add module to the dictionary
                modules[module_name] = module_data

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
