import os
import json

__name__ = "test scanner"
__description__ = "test"

def web_tech_id(domain):
    """Identifies the technologies used on a webpage using whatweb and exports it in json format"""
    command = "whatweb -a3 " + domain + " --log-json=./technologies.txt"
    os.system(command)
    with open("technologies.txt", 'r') as f:
        output = json.load(f)
    for entries in output:
        if entries["http_status"] == 200:
            unparsed_results = entries
    
    with open("technologies.json", 'w') as f:
        f.write(json.dumps(unparsed_results['plugins']))
        

web_tech_id("inlanefreight.com")