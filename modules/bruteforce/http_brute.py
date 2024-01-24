import time
from modules.base_module import baseModule

class http_bruteforce(baseModule):
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]

        ##ALWAYS REQUIRED
        self.module_variables["username"] = {"Value": "admin", "Description": "username (precedence over list)", "Required": True}
        self.module_variables["userlist"] = {"Value":"", "Description":"username list", "Required":True}
        self.module_variables["password"] = {"Value":"", "Description":"password (precedence over list)", "Required":True}
        self.module_variables["passlist"] = {"Value": "/wls/rockyou.txt", "Description":"password list", "Required":False}
        
        self.module_variables["mode"] = {"Value": "basic", "Description":"basic | get | post", "Required":True}

        self.always_required = ["mode","username","userlist","password","passlist"]
        self.valid_modes = {"http basic":["b", "basic", "d", "digest"],"http-get-form":["g", "get"],"http-post-form":["p", "post"]}

        ##Required only for http-get and http-post
        self.module_variables["error-pattern"] = {"Value": "Incorrect", "Description":"identify error", "Required":False}
        self.module_variables["urlpath"] = {"Value": "", "Description":"url path to form", "Required":False}
        self.module_variables["userfield"] = {"Value": "username", "Description":"username field", "Required":True}       
        self.module_variables["passfield"] = {"Value": "pass", "Description":"password field", "Required":False}

        self.mode_required_dict = {"http basic":[],"http-get-form":["error-pattern","urlpath","userfield","passfield"],"http-post-form":["error-pattern","urlpath","userfield","passfield"]}

        ##Optional
        self.module_variables["cookie"] = {"Value": "", "Description":"cookie", "Required":False}
        self.module_variables["threads"] = {"Value": "", "Description":"", "Required":False}
        self.module_variables["verbose"] = {"Value": "", "Description":"verbose output", "Required":False}
        #add b64 encoding option
        self.module_variables["base64"] = {"Value": "", "Description":"b64 encode creds [u/p/up]", "Required":False}
        self.module_variables["ignore-restore"] = {"Value": "True", "Description":"Ignore restore file \n(clear to unset)", "Required":False}
        self.module_variables["stop-on-found"] = {"Value": "True", "Description":"stop when cred found \n(clear to unset)", "Required":False}

        super().__init__(variables, self.always_required, self.valid_modes, self.mode_required_dict)

    #Override the abstract class to set tool
    def initialize_before_run(self, tools, variables):
        super().initialize_before_run(variables)
        self.hydra = tools.get("hydra")

    def get_command_list(self):
        #Check that required options are set
        self.username = self.module_variables["username"]["Value"]
        self.userlist = self.module_variables["userlist"]["Value"]
        self.password = self.module_variables["password"]["Value"]
        self.passlist = self.module_variables["passlist"]["Value"]

        if not (self.username or self.userlist) or not (self.password or self.passlist) or not self.target:
            print("You need to set either static credentials or wordlists to use this mode. Run command `variables` to see required options\n")
            return


        #Checking which mode to execute
        prefix = self.hydra
        if self.username and self.userlist:
            print("Both username and userlist has been set. Using username\n")
        if self.password and self.passlist:
            print("Both password and passlist has been set. Using password\n")  
        time.sleep(1)      
        user_arg = "-l " + self.username if self.username else "-L " + self.userlist
        pass_arg = "-p " + self.password if self.password else "-P " + self.passlist
        method = self.module_variables["mode"]["Value"]
        if method in self.valid_modes["http basic"]:
            return self.basic_brute(prefix,user_arg,pass_arg)
        elif method in self.valid_modes["http-get-form"]:
            return self.get_brute(prefix,user_arg,pass_arg)
        elif method in self.valid_modes["http-post-form"]:
            return self.post_brute(prefix,user_arg,pass_arg)
        else:
            print("Code should not reach here at all")
            return
    
    def basic_brute(self,prefix,user_arg,pass_arg):
        target_arg = self.target
        mode_arg = "http-get"
        command_list = [prefix, user_arg, pass_arg, target_arg, mode_arg]
        command_list.append(self.module_variables["urlpath"]["Value"]) if self.module_variables["urlpath"]["Value"] else None
        additional_options = self.get_additional_options()
        command_list = command_list[:3] + additional_options + command_list[3:]
        return command_list

    def get_brute(self,prefix,user_arg,pass_arg):
        #Set some options to `required`
        target_arg = self.target
        mode_arg = "http-get-form"
        get_arg = self.create_mode_arg_input()
        command_list = [prefix, user_arg, pass_arg, target_arg, mode_arg, get_arg]
        additional_options = self.get_additional_options()
        command_list = command_list[:3] + additional_options + command_list[3:]
        return command_list
    
    def post_brute(self,prefix,user_arg,pass_arg):
        target_arg = self.target
        mode_arg = "http-post-form"
        post_arg = self.create_mode_arg_input()
        
        command_list = [prefix, user_arg, pass_arg, target_arg, mode_arg, post_arg]
        additional_options = self.get_additional_options()
        command_list = command_list[:3] + additional_options + command_list[3:]
        return command_list
        
    def create_mode_arg_input(self):
        urlformaction = self.module_variables["urlpath"]["Value"]

        #Check credential encoding
        if not self.module_variables["base64"]["Value"]:
            username_field = self.module_variables["userfield"]["Value"] + "=^USER^"
            password_field = self.module_variables["passfield"]["Value"] + "=^PASS^"
        elif self.module_variables["userfield"]["Value"] == "up":
            username_field = self.module_variables["userfield"]["Value"] + "=^USER64^"
            password_field = self.module_variables["passfield"]["Value"] + "=^PASS64^"
        elif self.module_variables["userfield"]["Value"] == "u":
            username_field = self.module_variables["userfield"]["Value"] + "=^USER64^"
            password_field = self.module_variables["passfield"]["Value"] + "=^PASS^"
        elif self.module_variables["userfield"]["Value"] == "p":
            username_field = self.module_variables["userfield"]["Value"] + "=^USER^"
            password_field = self.module_variables["passfield"]["Value"] + "=^PASS64^"
        else:
            print("Invalid base64 input. Enter `u` for username, `p` for password pr `up` for both")
            return

        credential_field = username_field + "&" + password_field
        error_field = "F=" + self.module_variables["error-pattern"]["Value"]
        mode_arg_input = urlformaction + ":" + credential_field + ":" + error_field

        #Optional cookie field
        if self.module_variables["cookie"]["Value"]:
            cookie_field = ":H=Cookie: " + self.module_variables["cookie"]["Value"]
            mode_arg_input += cookie_field
    
        return '"' + mode_arg_input + '"'
    
    def get_additional_options(self):
        #Define all options
        port = self.port
        threads = self.module_variables["threads"]["Value"]
        port_arg = "-s " + str(port) if port else None
        threads_arg = "-t " + threads if threads else None
        verbose_arg = "-V"

        #Feature add ignore restore and stop on found
        ignore_arg = "-I" if self.module_variables["ignore-restore"]["Value"] else None
        stop_arg = "-f" if self.module_variables["stop-on-found"]["Value"] else None

        additional_options = [ignore_arg,stop_arg,verbose_arg,port_arg,threads_arg]
        return [option for option in additional_options if option]