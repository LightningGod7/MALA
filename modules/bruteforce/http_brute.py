import time
from modules.base_module import baseModule

class http_bruteforce(baseModule):
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]

        ##ALWAYS REQUIRED
        self.module_variables["username"] = {"Value": "admin", "Description": "single username (takes precedence over userlist)", "Required": True}
        self.module_variables["userlist"] = {"Value":"", "Description":"username list", "Required":True}
        self.module_variables["password"] = {"Value":"password", "Description":"single password (takes precedence over passlist)", "Required":True}
        self.module_variables["passlist"] = {"Value": "", "Description":"password list", "Required":False}
        
        self.module_variables["mode"] = {"Value": "basic", "Description":"basic auth | http get | http post", "Required":True}

        self.always_required = ["mode","username","userlist","password","passlist"]
        self.valid_modes = {"http basic":["b", "basic", "d", "digest"],"http-get-form":["g", "get"],"http-post-form":["p", "post"]}

        ##Required only for http-get and http-post
        self.module_variables["error-pattern"] = {"Value": "invalid", "Description":"error pattern to match on failed attempt", "Required":False}
        self.module_variables["urlpath"] = {"Value": "/066/login.php", "Description":"url path to the login form on the target e.g. /", "Required":False}
        self.module_variables["userfield"] = {"Value": "username", "Description":"username html field", "Required":True}       
        self.module_variables["passfield"] = {"Value": "pass", "Description":"password html field", "Required":False}

        self.mode_required_dict = {"http basic":[],"http-get-form":["error-pattern","urlpath","userfield","passfield"],"http-post-form":["error-pattern","urlpath","userfield","passfield"]}

        ##Optional
        self.module_variables["cookie"] = {"Value": "", "Description":"cookie for session authentication", "Required":False}
        self.module_variables["threads"] = {"Value": "", "Description":"number of threads to use", "Required":False}
        self.module_variables["verbose"] = {"Value": "", "Description":"verbose output", "Required":False}

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
        command_list += self.check_additional_options()
        return command_list

    def get_brute(self,prefix,user_arg,pass_arg):
        #Set some options to `required`
        target_arg = self.target
        mode_arg = "http-get-form"
        get_arg = self.create_mode_arg_input()
        command_list = [prefix, user_arg, pass_arg, target_arg, mode_arg, get_arg]
        command_list += self.check_additional_options()
        return command_list
    
    def post_brute(self,prefix,user_arg,pass_arg):
        target_arg = self.target
        mode_arg = "http-post-form"
        post_arg = self.create_mode_arg_input()
        command_list = [prefix, user_arg, pass_arg, target_arg, mode_arg, post_arg]
        command_list += self.check_additional_options()
        return command_list
        
    def create_mode_arg_input(self):
        urlformaction = self.module_variables["urlpath"]["Value"]
        username_field = self.module_variables["userfield"]["Value"] + "=^USER^"
        password_field = self.module_variables["passfield"]["Value"] + "=^PASS^"
        credential_field = username_field + "&" + password_field
        error_field = self.module_variables["error-pattern"]["Value"]
        mode_arg_input = urlformaction + ":" + credential_field + ":" + error_field

        #Optional cookie field
        if self.module_variables["cookie"]["Value"]:
            cookie_field = ":H=Cookie: " + self.module_variables["cookie"]["Value"]
            mode_arg_input += cookie_field
    
        return '"' + mode_arg_input + '"'
    
    def check_additional_options(self):
        #Define all options
        port = self.port
        threads = self.module_variables["threads"]["Value"]
        port_arg = "-s " + str(port) if port else None
        threads_arg = "-t " + threads if threads else None
        verbose_arg = "-V"
        additional_options = [port_arg,threads_arg,verbose_arg]
        return [option for option in additional_options if option]