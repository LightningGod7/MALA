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
