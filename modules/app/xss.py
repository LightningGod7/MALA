import os

__name__ = "test scanner"
__description__ = "test"

def xss_check(domain):
    """Uses XSStrike to detect prescence of XSS vulnerabilities"""
    command = "xsstrike --crawl -u " + domain
    output = os.system(command)
    
xss_check("inlanefreight.com")
