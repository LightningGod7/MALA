from modules.base_module import baseModule

class url_enum(baseModule):
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]

        #Always Required
        self.module_variables["mode"] = {"Value": "directory", "Description": "directory, range or subdomain", "Required":True}
        
        self.always_required = ["mode"]
        self.valid_modes = {"directory":["d","dir","directory"],"range": ["r", "ran", "range"],"subdomain":["s", "sub", "subdomain"]}

        #Required only for range_fuzz
        self.module_variables["range"] = {"Value": "", "Description":"range of numbers to fuzz `xxx-yyy`. For when range mode is set", "Required":False}
        self.mode_required_dict = {"directory":[],"range": ["range"],"subdomain":[]}

        #Optional
        self.module_variables["extensions"] = {"Value":"", "Description":"file extensions to fuzz (e.g. .php, .html, .txt)", "Required":False}
        self.module_variables["recursive"] = {"Value":"", "Description":"recursion in enumeration and depth. (`i` for infinite)", "Required":False}
        self.module_variables["filter"] = {"Value":"", "Description":"filter by `line, word, size, status:[metric]` split each filter with ',' e.g. status:404,line:7 (only can have 1 of each type of filter)", "Required":False}
        self.module_variables["username"] = {"Value": "", "Description":"auth mode will be enabled if both user and pass are set", "Required":False}
        self.module_variables["password"] = {"Value": "", "Description":"auth mode will be enabled if both user and pass are set", "Required":False}
        self.module_variables["cookie"] = {"Value": "", "Description":"cookie session authentication. Takes precedence over credentials auth", "Required":False}
    
        super().__init__(variables,self.always_required, self.valid_modes, self.mode_required_dict)

    def initialize_before_run(self,tools,variables):
        ### super constructor
        super().initialize_before_run(variables)

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
        if method in self.valid_modes["directory"]:
            return self.directory_fuzz()
        elif method in self.valid_modes["range"]:
            return self.range_fuzz()
        elif method in self.valid_modes["subdomain"]:
            return self.subdomain_fuzz()
        else:
            print("Code should not reach here at all")
            return

    #Module functionalities
    def directory_fuzz(self):
        prefix = self.gobuster + " dir"
        target_arg = "-u " + self.url
        wordlist_arg = "-w " + self.wordlist
        command_list = [prefix, target_arg, wordlist_arg]
        
        ##Add cases for recursive, authentication, extensions, diff types of output etc
        command_list += self.get_additional_options("g","-c", "-x")
        return command_list
    
    def range_fuzz(self):
        fuzz_range = self.module_variables["range"]["Value"]
        if not fuzz_range:
            print("Please supply range to fuzz for range fuzzing mode\n")
            return
        prefix = self.wfuzz
        range_arg = "-z range," + fuzz_range
        target_arg = "-u " + self.url + "/FUZZ"
        command_list = [prefix, range_arg, target_arg]

        ##Add cases for recursive, authentication, extensions, diff types of output etc
        command_list += self.get_additional_options("w","-b")

        return command_list
    
    def subdomain_fuzz(self):
        prefix = self.gobuster + " dns"
        target_arg = "-d " + self.target
        wordlist_arg = "-w " + self.wordlist
        command_list = [prefix, target_arg, wordlist_arg]
        
        ##Add cases for recursive, diff types of output etc
        return command_list

    def get_additional_options(self, tool_flag, cookie_flag, ext_flag=""):
        module_options = self.module_variables
        
        #Define all options
        recursive = module_options["recursive"]["Value"]
        filter_input = module_options["filter"]["Value"].split(",")
        username = module_options["username"]["Value"]
        password = module_options["password"]["Value"]
        cookie = module_options["cookie"]["Value"]

        extension_arg = ""
        if tool_flag == "g":
            #Check extensions flag
            extension_arg = ""
            if module_options["extensions"]["Value"]:
                extention_list = module_options["extensions"]["Value"].split(",")
                extensions = ['.' + ext if not ext.startswith('.') else ext for ext in extention_list]
                extension_arg = ext_flag + " " + ','.join(extensions)
                

        #Check recursive flag
        recursive_arg = ""
        if tool_flag == "g":
            if recursive == "i":
                recursive_arg = "-r"
            elif recursive:
                recursive_arg = "-r --depth " + recursive
        elif tool_flag == "w":
            if recursive == "i":
                recursive_arg = "-R" + "100"
            elif recursive:
                recursive_arg = "-R" + recursive

        

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

        #If not using wfuzz then no need for filter input checks
        if tool_flag != "w":
            additional_options = [extension_arg,recursive_arg,auth_arg]
            return [option for option in additional_options if option]

        #set defualt to filter 404
        filter_arg = ["", "", "", "--hc 404"]
        if filter_input[0] != "":
            #Validate the input
            for filter in filter_input:
                filter_type = filter.split(":")[0]
                filter_metric = filter.split(":")[1]
                if filter_type.lower() == "line":
                    line_filter = "--hl " + filter_metric
                    filter_arg[0] = line_filter
                elif filter_type.lower() == "word":
                    word_filter = "--hw " + filter_metric
                    filter_arg[1] = word_filter
                elif filter_type.lower() == "chars":
                    size_filter = "--hh " + filter_metric
                    filter_arg[2] = size_filter
                elif filter_type.lower() == "status":
                    status_filter = "--hc " + filter_metric
                    filter_arg[3] = status_filter


        additional_options = filter_arg + [extension_arg,recursive_arg,auth_arg]
        return [option for option in additional_options if option]

                
        



   