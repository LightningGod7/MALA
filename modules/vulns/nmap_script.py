from modules.base_module import baseModule

class vulnScan(baseModule):
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]

        ##ALWAYS REQUIRED
        self.module_variables["mode"] = {"Value": "admin", "Description": "nmap script to use", "Required": True}
        self.always_required = ["mode"]
        ##Optional
        self.module_variables["mode args"] = {"Value": "", "Description":"arguments for the provided script", "Required":False}

        super().__init__(variables, self.always_required)

    #Override the abstract class to set tool
    def initialize_before_run(self, tools, variables):
        super().initialize_before_run(variables)
        self.nmap = tools.get("nmap")

    def get_command_list(self):
        #Check that required options are set
        if not self.target:
            print("Target is not set")
            return  
    
        mode = self.module_variables["mode"]["Value"]
        mode_arguments = self.module_variables["mode args"]["Value"]
        if mode:
            return self.command_builder(mode, mode_arguments)
        else:
            print("SHOW ALL SCRIPT OPTIONS HERE")
            return

    def command_builder(self, mode, mode_arguments=None):
        prefix = self.nmap
        port_arg = ("-p " + str(self.port)) if self.port else "80"
        script_arg = "--script " + mode
        target_arg = self.target

        command_list = [prefix, port_arg, script_arg, target_arg]

        if mode_arguments:
            command_list += mode_arguments

        return command_list

    # def nmap_script_option(option):
    #     if not nmap_variables["args"]:
    #         if any(script in scripts_withargs for script in option):
    #             print("Script selected requires arguments but none were given.")
    #             return
    #     script_options = ','.join(option)
    #     return script_options


    # nmap_variables = {"script": [], "args":""}

    # scripts_noargs = {
    #     "backup-config-enum": "http-config-backup",
    #     "drupal-users-enum": "http-drupal-enum-users",
    #     "drupal-enum": "http-drupal-enum",
    #     "enum": "http-enum",
    #     "waf-detect": "http-waf-detect",
    #     "webdav-scan": "http-webdav-scan",
    #     "wordpress-users": "http-wordpress-users"
    # }

    # scripts_withargs = {
    #     "uploads-exploit": "http-fileupload-exploiter",
    #     "form-brute": "http-form-brute",
    #     "form-fuzz": "http-form-fuzzer",
    #     "waf-fingerprint": "http-waf-fingerprint",
    #     "joomla-brute": "http-joomla-brute",
    #     "phpmyadmin-dir-traversal": "http-phpmyadmin-dir-traversal",
    #     "wordpress-brute": "http-wordpress-brute",
    #     "wordpress-enum": "http-wordpress-enum"
    # }

    # script_options = ""