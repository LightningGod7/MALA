class http_bruteforce:
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]
        self.module_variables["username"] = {"Value": "adam", "Description": "single username"}
        self.module_variables["userlist"] = {"Value":"", "Description":"username list"}
        self.module_variables["userfield"] = {"Value": "user", "Description":"username html field"}
        self.module_variables["password"] = {"Value":"123", "Description":"single password"}
        self.module_variables["passlist"] = {"Value": "", "Description":"password list"}
        self.module_variables["passfield"] = {"Value": "pass", "Description":"password html field"}
        self.module_variables["port"] = {"Value": "", "Description":"target port"}
        self.module_variables["urlpath"] = {"Value": "/admin/login.php", "Description":"url path to the login form on the target e.g. /"}
        self.module_variables["mode"] = {"Value": "get", "Description":"basic auth `basic` | http get `get` | http post `post`"}
        self.module_variables["error-pattern"] = {"Value": "invalid", "Description":"error pattern to match on failed attempt"}
        self.module_variables["cookie"] = {"Value": "", "Description":"cookie session authentication"}
        self.module_variables["threads"] = {"Value": "", "Description":"number of threads to use"}

    def initialize_before_run(self,tools,variables):
        ### GET common variables
        self.variables = variables
        common_vars = variables.get("common_variables")
        self.target = common_vars["RHOST"]["Value"]
        self.port = common_vars["RPORT"]["Value"]
        self.wordlist = common_vars["wordlist"]["Value"]
        self.hydra = tools["hydra"]
        # module_variables["output"]

    #MAIN SAUCE
    def get_command_list(self):
        #Checking which mode to execute
        self.username = self.module_variables["username"]["Value"]
        self.userlist = self.module_variables["userlist"]["Value"]
        self.password = self.module_variables["password"]["Value"]
        self.passlist = self.module_variables["passlist"]["Value"]

        if not (self.username or self.userlist) or not (self.password or self.passlist) or not self.target:
            return

        prefix = self.hydra
        user_arg = "-l " + self.username if self.username else "-L " + self.userlist
        pass_arg = "-p " + self.password if self.password else "-P " + self.passlist
        method = self.module_variables["mode"]["Value"]
        basic_match = ["basic"]
        get_match = ["get"]
        post_match = ["post"]
        if method in basic_match:
            return self.basic_brute(prefix,user_arg,pass_arg)
        elif method in get_match:
            return self.get_brute(prefix,user_arg,pass_arg)
        elif method in post_match:
            return self.post_brute(prefix,user_arg,pass_arg)
        else:
            print("Unknown mode. Please set mode to `directory` or `range`")
            return
    
    def basic_brute(self,prefix,user_arg,pass_arg):
        target_arg = self.target
        verbose_arg = "-V"
        command_list = [prefix, user_arg, pass_arg, verbose_arg, target_arg]
        command_list.extend(self.module_variables["urlpath"]["Value"]) if self.module_variables["urlpath"]["Value"] else None
        return command_list

    def get_brute(self,prefix,user_arg,pass_arg):
        target_arg = self.target
        verbose_arg = "-V"
        mode_arg = "http-get-form"
        get_arg = self.create_mode_arg_input()
        command_list = [prefix, user_arg, pass_arg, verbose_arg, target_arg, mode_arg, get_arg]
        return command_list
    
    def post_brute(self,prefix,user_arg,pass_arg):
        target_arg = self.target
        verbose_arg = "-V"
        mode_arg = "http-post-form"
        post_arg = self.create_mode_arg_input()
        command_list = [prefix, user_arg, pass_arg, verbose_arg, target_arg, mode_arg, post_arg]
        return command_list
        
    def create_mode_arg_input(self):
        urlformaction = self.module_variables["urlpath"]["Value"]
        username_field = self.module_variables["userfield"]["Value"] + "=^USER^"
        password_field = self.module_variables["passfield"]["Value"] + "=^PASS^"
        credential_field = username_field + "&" + password_field
        error_field = self.module_variables["error-pattern"]["Value"]
        mode_arg_input = "'" + urlformaction + ":" + credential_field + ":" + error_field + "'"
        return mode_arg_input
    
    def check_additional_options():

        additional_options = []
        return additional_options