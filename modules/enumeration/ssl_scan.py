from modules.base_module import baseModule

class ssl_scan(baseModule):
    def __init__(self, variables):
        self.module_variables = variables["module_variables"]
        super().__init__(variables)

    def initialize_before_run(self,tools,variables):
        super().initialize_before_run(variables)
        self.curl = tools.get("curl")

    def test(self):
        print("Imported this module")
        print(self.target)
        print(self.curl)
        print("RHOST format is: www.example.com")

    def get_command_list(self):
        return self.ssl_domain_enum()

    def ssl_domain_enum(self):
        """This module gets various subdomains listed in a domains SSL cert"""
        if not self.target:
            print("Not all compulsory options are set. Check with `options` command")
            return 
        
        prefix = self.curl # add Output
        target_arg = "https://crt.sh/?q=" + self.target + "&output=json"
        command_list = [prefix, target_arg]
        return command_list


    #for entries in response:
    #    common_name = entries["common_name"]
    #    name_value = entries["name_value"]
#
    #    if common_name not in domain_list:
    #        domain_list.append(common_name)
    #    
    #    if "\n" in name_value:
    #        domains = name_value.split("\n")
    #        for domain in domains:
    #            if domain not in domain_list:
    #                domain_list.append(domain)
    #    else:
    #        if name_value not in domain_list:
    #            domain_list.append(domain)
    #
    #domain_list.sort()
    #print(domain_list) #remove this
    #
#