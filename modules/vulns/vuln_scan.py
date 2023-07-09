from modules.base_module import baseModule

class vulnScan(baseModule):
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]

        ##ALWAYS REQUIRED
        self.module_variables["mode"] = {"Value": "admin", "Description": "nmap script to use", "Required": True}

        ##Optional
        self.module_variables["cookie"] = {"Value": "", "Description":"cookie for session authentication", "Required":False}
        self.module_variables["threads"] = {"Value": "", "Description":"number of threads to use", "Required":False}
        self.module_variables["verbose"] = {"Value": "", "Description":"verbose output", "Required":False}

        super().__init__(variables, self.always_required, self.valid_modes, self.mode_required_dict)

    #Override the abstract class to set tool
    def initialize_before_run(self, tools, variables):
        super().initialize_before_run(variables)
        self.hydra = tools.get("nmap")

    def get_command_list(self):
        #Check that required options are set
        if not self.target:
            print("Target is not set")
            return  
     
        user_arg = "-l " + self.username if self.username else "-L " + self.userlist
        pass_arg = "-p " + self.password if self.password else "-P " + self.passlist
        method = self.module_variables["mode"]["Value"]
        if method:
            script_arg = method
        else:
            print("SHOW ALL SCRIPT OPTIONS HERE")
            return

    nmap_variables = {"script": [], "args":""}

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

    def build_nmap_command(target, port, script_options, script_args=None):
        command = ['nmap', '-p', port, '-sV', '--script', script_options, target]
        
        if script_args:
            command.extend(['--script-args', script_args])
        
        return command

    def nmap_script_option(option):
        if not nmap_variables["args"]:
            if any(script in scripts_withargs for script in option):
                print("Script selected requires arguments but none were given.")
                return
        script_options = ','.join(option)
        return script_options


