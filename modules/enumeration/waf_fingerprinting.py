from modules.base_module import baseModule

class waf_fingerprint(baseModule):
    def __init__(self, variables):
        self.module_variables = variables["module_variables"]
        super().__init__(variables)

    def initialize_before_run(self,tools,variables):
        super().initialize_before_run(variables)
        self.wafw00f = tools.get("wafw00f")

    def test(self):
        print("Imported this module")
        print(self.target)
        print(self.wafw00f)

    def get_command_list(self):
        return self.waf_fingerprint()

    def waf_fingerprint(self):
        if not self.target:
            print("Not all compulsory options are set. Check with `options` command")
            return
        self.url = "http://" + self.target

        prefix = self.wafw00f
        target_arg = "-a " + self.url
        command_list = [prefix, target_arg]
        return command_list