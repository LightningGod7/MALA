import os
import requests
import datetime

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
        edb_filename = 'edb.csv'
        directory = 'modules/edb'
        date_filename = "lastfetched.txt"
        csv_path = os.path.join(os.getcwd(), directory, edb_filename)

        #if exist, check last update date (univ config), > 1 week, prompt to update
        if os.path.isfile(csv_path):
            print("The EDB exists locally!")
            #check last fetched
            file_path = os.path.join(directory, date_filename)
            try:
                # Read the datetime from the text file
                with open(file_path, "r") as file:
                    datetime_str = file.read().strip()
                saved_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                current_datetime = datetime.now()
                delta = current_datetime - saved_datetime
                num_days = delta.days
                if int(num_days) < 7:
                    print("Number of days since last fetched:", num_days)
                else:
                    print("Number of days since last fetched is more than a week. It is recommended to update the database.")
            except FileNotFoundError:
                print("Last Fetched Date for EDB not found.")
            if (input("Would you like to update to the latest EDB? :")).lower() in ['y','yes']:
                print("Updating Exploit Database...")
                edb_url = 'https://gitlab.com/exploit-database/exploitdb/-/blob/main/files_exploits.csv'
                r = requests.get(edb_url, allow_redirects=True)
                open('edb.csv','wb').write(r.content)
                print("Download has completed!")
                # Update the last fetched datetime of EDB into modules/edb
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file_path = os.path.join(directory, date_filename)
                with open(file_path, "w") as file:
                    file.write(current_datetime)
            else:
                print("Skipping Updating of EDB.")

        #if no exist, ask if want to download to mirrorpath
        else:
            print("Exploit DB not found!")
            if (input("Would you like to download the latest EDB? :")).lower() in ['y','yes']:
                print("Downloading Exploit Database...")
                edb_url = 'https://gitlab.com/exploit-database/exploitdb/-/blob/main/files_exploits.csv'
                r = requests.get(edb_url, allow_redirects=True)
                open('edb.csv','wb').write(r.content)
                print("Download has completed!")
                # Update the last fetched datetime of EDB into modules/edb
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file_path = os.path.join(directory, date_filename)
                with open(file_path, "w") as file:
                    file.write(current_datetime)
            else:
                print("WARNING : NO EDB FOUND. SEARCHING WILL NOT PRODUCE ANY RESULTS!")
        #if no, warn that no edb = no search db

        
    def update_edb():
        edb_filename = 'edb.csv'
        directory = 'modules/edb'
        date_filename = "lastfetched.txt"
        print("Downloading Exploit Database...")
        edb_url = 'https://gitlab.com/exploit-database/exploitdb/-/blob/main/files_exploits.csv'
        r = requests.get(edb_url, allow_redirects=True)
        open('edb.csv','wb').write(r.content)
        print("Download has completed!")
        # Update the last fetched datetime of EDB into modules/edb
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = os.path.join(directory, date_filename)
        with open(file_path, "w") as file:
            file.write(current_datetime)
        #need requests lib

    def search_main():
        print("function")
        #main search function, splits into search raw (whole) or search for title only (helper functions below)

    def search_raw():
        print("function")
        #helper function performs a normal search (OR of all queries, split by spacing)

    def search_title():
        print("function")
        #helper function performs a title-only search
        
    def query_mirror():
        print("function")
        #helper function to download specific exploits
        # MUST be a single exloit (ID)

    def query_mirrors():
        print("function")
        #helper function to download list of exploits
        #OPTIONAL FUNCTION that i just thought of