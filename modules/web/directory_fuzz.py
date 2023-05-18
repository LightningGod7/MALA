import os

def directory_fuzz(domain,port,wordlist):
    """This module uses ffuf to fuzz directories out from webpages"""
    #if possible change the output later
    if port: 
        command = "ffuf -of json -o ./ffuf-directories.json -w " + wordlist + ":FUZZ -u " + domain + ":" + port + "/FUZZ"
    else:
        command = "ffuf -of json -o ./ffuf-directories.json -w " + wordlist + ":FUZZ -u " + domain + "/FUZZ"

    os.system(command)

directory_fuzz("https://inlanefreight.com", "", "/usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt")

    