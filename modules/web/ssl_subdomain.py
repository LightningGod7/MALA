import requests
import json

def ssl_domain_enum(domain):
    """This module gets various subdomains listed in a domains SSL cert"""
    domain_list = []
    response = requests.get("https://crt.sh/?q=" + domain +"&output=json").json()
    for entries in response:
        common_name = entries["common_name"]
        name_value = entries["name_value"]

        if common_name not in domain_list:
            domain_list.append(common_name)
        
        if "\n" in name_value:
            domains = name_value.split("\n")
            for domain in domains:
                if domain not in domain_list:
                    domain_list.append(domain)
        else:
            if name_value not in domain_list:
                domain_list.append(domain)
    
    domain_list.sort()
    print(domain_list) #remove this
    
ssl_domain_enum("github.com")