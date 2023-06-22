import os

__name__ = "test scanner"
__description__ = "test"


def subdomain_fuzz(domain,wordlist):
    """This module uses ffuf to fuzz subdomains"""
    #if possible change the output later
    command = "ffuf -of json -o ./ffuf-subdomains.json -w " + wordlist + ":FUZZ -u " + "Https://FUZZ." + domain
    os.system(command)

subdomain_fuzz("inlanefreight.com", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt")

def wfuzz_subdomains(target, wordlist, port=None):
    """Perform subdomain fuzzing using wfuzz"""
    command = "wfuzz -c"
    if port:
        command += f" -p {port}"
    command += f" -z file,{wordlist} --hc 404 -H 'Host: FUZZ.{target}' {target}"
    os.system(command)

def ffuf_subdomains(target, wordlist, port=None):
    """Perform subdomain fuzzing using ffuf"""
    command = "ffuf -c"
    if port:
        command += f" -p {port}"
    command += f" -w {wordlist} -H 'Host: FUZZ.{target}' {target}"
    os.system(command)

def wfuzz_auth_subdomains(target, wordlist, sessionvar=None, sessionval=None, username=None, password=None, port=None):
    """Perform subdomain fuzzing with authentication using wfuzz"""
    command = "wfuzz -c"
    if sessionvar and sessionval:
        command += f" -b '{sessionvar}={sessionval}'"
    if username and password:
        command += f" --basic -u {username}:{password}"
    if port:
        command += f" -p {port}"
    command += f" -z file,{wordlist} --hc 404 -H 'Host: FUZZ.{target}' {target}"
    os.system(command)

def ffuf_auth_subdomains(target, wordlist, sessionvar=None, sessionval=None, username=None, password=None, port=None):
    """Perform subdomain fuzzing with authentication using ffuf"""
    command = "ffuf -c"
    if sessionvar and sessionval:
        command += f" -H '{sessionvar}: {sessionval}'"
    if username and password:
        command += f" --basic -u {username}:{password}"
    if port:
        command += f" -p {port}"
    command += f" -w {wordlist} -H 'Host: FUZZ.{target}' {target}"
    os.system(command)
    