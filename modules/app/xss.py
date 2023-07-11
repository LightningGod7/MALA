from modules.base_module import baseModule

class xss(baseModule):
    def __init__(self, variables):
        self.module_variables = variables["module_variables"]
        super().__init__(variables)

    def initialize_before_run(self,tools,variables):
        super().initialize_before_run(variables)
        self.xsstrike = tools.get("xsstrike")
        self.url = "http://" + self.target
        if self.port:
            self.url += ":" + str(self.port)
        self.curl = tools.get("curl")

    def test(self):
        print("Imported this module")
        print(self.target)
        print(self.curl)
        print("RHOST format is: www.example.com")

    def get_command_list(self):
        return self.xss_test()

    def xss_test(self):
        """This module gets various subdomains listed in a domains SSL cert"""
        if not self.target:
            print("Not all compulsory options are set. Check with `options` command")
            return 
        
        prefix = self.xsstrike # add Output
        target_arg = "--crawl -u " + self.url
        command_list = [prefix, target_arg]
        return command_list


#import os
#
#__name__ = "test scanner"
#__description__ = "test"
#
#def xss_check(domain):
#    """Uses XSStrike to detect prescence of XSS vulnerabilities"""
#    command = "xsstrike --crawl -u " + domain
#    output = os.system(command)
#    
#xss_check("inlanefreight.com")
#