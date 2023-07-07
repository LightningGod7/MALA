class baseModule:
    def __init__(self,mode_dict = {}):
        # self.variables = variables
        self.mode_dict = mode_dict
    def validate_input(self, option, value):
        if option not in self.module_variables:
            print(f"Option {option} does not exist to be set. Check available options with the command `variables`")
            return False
        if option == "mode":
            return self.initialize_selected_mode(value)
        else:
            return self.basic_validation(option, value)
    
    def basic_validation(self, option, value):
        if option == "port":
            return self.is_valid_port(value)
        
    def initialize_selected_mode(self, mode_input):
        ### Check mode
        for mode, mode_pattern in self.mode_dict.items():
            if mode_input in mode_pattern:
                print(f"Setting mode to {mode}")
                self.required_mode_options()
                return mode
        print(f"{mode_input} is not a valid mode. Check available modes with command `variables`")
        return None

    def required_mode_options(self):
        return

    def get_command_list(self):
        return
    
    def initialize_before_run(self,variables):
        ### GET common variables
        self.variables = variables
        common_vars = variables.get("common_variables")
        self.target = common_vars["RHOST"]["Value"]
        self.port = common_vars["RPORT"]["Value"]
        self.wordlist = common_vars["wordlist"]["Value"]
        # module_variables["output"]
    #MAIN SAUCE

    def is_valid_port(self, port):
        try:
            port = int(port)
            return port >= 0 and port <= 65535
        except ValueError:
            print("Invalid port number")
            return False
