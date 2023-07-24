from modules.base_module import baseModule

class webtech_id(baseModule):
    def __init__(self, variables):
        self.module_variables = variables["module_variables"]
        super().__init__(variables)

    def initialize_before_run(self,tools,variables):
        super().initialize_before_run(variables)
        self.whatweb = tools.get("whatweb")
        self.url = "http://" + self.target
        
    def test(self):
        print("Imported this module")
        print(self.target)
        print(self.whatweb)


    def get_command_list(self):
        return self.webtech_id()

    def webtech_id(self):
        if not self.target:
            print("Not all compulsory options are set. Check with `options` command")
            return

        prefix = self.whatweb
        target_arg = "-a3 " + self.url + " --log-json=./technologies.txt"
        command_list = [prefix, target_arg]
        return command_list
    
#import os
#import json
#
#__name__ = "test scanner"
#__description__ = "test"
#
#def web_tech_id(domain):
#    """Identifies the technologies used on a webpage using whatweb and exports it in json format"""
#    command = "whatweb -a3 " + domain + " --log-json=./technologies.txt"
#    os.system(command)
#    with open("technologies.txt", 'r') as f:
#        output = json.load(f)
#    for entries in output:
#        if entries["http_status"] == 200:
#            unparsed_results = entries
#    
#    with open("technologies.json", 'w') as f:
#        f.write(json.dumps(unparsed_results['plugins']))
#        
#
#web_tech_id("inlanefreight.com")