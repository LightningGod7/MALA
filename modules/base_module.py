class baseModule:
    def __init__(self,variables,always_required,mode_dict = {},mode_required_dict= {}):
        # self.variables = variables
        self.module_variables = variables["module_variables"]
        self.always_required_options = always_required
        self.mode_dict = mode_dict
        self.mode_required_dict = mode_required_dict

    ###Handling Inputs
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
        
        return True
        
    ###Initializing mode options
    def initialize_selected_mode(self, mode_input):
        ### If no mode checking then just continue
        if not len(self.mode_dict):
            return mode_input
        
        ### Check mode
        for mode, mode_pattern in self.mode_dict.items():
            if mode_input in mode_pattern:
                self.required_mode_options(mode)
                return mode
        print(f"{mode_input} is not a valid mode. Check available modes with command `variables`")
        return None

    def required_mode_options(self, current_mode):
        #Reset all required options 1st
        always_required_set = set(self.always_required_options)
        for option, option_values in self.module_variables.items():
            option_values["Required"] = option in always_required_set

        #Set mode required options
        for options in self.mode_required_dict[current_mode]:
            self.module_variables[options]["Required"] = True
        return

    ###Initializing for command execution
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



    ###Various input value checks
    def is_valid_port(self, port):
        try:
            port = int(port)
            return port >= 0 and port <= 65535
        except ValueError:
            print("Invalid port number")
            return False
