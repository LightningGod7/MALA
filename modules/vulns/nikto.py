import os
import re 
from prettytable import PrettyTable

from modules.base_module import baseModule

class nikto(baseModule):
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]
        self.module_variables["mode"] = {"Value": "scan", "Description": "scan or show tuning and mutate options", "Required":True}
        ##ALWAYS REQUIRED
        self.always_required = ["mode"]
        self.valid_modes = {"scan":["scan"],"show options": ["show", "show options"]}
        ##Optional
        self.module_variables["username"] = {"Value": "", "Description":"Username for host based authentication ", "Required":False}
        self.module_variables["password"] = {"Value": "", "Description":"Password for host based authentication", "Required":False}
        self.module_variables["tuning"] = {"Value": "", "Description":"Scan Tuning", "Required":False}
        self.module_variables["mutate"] = {"Value": "", "Description":"Guess additional file names (Depracated but still usable)", "Required":False}
        # self.module_variables["plugins"] = {"Value": "", "Description":"List of plugins to run", "Required":False}
        self.module_variables["ssl"] = {"Value": "", "Description":"scan ssl vulns", "Required":False}

        self.tuning_options = {
                            '1': 'Interesting File / Seen in logs',
                            '2': 'Misconfiguration / Default File',
                            '3': 'Information Disclosure',
                            '4': 'Injection (XSS/Script/HTML)',
                            '5': 'Remote File Retrieval - Inside Web Root',
                            '6': 'Denial of Service',
                            '7': 'Remote File Retrieval - Server Wide',
                            '8': 'Command Execution / Remote Shell',
                            '9': 'SQL Injection',
                            '0': 'File Upload',
                            'a': 'Authentication Bypass',
                            'b': 'Software Identification',
                            'c': 'Remote Source Inclusion',
                            'x': 'Reverse Tuning Options (include all except specified)'
                        }

        self.mutate_options = {
                            '1': 'Test all files with all root directories',
                            '2': 'Guess for password file names',
                            '3': 'Enumerate user names via Apache (/~user type requests)',
                            '4': 'Enumerate user names via cgiwrap (/cgi-bin/cgiwrap/~user type requests)',
                            '5': 'Attempt to brute force sub-domain names, assume that the host name is the parent domain',
                            '6': 'Attempt to guess directory names from the supplied dictionary file'
                        }

        super().__init__(variables, self.always_required, self.valid_modes)

    #Override the abstract class to set tool
    def initialize_before_run(self, tools, variables):
        super().initialize_before_run(variables)
        self.nikto = tools.get("nikto")

    def get_command_list(self):
        #Check that required options are set
        method = self.module_variables["mode"]["Value"]

        if not self.target and method not in self.valid_modes["scan"]:
            print("Target is not set, nothing to scan")
            return  
        elif method in self.valid_modes["show options"]:
            self.show_options()
            return ["echo"]
        
        prefix = self.nikto
        target_arg = "-h " + self.target
        command_list = [prefix,target_arg]
        additional_options = self.get_additional_options()
        if additional_options == "Invalid input":
            return "Handled"
        command_list += additional_options.append("-nointeractive")
        return command_list

    def get_additional_options(self):
        username = self.module_variables["username"]["Value"]
        password = self.module_variables["password"]["Value"]
        tuning = self.module_variables["tuning"]["Value"]
        tuning_pattern = r"^(x\s*(?:\d|[a-c])+|\d+|[a-c]+)$"
        mutate = self.module_variables["mutate"]["Value"]
        mutate_pattern = r"^[1-6]{1,6}$"
        # plugins = self.module_variables["Plugins"]["Value"]
        ssl = self.module_variables["ssl"]["Value"]

        #Check for port
        port_arg = None if self.port == 80 or self.port == None else ("-p " + str(self.port)) 

        #Check for authentication
        auth_arg = ("-id " + f'"{username}:{password}"') if username or password else None

        #Validate tuning input
        if tuning and re.match(tuning_pattern, tuning):
            tuning_arg = "-Tuning " + tuning
        elif tuning:
            print("Invalid tuning option")
            return "Invalid input"
        else:
            tuning_arg = None
        
        #Validate mutate input
        if mutate and re.match(mutate_pattern, mutate):
            mutate_arg = "-mutate " + mutate
        elif mutate:
            print("Invalid mutate option")
            return "Invalid input"
        else:
            mutate_arg = None

        #Check for ssl
        ssl_arg = "-ssl" if ssl else None

        additional_options = [port_arg, auth_arg, tuning_arg, mutate_arg, ssl_arg]
        return [option for option in additional_options if option]

    def show_options(self):
        print("\n --Tuning options--")  
        self.tuning_table = PrettyTable()
        self.tuning_table.field_names = ["Option", "Description"]
        self.tuning_table.max_table_width=120
        for option, description in self.tuning_options.items():
            self.tuning_table.add_row([option, description])
        print(self.tuning_table)
        print("\nExample 1: 90a - Scans for SQL Injection, File Uploads and Authentication Bypass")
        print("Example 2: x a - Scans everything except Authentication Bypass")
        print("\n --Mutate options--")    
        self.mutate_table = PrettyTable()
        self.mutate_table.field_names = ["Option", "Description"]
        self.mutate_table.max_table_width=120
        for option, description in self.mutate_options.items():
            self.mutate_table.add_row([option, description])
        print(self.mutate_table)
        print("Example 1: 123 - Test all files with all root directories, Guess for password file names and Enumerate user names via Apache")
        return "Handled"
