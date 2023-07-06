class searchsploit:
    #Functions Needed
    #Init - Print CWD, EDB Last Update Date
    #Check EDB Last Update Date (if date >1 week OR EDB not found, prompt to update)
    #Update EDB (Update Last Update Date)
    #Usage Help (if input == help print what)
    #Help things to include: set for all options
    #set query (string) / [OPTIONS] showpath, showurl, mirror, titleonly (Bool) / downloadpath (string/path)

    def __init__(self, variables):
        ### SET module variables
        self.module_variables = variables["module_variables"]
        self.module_variables["query"] = {"Value": "", "Description": "full query"}
        self.module_variables["terms"] = {"Value": "", "Description": "space-delimited list of search terms to include"}
        self.module_variables["exlusion(s)"] = {"Value": "", "Description":"comma-delimited list of search terms to exlude"}
        self.module_variables["mirrorpath"] = {"Value": "Not set", "Description":"destination for mirrored exploit"}
        self.module_variables["mirror"] = {"Value": False, "Description":"make copy of exploit in mirrorpath default false"}
        self.module_variables["titleonly"] = {"Value": False, "Description":"query only searches for titles default false"}
        self.module_variables["showpath"] = {"Value": True, "Description":"displays local path to exploit default true"}
        self.module_variables["showurl"] = {"Value": True, "Description":"displays url for source of exploit default true"}

    def check_edb_last_update_date():
        #search for edb existence
        #if no exist, ask if want to download to mirrorpath
        #if y/Y/yes/Yes/YES, download edb and break
        #if no, warn that no edb = no search db

        #if exist, check last update date (univ config), > 1 week, prompt to update

    def update_edb():
        #need requests lib

    def search_main():
        #main search function, splits into search raw (whole) or search for title only (helper functions below)

    def search_raw():
        #helper function performs a normal search (OR of all queries, split by spacing)

    def search_title():
        #helper function performs a title-only search
        
    def query_mirror():
        #helper function to download specific exploits
        # MUST be a single exloit (ID)

    def query_mirrors():
        #helper function to download list of exploits
        #OPTIONAL FUNCTION that i just thought of