class url_enumeration:
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]
        self.module_variables["mode"] = {"Value": " ", "Description": "directory or range"}
        self.module_variables["extensions"] = {"Value":"", "Description":"file extensions to fuzz (e.g. .php, .html, .txt)"}
        self.module_variables["recursive"] = {"Value":0, "Description":"recursion in enumeration and depth. (-1 for infinite)"}
        self.module_variables["username"] = {"Value": "", "Description":"auth mode will be enabled if both user and pass are set"}
        self.module_variables["password"] = {"Value": "", "Description":"auth mode will be enabled if both user and pass are set"}
        self.module_variables["cookie"] = {"Value": "", "Description":"cookie session authentication. Takes precedence over credentials auth"}
        self.module_variables["range"] = {"Value": "", "Description":"range of numbers to fuzz `xxx-yyy`. For when range mode is set"}

    def initialize_before_run(self,tools,variables):
        ### GET common variables
        self.variables = variables
        common_vars = variables.get("common_variables")
        self.target = common_vars["RHOST"]["Value"]
        self.port = common_vars["RPORT"]["Value"]
        self.wordlist = common_vars["wordlist"]["Value"]
        self.gobuster = tools.get("gobuster")
        self.wfuzz = tools.get("wfuzz")

        # module_variables["output"]
        self.url = "http://" + self.target
        if self.port:
            self.url += ":" + str(self.port)

    #MAIN SAUCE
    def get_command_list(self):
        if not self.target or not self.wordlist:
            print("Not all compulsory options are set. Check with `options` command")
            return       
        #Checking which mode to execute
        method = self.module_variables["mode"]["Value"]
        directory_match = ["d","dir","directory"]
        range_match = ["r", "ran", "range"]
        if method in directory_match:
            return self.directory_fuzz()
        elif method in range_match:
            return self.range_fuzz()
        else:
            print("Unknown mode. Please set mode to `directory` or `range`")
            return


    #Module functionalities
    def directory_fuzz(self):
        prefix = self.gobuster + " dir"
        target_arg = "-u " + self.url
        wordlist_arg = "-w " + self.wordlist
        command_list = [prefix, target_arg, wordlist_arg]
        
        ##Add cases for recursive, authentication, extensions, diff types of output etc
        command_list += self.check_additional_options("-x", "-c","g")
        return command_list
    
    def range_fuzz(self):
        if not fuzz_range:
            print("Please supply range to fuzz for range fuzzing mode")
            return
        fuzz_range = self.module_variables["range"]["Value"]
        prefix = self.wfuzz
        range_arg = "-z range," + fuzz_range
        target_arg = "-u " + self.url
        command_list = [prefix, range_arg, target_arg]

        ##Add cases for recursive, authentication, extensions, diff types of output etc
        command_list += self.check_additional_options("-e", "-cookies","r")
        return command_list
    
    def subdomain_fuzz(self):
        prefix = self.gobuster + " dns"
        target_arg = "-d " + self.target
        wordlist_arg = "-w " + self.wordlist
        command_list = [prefix, target_arg, wordlist_arg]
        
        ##Add cases for recursive, authentication, extensions, diff types of output etc
        return command_list

    def check_additional_options(self, ext_flag, cookie_flag, cred_flag):
        module_options = self.module_variables
        
        #Define all options
        extentions = []
        recursive = module_options["recursive"]["Value"]
        username = module_options["username"]["Value"]
        password = module_options["password"]["Value"]
        cookie = module_options["cookie"]["Value"]
        extension_arg = ""
        recursive_arg = ""
        auth_arg = ""

        #Check extentions option
        if len(module_options["extensions"]["Value"]):
            #Check that all extentions are prepended with '.'
            extensions = ['.' + ext if not ext.startswith('.') else ext for ext in module_options["extensions"]["Value"]]
            extension_arg = ext_flag + " " + ''.join(extentions)

        #Check recursive flag
        if recursive=="i":
            recursive_arg = "-r"
        elif recursive:
            recursive_arg = "-r --depth " + recursive
        
        #Check Auth flag
        if username and password:
            if cred_flag == "g":
                auth_arg = " -U " + username + " -P " + password
            else:
                auth_arg = username + ":" + password
        
        if cookie:
            auth_arg = cookie_flag + " " + cookie
        
        additional_options = [extension_arg,recursive_arg,auth_arg]
        return additional_options


   