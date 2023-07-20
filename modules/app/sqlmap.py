from modules.base_module import baseModule

class sql_enum(baseModule):
    def __init__(self, variables):
        self.module_variables = variables["module_variables"]

        #Always required
        self.module_variables["mode"] = {"Value": " ", "Description": "Request or URL", "Required": True}
        self.always_required = ["mode"]
        self.valid_modes = {"request":["r","req","request"],"url": ["u", "url"]}

        #Required only for request mode
        self.module_variables["request_file"] = {"Value":" ", "Description":"Path to the request file", "Required": False}
        self.mode_required_dict = {"request":["request_file"],"url": []}
        super().__init__(variables, self.always_required, self.valid_modes,self.mode_required_dict)

    def initialize_before_run(self,tools,variables):
        super().initialize_before_run(variables)
        self.sqlmap = tools.get("sqlmap")
        self.url = "http://" + self.target
        if self.port:
            self.url += ":" + str(self.port)
        self.whatweb = tools.get("whatweb")

    def test(self):
        print("Imported this module")
        print(self.target)
        print(self.whatweb)

    def get_command_list(self):
        #Checking which mode to execute
        method = self.module_variables["mode"]["Value"]
        request_match = ["r","req","request"]
        url_match = ["u", "url"]
        if method in request_match:
            return self.request_sql()
        elif method in url_match:
            return self.url_sql()
        else:
            print("Unknown mode. Please set mode to `request` or `url`")
            return

    def request_sql(self):
        module_options = self.module_variables
        file = module_options["request_file"]["Value"]
        if file == " ":
            print("Not all compulsory options are set. Check with `options` command")
            return
        prefix = self.sqlmap
        target_arg = "-r " + file
        args = "--batch --banner --current-user --current-db --is-dba --dump"
        command_list = [prefix, target_arg, args]
        print(command_list)
        if None in command_list:
            print("Not all compulsory options are set. Check with `options` command")
            return
        else:
            return command_list
    
    def url_sql(self):
        if not self.target:
            print("Not all compulsory options are set. Check with `options` command")
            return 
        prefix = self.sqlmap
        target_arg = "-u " + self.url
        args = "--batch --banner --current-user --current-db --is-dba --dump"
        command_list = [prefix, target_arg, args]
        if None in command_list:
            print("Not all compulsory options are set. Check with `options` command")
            return
        else:
            return command_list