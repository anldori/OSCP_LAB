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
