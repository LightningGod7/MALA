class waf_fingerprint:
    def __init__(self, tools, variables):

        ### Get Common Variables
        self.variables = variables
        common_vars = variables.get("common_variables")
        self.target = common_vars["RHOST"]["Value"]
        self.port = common_vars["RPORT"]["Value"]
        self.wafw00f = tools.get("wafw00f")

        # module_variables["output"]
        self.url = "http://" + self.target
        if self.port:
            self.url += ":" + str(self.port)

    def test(self):
        print("Imported this module")
        print(self.target)
        print(self.port)
        print(self.wafw00f)

    def get_command_list(self):
        return self.waf_fingerprint()

    def waf_fingerprint(self):
        if not self.target:
            print("Not all compulsory options are set. Check with `options` command")
            return
        
        prefix = self.wafw00f
        target_arg = "-a " + self.url
        command_list = [prefix, target_arg]
        return command_list