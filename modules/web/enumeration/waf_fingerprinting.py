import os

__name__ = "test scanner"
__description__ = "test"


def waf_fingerprint(domain):
    """Uses Wafw00f to detect prescence of a WAF"""
    command = "wafw00f -a " + domain + "| grep 'is behind'"
    output = os.popen(command).read()
    if output:
        print("WAF Found\n")
        print(output)
    else:
        print("No WAF detected or Undetectable by wafw00f")
    
waf_fingerprint("inlanefreight.com")