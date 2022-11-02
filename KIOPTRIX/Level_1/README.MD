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
 172.10.0.189    00:0c:29:b7:19:1a      8     480  VMware, Inc. 
```

Target: 172.10.0.189
