# Web-Sec-Tools
Automation tools for web security







-------- Check List ----------

=== Modules ===



0. Basic enum
- Vuln scanning
- Banner grabbing
- Tech Stack identification
- Enumeration + abusing apis

1. Directory brute force & fuzzing

2. XSS 
 - Stored & reflected
 - ID-ing XSS Vulns

3. Directory Traversal
 - Identify & exploit directory traversals
 - Encoding Special characters
 
4. File inclusion Vulns
 - LFI
 - PHP Wrappers
 - RFI

5. File Upload Vulns
 - Executable files (.php rev shells etc)
 - Non executable files (id_rsa/ config over writes)

6. Command Injections
 - OS Command injection (windows? linux?)
 
7. SQL Injection
  - ID-ing SQLi via error-based payloads
  - UNION-based
  - Blind

8. Searchsploit integration


=== Tool controllers ===
9. Modularizing basic web tools
- Break down the basic web tool's (Wfuzz, ffuf, gobuster, dirb etc) command structure and create a universal python string variable. 
- plug and play by string variables in the full command string 
- Bunch of variable setters per module call (if want do with auth, what wordlists are used, if got specify port etc)
- The string will construct itself at the end

10. Controller script
- Need a controller file to make the tool act like msfconsole
- Let users set bunch of variable before running any modules
- Lets them continue to run other modules after some are completed or still runnning concurrently without having to type out the long ass command

11. Command builder script
- Modules will call this py file at the end
- Modules pass this file all arguments required to form the command
  - binary to use (nmap / gobuster / ffuf etc)
  - arguments to use

12. Startup Configs to initialize variables
- Full path to binaries used

13. Misc tools
- URL encoder/ decoder


===Common Reference Tools===
1. Domains
  - WHOIS
  - DIG
  - crt.sh
  - Zone Transfers
 
2. Web Servers
  - Curl
  - WhatWeb
  - WafW00f
  - Wappalyzer
  - Aquatone
  - ffuf
