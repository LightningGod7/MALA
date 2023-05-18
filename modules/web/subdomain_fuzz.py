import os

def subdomain_fuzz(domain,wordlist):
    """This module uses ffuf to fuzz subdomains"""
    #if possible change the output later
    command = "ffuf -of json -o ./ffuf-subdomains.json -w " + wordlist + ":FUZZ -u " + "Https://FUZZ." + domain
    os.system(command)

subdomain_fuzz("inlanefreight.com", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt")

    