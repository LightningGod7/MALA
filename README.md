# Web-Sec-Tools
Automation tools for web security





===Enumeration===

- Vuln scanning
- Banner grabbing
- Tech Stack identification
- Enumeration + abusing apis

1. Check for subdomains (refer dnssec, dnsenum/ gobuster command?)
  wfuzz -c -f subdomains.txt -w /usr/share/wordlists/subdomain-10000.txt -u "http://zeus.com/" -H "Host: FUZZ.zeus.com" --hl [lines]

===Common web attacks===

1. Directory brute force
 - Automate flow

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
