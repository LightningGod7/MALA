from modules.base_module import baseModule

class portscan(baseModule):
    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]

        #Always Required
        self.module_variables["mode"] = {"Value": "tcp-all", "Description": "quick scan on all tcp ports", "Required":True}

        self.always_required = ["mode"]
        self.valid_modes = {"tcp-all":["t","tcp","tcp-all"],"udp":["udp", "u"],"aggressive":["agg"]}
 
        self.module_variables["ports"] = {"Value":"", "Description":"ports `21,22,23`", "Required":False}
    
        super().__init__(variables,self.always_required, self.valid_modes)

    def initialize_before_run(self,tools,variables):
        ### super constructor
        super().initialize_before_run(variables)

        self.nmap = tools.get("nmap")
        self.nmapAutomator = tools.get("nmapAutomator")
        self.autorecon = tools.get("autorecon")
        self.rustscan = tools.get("rustscan")

    #MAIN SAUCE
    def get_command_list(self):
        if not self.target:
            print("Not all compulsory options are set. Check with `options` command")
            return       
        
        #Checking which mode to execute
        method = self.module_variables["mode"]["Value"]
        if method in self.valid_modes["tcp-all"]:
            return self.quick_all_tcp()
        elif method in self.valid_modes["udp"]:
            return self.udp_scan()
        elif method in self.valid_modes["aggressive"]:
            return self.aggressive_on_identified()
        else:
            print("Code should not reach here at all")
            return

    #Module functionalities
    
    #dir fuzz with feroxbuster
    def quick_all_tcp(self):
        prefix = self.rustscan + " -a"
        target_arg = self.target
        ulimit_arg = "--ulimit 5000"
        command_list = [prefix, target_arg, ulimit_arg]

        return command_list
    
    def aggressive_on_identified(self):
        port_input = self.module_variables["ports"]["Value"]
        prefix = self.nmap
        agg_arg = "-A "
        port_arg = "-p " + port_input if port_input else ""
        verbose_arg = "-v"
        target_arg = self.target
        command_list = [prefix, agg_arg, port_arg, verbose_arg, target_arg]
        return command_list

    def udp_scan(self):
        port_input = self.module_variables["ports"]["Value"]
        prefix = self.nmap
        type_arg = "-sU"
        verbose_arg = "-v"
        port_arg = port_arg = "-p " + port_input if port_input else ""
        target_arg = self.target
        command_list = [prefix, type_arg, port_arg, verbose_arg, target_arg]
        return command_list


                
   