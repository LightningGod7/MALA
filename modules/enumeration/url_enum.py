from modules.base_module import baseModule

class url_enum(baseModule):
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]

        #Always Required
        self.module_variables["mode"] = {"Value": "directory", "Description": "directory, range or subdomain", "Required":True}
        
        self.always_required = ["mode"]
        self.valid_modes = {"directory":["d","dir","directory"],"subdomain":["s", "sub", "subdomain"]}

        #Required only for range_fuzz
        self.module_variables["range"] = {"Value": "", "Description":"range of numbers to fuzz `xxx-yyy`. For when range mode is set", "Required":False}
        self.mode_required_dict = {"directory":[],"range": ["range"],"subdomain":[]}

        #Optional
        self.module_variables["extensions"] = {"Value":"", "Description":"e.g. .php, .html, .txt", "Required":False}
        self.module_variables["recursive"] = {"Value":"", "Description":"`i` for infinite", "Required":False}
        self.module_variables["filter"] = {"Value":"", "Description":"line(L), word(W), size(S), status(C) `set filter C:403,404;L:200;S:100` ", "Required":False}
        self.module_variables["username"] = {"Value": "", "Description":"auth enabled if both user and pass set", "Required":False}
        self.module_variables["password"] = {"Value": "", "Description":"auth enabled if both user and pass set", "Required":False}
        self.module_variables["cookie"] = {"Value": "", "Description":"cookie session authentication. Precedence over credentials auth", "Required":False}
    
        super().__init__(variables,self.always_required, self.valid_modes, self.mode_required_dict)

    def initialize_before_run(self,tools,variables):
        ### super constructor
        super().initialize_before_run(variables)

        self.gobuster = tools.get("gobuster")
        self.wfuzz = tools.get("wfuzz")
        self.ffuf = tools.get("ffuf")
        self.feroxbuster = tools.get("feroxbuster")

        # module_variables["output"]
        self.url = "http://" + self.target
        if self.port:
            self.url += ":" + str(self.port)
        if self.path:
            self.url += str(self.path) if str(self.path).startswith("/") else str(self.path)

    #MAIN SAUCE
    def get_command_list(self):
        if not self.target or not self.wordlist:
            print("Not all compulsory options are set. Check with `options` command")
            return       
        
        #Checking which mode to execute
        method = self.module_variables["mode"]["Value"]
        if method in self.valid_modes["directory"]:
            return self.directory_fuzz()
        elif method in self.valid_modes["subdomain"]:
            return self.subdomain_fuzz()
        else:
            print("Code should not reach here at all")
            return

    #Module functionalities
        
    #dir fuzz with feroxbuster
    def directory_fuzz(self):
        prefix = self.feroxbuster
        target_arg = "-u " + self.url
        wordlist_arg = "-w " + self.wordlist
        command_list = [prefix, target_arg, wordlist_arg]
        
        ##Add cases for recursive, authentication, extensions, diff types of output etc
        command_list += self.get_additional_options("fe","-c", "-x")
        return command_list
    
    def subdomain_fuzz(self):
        prefix = self.ffuf
        target_arg = "-u " + self.url
        host_arg = "'Host:FUZZ." + self.target + "'"
        wordlist_arg = "-w " + self.wordlist
        command_list = [prefix, target_arg, host_arg, wordlist_arg]
        
        ##Add cases for recursive, diff types of output etc
        return command_list

    def get_additional_options(self, tool_flag, cookie_flag, ext_flag=""):
        module_options = self.module_variables
        
        #Define all options
        filter_input = module_options["filter"]["Value"].split(";")
        username = module_options["username"]["Value"]
        password = module_options["password"]["Value"]
        cookie = module_options["cookie"]["Value"]

        extension_arg = ""
        
        #Directory fuzzing
        if tool_flag == "fe":
            #Check extensions flag
            extension_arg = ""
            if module_options["extensions"]["Value"]:
                extention_list = module_options["extensions"]["Value"].split(",")
                extensions = ['.' + ext if not ext.startswith('.') else ext for ext in extention_list]
                extension_arg = ext_flag + " " + ','.join(extensions)
        
        #Set auth flag to empty 1st
        auth_arg = ""

        #Check Auth flag
        if username and password:
            if tool_flag == "g":
                auth_arg = " -U " + username + " -P " + password
            else:
                auth_arg = "-b " + username + ":" + password
        
        #Check cookie flag
        if cookie:
            auth_arg = cookie_flag + " " + cookie

        #Set filter for ferox
        if tool_flag == "fe":
            filter_arg = ["", "", "", ""]
            if filter_input[0] != "":
                #Validate the input
                for filter in filter_input:
                    filter_type = filter.split(":")[0]
                    filter_metric = filter.split(":")[1]
                    if filter_type.lower() == "n":
                        line_filter = "-N " + filter_metric
                        filter_arg[0] = line_filter
                    elif filter_type.lower() == "w":
                        word_filter = "-W " + filter_metric
                        filter_arg[1] = word_filter
                    elif filter_type.lower() == "s":
                        size_filter = "-S " + filter_metric
                        filter_arg[2] = size_filter
                    elif filter_type.lower() == "c":
                        status_filter = "-C " + filter_metric
                        filter_arg[3] = status_filter

        #Set filter for ffuf
        if tool_flag == "f":
            filter_arg = ["", "", "", "-fc 404"]
            if filter_input[0] != "":
                #Validate the input
                for filter in filter_input:
                    filter_type = filter.split(":")[0]
                    filter_metric = filter.split(":")[1]
                    if filter_type.lower() == "l":
                        line_filter = "-fl " + filter_metric
                        filter_arg[0] = line_filter
                    elif filter_type.lower() == "w":
                        word_filter = "-fw " + filter_metric
                        filter_arg[1] = word_filter
                    elif filter_type.lower() == "s":
                        size_filter = "-fs " + filter_metric
                        filter_arg[2] = size_filter
                    elif filter_type.lower() == "c":
                        status_filter = "-fc " + filter_metric
                        filter_arg[3] = status_filter

        additional_options = filter_arg + [extension_arg,auth_arg]
        return [option for option in additional_options if option]

                
        



   