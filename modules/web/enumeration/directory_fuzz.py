import os

def directory_fuzz(domain,port,wordlist):
    """This module uses ffuf to fuzz directories out from webpages"""
    #if possible change the output later
    if port: 
        command = "ffuf -of json -o ./ffuf-directories.json -w " + wordlist + ":FUZZ -u " + domain + ":" + port + "/FUZZ"
    else:
        command = "ffuf -of json -o ./ffuf-directories.json -w " + wordlist + ":FUZZ -u " + domain + "/FUZZ"

    os.system(command)

def wfuzz_directory(target, wordlist, port=None):
    """Perform directory fuzzing using wfuzz"""
    command = "wfuzz -c"
    if port:
        command += f" -p {port}"
    command += f" -z file,{wordlist} --hc 404 {target}/FUZZ"
    os.system(command)

def ffuf_directory(target, wordlist, port=None):
    """Perform directory fuzzing using ffuf"""
    command = "ffuf -c"
    if port:
        command += f" -p {port}"
    command += f" -w {wordlist} -u {target}/FUZZ"
    os.system(command)

def wfuzz_auth_directory(target, wordlist, sessionvar=None, sessionval=None, username=None, password=None, port=None):
    """Perform directory fuzzing with authentication using wfuzz"""
    command = "wfuzz -c"
    if sessionvar and sessionval:
        command += f" -b '{sessionvar}={sessionval}'"
    if username and password:
        command += f" --basic -u {username}:{password}"
    if port:
        command += f" -p {port}"
    command += f" -z file,{wordlist} --hc 404 {target}/FUZZ"
    os.system(command)

def ffuf_auth_directory(target, wordlist, sessionvar=None, sessionval=None, username=None, password=None, port=None):
    """Perform directory fuzzing with authentication using ffuf"""
    command = "ffuf -c"
    if sessionvar and sessionval:
        command += f" -H '{sessionvar}: {sessionval}'"
    if username and password:
        command += f" --basic -u {username}:{password}"
    if port:
        command += f" -p {port}"
    command += f" -w {wordlist} -u {target}/FUZZ"
    os.system(command)





   