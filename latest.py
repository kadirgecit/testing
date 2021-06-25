#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess, os, random, string, sys, shutil, socket
from itertools import cycle, izip

rDownloadURL = {"main": "https://www.dropbox.com/s/zibryqq8pya8npn/xplus_main.tar.gz?dl=0", "sub": "0"}
rPackages = ["libcurl3", "libxslt1-dev", "libgeoip-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "mysql-server"]
rInstall = {"MAIN": "main", "LB": "sub"}
rMySQLCnf = "IyBYdHJlYW0gQ29kZXMKCltjbGllbnRdCnBvcnQgICAgICAgICAgICA9IDMzMDYKCltteXNxbGRfc2FmZV0KbmljZSAgICAgICAgICAgID0gMAoKW215c3FsZF0KdXNlciAgICAgICAgICAgID0gbXlzcWwKcG9ydCAgICAgICAgICAgID0gNzk5OQpiYXNlZGlyICAgICAgICAgPSAvdXNyCmRhdGFkaXIgICAgICAgICA9IC92YXIvbGliL215c3FsCnRtcGRpciAgICAgICAgICA9IC90bXAKbGMtbWVzc2FnZXMtZGlyID0gL3Vzci9zaGFyZS9teXNxbApza2lwLWV4dGVybmFsLWxvY2tpbmcKc2tpcC1uYW1lLXJlc29sdmU9MQoKYmluZC1hZGRyZXNzICAgICAgICAgICAgPSAqCmtleV9idWZmZXJfc2l6ZSA9IDEyOE0KCm15aXNhbV9zb3J0X2J1ZmZlcl9zaXplID0gNE0KbWF4X2FsbG93ZWRfcGFja2V0ICAgICAgPSA2NE0KbXlpc2FtLXJlY292ZXItb3B0aW9ucyA9IEJBQ0tVUAptYXhfbGVuZ3RoX2Zvcl9zb3J0X2RhdGEgPSA4MTkyCnF1ZXJ5X2NhY2hlX2xpbWl0ICAgICAgID0gNE0KcXVlcnlfY2FjaGVfc2l6ZSAgICAgICAgPSAyNTZNCgoKZXhwaXJlX2xvZ3NfZGF5cyAgICAgICAgPSAxMAptYXhfYmlubG9nX3NpemUgICAgICAgICA9IDEwME0KCm1heF9jb25uZWN0aW9ucyAgPSAyMDAwMApiYWNrX2xvZyA9IDQwOTYKb3Blbl9maWxlc19saW1pdCA9IDIwMjQwCmlubm9kYl9vcGVuX2ZpbGVzID0gMjAyNDAKbWF4X2Nvbm5lY3RfZXJyb3JzID0gMzA3Mgp0YWJsZV9vcGVuX2NhY2hlID0gNDA5Ngp0YWJsZV9kZWZpbml0aW9uX2NhY2hlID0gNDA5NgoKCnRtcF90YWJsZV9zaXplID0gMUcKbWF4X2hlYXBfdGFibGVfc2l6ZSA9IDFHCgppbm5vZGJfYnVmZmVyX3Bvb2xfc2l6ZSA9IDEwRwppbm5vZGJfYnVmZmVyX3Bvb2xfaW5zdGFuY2VzID0gMTAKaW5ub2RiX3JlYWRfaW9fdGhyZWFkcyA9IDY0Cmlubm9kYl93cml0ZV9pb190aHJlYWRzID0gNjQKaW5ub2RiX3RocmVhZF9jb25jdXJyZW5jeSA9IDAKaW5ub2RiX2ZsdXNoX2xvZ19hdF90cnhfY29tbWl0ID0gMAppbm5vZGJfZmx1c2hfbWV0aG9kID0gT19ESVJFQ1QKcGVyZm9ybWFuY2Vfc2NoZW1hID0gMAppbm5vZGItZmlsZS1wZXItdGFibGUgPSAxCmlubm9kYl9pb19jYXBhY2l0eT0yMDAwMAppbm5vZGJfdGFibGVfbG9ja3MgPSAwCmlubm9kYl9sb2NrX3dhaXRfdGltZW91dCA9IDAKaW5ub2RiX2RlYWRsb2NrX2RldGVjdCA9IDAKCgpzcWwtbW9kZT0iTk9fRU5HSU5FX1NVQlNUSVRVVElPTiIKCltteXNxbGR1bXBdCnF1aWNrCnF1b3RlLW5hbWVzCm1heF9hbGxvd2VkX3BhY2tldCAgICAgID0gMTZNCgpbbXlzcWxdCgpbaXNhbWNoa10Ka2V5X2J1ZmZlcl9zaXplICAgICAgICAgICAgICA9IDE2TQo=".decode("base64")
logo = "ICAgICAgICAgICAgICAgICAgTk1NTU1NTU1NTU1NTU1NTU1Nb2AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDovLy8vK2hoaGRkZGRkZGRkLy8vLwogICAgICAgICAgICAgICAgICAgK05NTU1NTU1NTU1NTU1NTU1NTXNgICAgICAgICAgICAgICAgICAgICAgICAgYGBgYCsrKytoaGhkZGRkZGRkZGRkaGgvLy8KICAgICAgICAgICAgICAgICAgICAgK05NTU1NTU1NTU1NTU1NTU1NTXNgICAgICAgICAgICAgICAgYGBgKysrK2hkZGRkZGRkZGRkZGRkZGhoaC8vLQogICAgICAgICAgICAgICAgICAgICAgICtOTU1NTU1NTU1NTU1NTU1NTU1zYCAgICAgICBgYGArKytkZGRkZGRkZGRkZGRkZGRkZGRoaC86CiAgICAgICAgICAgICAgICAgICAgICAgICAvbU1NTU1NTU1NTU1NTU1NTU1NeS5gYG9vb2RkZGRkZGRkZGRkZGRkZGRkZGRoaDo6LwogICAgICAgICAgICAgICAgICAgICAgICAgICAvTU1NTU1NTU1NTU1NTU1NTk5tZGRkZGRkZGRkZGRkZGRkZGRkZGR5eTo6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAvbU1NTU1NTU1NTk5tbWRkZGRkZGRkZGRkZGRkZGRkZGRkeXk6OgogICAgICAgICAgICAgICAgICAgICAgICAgIC0uLnNzZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkeXMtICAgICAgICAgICAgV2VsY29tZSB0byBYdHJlYW1QbHVzIGluc3RhbGxlciBpbnRlcmZhY2UgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgLnNzbWRkZGRkZGRkZGRkZGRkZGRkZGRkZGRkZGRtTisgICAgICAgICBQbGVhc2UgZG8gbm90IGludGVycnVwdCB0aGUgaW5zdGFsbGVyIHVudGlsIGl0IGZpbmlzaGVkICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAtLXNzZGRkZGRkZGRkZGRoaGhoZGRkZGRkZGRkZGRtTk1NTU1oLQogICAgICAgICAgICAgICAtLXNzZGRkZGRkZGRkZGRoaGhoaGhoaGRkZGRkaGRkbU5NTU1NTU1NTU1kOiAgICAgICAgICAgICAgICAgICAgIFh0cmVhbVBsdXMgVGVhbQogICAgICAgICAgIC0teWRkZGRkZGRkZGRkaGhoaGhoaGhoaGhoZGRkZGRtTk1NTU1NTU1NTU1NTU1NOgogICAgICAgICAteXlkZGRkZGRkZGRkZGhoaGhoaGhoaGhoaGhoaGRkZG95TU1NTU1NTU1NTU1NTU1NTU1kOgogICAgICA6eXlkZGRkZGRkZGRkZGhoaGhoaGhoaGhoaGhoaGhoaG8uLiAgLXlNTU1NTU1NTU1NTU1NTU1NTWQvCiAgICAgOmRkZGRkZGRkZGRkaGhoaGhoaGhoaGhoaGhoaGhoZG8uICAgICAgIC55TU1NTU1NTU1NTU1NTU1NTU1tLwogICAgIGRkZGRkZGRkZGhoaGhoaGhoaGhoaGhoaGhoaGhkby4gICAgICAgICAgIC55TU1NTU1NTU1NTU1NTU1NTU1tLwogICAgaGRkZGRkZGRoaGhoaGhoaGhoaGhoaGhoaGhoaG9gICAgICAgICAgICAgICAgeU1NTU1NTU1NTU1NTU1NTU1NTW0vCiAgIGhkZGRkZGhoaGhoaGhoaGhoaGhoaGhoaGhoaCtgICAgICAgICAgICAgICAgICAgYHNNTU1NTU1NTU1NTU1NTU1NTU0rCiAgL2RkZGRoaGhoaGhoaGhoaGhoaGhoaGhoaGgrYCAgICAgICAgICAgICAgICAgICAgICBgc01NTU1NTU1NTU1NTU1NTU1NTisKIC9kZGRoaGhoaGhoaGhoaGhoaGhoaGhoaGgrYCAgICAgICAgICAgICAgICAgICAgICAgICAgYHNNTU1NTU1NTU1NTU1NTU1NTU4rCiBkZGhoaGhoaGhoaGhoaGhoaGhoaGhoaGgrICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYG9NTU1NTU1NTU1NTU1NTU1NTU5vCmhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoLyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgb01NTU1NTU1NTU1NTU1NTU1NTQ==".decode("base64")

class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def generate(length=16): return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getVersion():
    try: return subprocess.check_output("lsb_release -d".split()).split(":")[-1].strip()
    except: return ""
    
 
def printa(rText, rText2, rColour=col.OKBLUE, rPadding=0):
    print "%s ┌──────────────────────────────────────────┐ %s" % (rColour, col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s │ %s%s%s │ %s" % (rColour, " "*(20-(len(rText)/2)), rText, " "*(40-(20-(len(rText)/2))-len(rText)), col.ENDC)
    print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s │ %s%s%s │ %s" % (rColour, " "*(20-(len(rText2)/2)), rText2, " "*(40-(20-(len(rText2)/2))-len(rText2)), col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s └──────────────────────────────────────────┘ %s" % (rColour, col.ENDC)
    print " "

def printc(rText, rColour=col.OKBLUE, rPadding=0):
    os.system("clear")
    print logo
    print " "
    print "%s ┌──────────────────────────────────────────┐ %s" % (rColour, col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s │ %s%s%s │ %s" % (rColour, " "*(20-(len(rText)/2)), rText, " "*(40-(20-(len(rText)/2))-len(rText)), col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s └──────────────────────────────────────────┘ %s" % (rColour, col.ENDC)
    print " "

def printd(rText, rColour=col.OKBLUE, rPadding=0):
    print "%s ┌──────────────────────────────────────────┐ %s" % (rColour, col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s │ %s%s%s │ %s" % (rColour, " "*(20-(len(rText)/2)), rText, " "*(40-(20-(len(rText)/2))-len(rText)), col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s └──────────────────────────────────────────┘ %s" % (rColour, col.ENDC)
    print " "
    
def info(rText, rText2, rText3, rText4, rColour=col.OKBLUE, rPadding=0):
    print "%s ┌──────────────────────────────────────────┐ %s" % (rColour, col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s │ %s%s%s │ %s" % (rColour, " "*(20-(len(rText)/2)), rText, " "*(40-(20-(len(rText)/2))-len(rText)), col.ENDC)
    print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s │ %s%s%s │ %s" % (rColour, " "*(20-(len(rText2)/2)), rText2, " "*(40-(20-(len(rText2)/2))-len(rText2)), col.ENDC)
    print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s │ %s%s%s │ %s" % (rColour, " "*(20-(len(rText3)/2)), rText3, " "*(40-(20-(len(rText3)/2))-len(rText3)), col.ENDC)
    print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s │ %s%s%s │ %s" % (rColour, " "*(20-(len(rText4)/2)), rText4, " "*(40-(20-(len(rText4)/2))-len(rText4)), col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s └──────────────────────────────────────────┘ %s" % (rColour, col.ENDC)
    print " "

def prepare(rType="MAIN"):
    global rPackages
    if rType <> "MAIN": rPackages = rPackages[:-1]
    printc("Preparing Installation")
    for rFile in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]:
        try: os.remove(rFile)
        except: pass
    os.system("apt-get update > /dev/null")
    printc("Removing libcurl4 if installed")
    os.system("apt-get remove --auto-remove libcurl4 -y 2>&1 >/dev/null")
    for rPackage in rPackages:
        printc("Installing %s" % rPackage)
        os.system("apt-get install %s -y 2>&1 >/dev/nulll" % rPackage) 
    printc("Installing libpng")
    os.system("wget -q -O /tmp/libpng12.deb https://www.dropbox.com/s/bftvb3dzgrqf61w/libpng12-0_1.2.54-1ubuntu1_amd64.deb?dl=1")
    os.system("dpkg -i /tmp/libpng12.deb 2>&1 >/dev/null")
    os.system("apt-get install -y 2>&1 >/dev/null") # Clean up above
    try: os.remove("/tmp/libpng12.deb")
    except: pass
    try:
        subprocess.check_output("getent passwd xtreamcodes 2>&1 >/dev/null".split())
    except:
        # Create User
        printc("Creating user xtreamcodes")
        os.system("adduser --system --shell /bin/false --group --disabled-login xtreamcodes 2>&1 >/dev/null")
    if not os.path.exists("/home/xtreamcodes"): os.mkdir("/home/xtreamcodes")
    return True

def install(rType="MAIN"):
    global rInstall, rDownloadURL
    printc("Downloading Software")
    try: rURL = rDownloadURL[rInstall[rType]]
    except:
        printc("Invalid download URL!", col.FAIL)
        return False
    os.system('wget -q -O "/tmp/xtreamcodes.tar.gz" "%s"' % rURL)
    if os.path.exists("/tmp/xtreamcodes.tar.gz"):
        printc("Installing Software")
        os.system('tar -zxvf "/tmp/xtreamcodes.tar.gz" -C "/home/xtreamcodes/" 2>&1 >/dev/null')
        try: os.remove("/tmp/xtreamcodes.tar.gz")
        except: pass
        return True
    printc("Failed to download installation file!", col.FAIL)
    return False

def mysql(rUsername, rPassword):
    global rMySQLCnf
    printc("Configuring MySQL")
    rCreate = True
    if os.path.exists("/etc/mysql/my.cnf"):
        if open("/etc/mysql/my.cnf", "r").read(14) == "# Xtream Codes": rCreate = False
    if rCreate:
        shutil.copy("/etc/mysql/my.cnf", "/etc/mysql/my.cnf.xc")
        rFile = open("/etc/mysql/my.cnf", "w")
        rFile.write(rMySQLCnf)
        rFile.close()
        os.system("service mysql restart 2>&1 >/dev/null")
    printc("Enter New MySQL Root Password:", col.WARNING)
    for i in range(5):
        rExtra = ""
        rDrop = True
        try:
            if rDrop:
                os.system('mysql -u root%s -e "DROP DATABASE IF EXISTS xtream_iptvpro; CREATE DATABASE IF NOT EXISTS xtream_iptvpro;" 2>&1 >/dev/null' % rExtra)
                os.system("mysql -u root%s xtream_iptvpro < /home/xtreamcodes/iptv_xtream_codes/databaseplus.sql 2>&1 >/dev/null" % rExtra)
                os.system('mysql -u root%s -e "USE xtream_iptvpro; UPDATE settings SET live_streaming_pass = \'%s\', unique_id = \'%s\', crypt_load_balancing = \'%s\';" 2>&1 >/dev/null' % (rExtra, generate(20), generate(10), generate(20)))
                os.system('mysql -u root%s -e "USE xtream_iptvpro; REPLACE INTO streaming_servers (id, server_name, domain_name, server_ip, vpn_ip, ssh_password, ssh_port, diff_time_main, http_broadcast_port, total_clients, system_os, network_interface, latency, status, enable_geoip, geoip_countries, last_check_ago, can_delete, server_hardware, total_services, persistent_connections, rtmp_port, geoip_type, isp_names, isp_type, enable_isp, boost_fpm, http_ports_add, network_guaranteed_speed, https_broadcast_port, https_ports_add, whitelist_ips, watchdog_data, timeshift_only) VALUES (1, \'Main Server\', \'\', \'%s\', \'\', NULL, NULL, 0, 25461, 1000, \'%s\', \'eth0\', 0, 1, 0, \'\', 0, 0, \'{}\', 3, 0, 25462, \'low_priority\', \'\', \'low_priority\', 0, 1, \'\', 1000, 25463, \'\', \'[\"127.0.0.1\",\"\"]\', \'{}\', 0);" 2>&1 >/dev/null' % (rExtra, getIP(), getVersion()))
                os.system('mysql -u root%s -e "USE xtream_iptvpro; REPLACE INTO reg_users (id, username, password, email, member_group_id, verified, status) VALUES (1, \'admin\', \'\$6\$rounds=20000\$xtreamcodes\$XThC5OwfuS0YwS4ahiifzF14vkGbGsFF1w7ETL4sRRC5sOrAWCjWvQJDromZUQoQuwbAXAFdX3h3Cp3vqulpS0\', \'admin@website.com\', 1, 1, 1);" 2>&1 >/dev/null'  % rExtra)
            os.system('mysql -u root%s -e "GRANT ALL PRIVILEGES ON *.* TO \'%s\'@\'%%\' IDENTIFIED BY \'%s\' WITH GRANT OPTION; FLUSH PRIVILEGES;" 2>&1 >/dev/null' % (rExtra, rUsername, rPassword))
            try: os.remove("/home/xtreamcodes/iptv_xtream_codes/database.sql")
            except: pass
            try: os.remove("/home/xtreamcodes/iptv_xtream_codes/databaseplus.sql")
            except: pass
            return True
        except: printc("Invalid password! Try again", col.FAIL)
    return False

def encrypt(rHost="127.0.0.1", rUsername="user_iptvpro", rPassword="", rDatabase="xtream_iptvpro", rServerID=1, rPort=7999):
    printc("Encrypting...")
    try: os.remove("/home/xtreamcodes/iptv_xtream_codes/config")
    except: pass
    rf = open('/home/xtreamcodes/iptv_xtream_codes/config', 'wb')
    rf.write(''.join(chr(ord(c)^ord(k)) for c,k in izip('{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1'))).encode('base64').replace('\n', ''))
    rf.close()

def configure():
    printc("Configuring System")
    if not "/home/xtreamcodes/iptv_xtream_codes/" in open("/etc/fstab").read():
        rFile = open("/etc/fstab", "a")
        rFile.write("tmpfs /home/xtreamcodes/iptv_xtream_codes/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamcodes/iptv_xtream_codes/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
        rFile.close()
    if not "xtreamcodes" in open("/etc/sudoers").read():
        os.system('echo "xtreamcodes ALL=(root) NOPASSWD: /sbin/iptables, /usr/bin/chattr" >> /etc/sudoers')
    if not os.path.exists("/etc/init.d/xtreamplus"):
        rStart = open("/etc/init.d/xtreamplus", "w")
        rStart.write("#!/bin/bash\n### BEGIN INIT INFO\n# Provides:          xtreamplus\n# Required-Start:    $all\n# Required-Stop:\n# Default-Start:     2 3 4 5\n# Default-Stop:\n# Short-Description: Run /etc/init.d/xtreamplus if it exist\n### END INIT INFO\nsleep 1\n/home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null")
        rStart.close()
        os.system("chmod +x /etc/init.d/xtreamplus")
        os.system("update-rc.d xtreamplus defaults")
        os.system("update-rc.d xtreamplus enable")
    try: os.remove("/usr/bin/ffmpeg")
    except: pass
    if not os.path.exists("/home/xtreamcodes/iptv_xtream_codes/tv_archive"): os.mkdir("/home/xtreamcodes/iptv_xtream_codes/tv_archive/")
    os.system("ln -s /home/xtreamcodes/iptv_xtream_codes/bin/ffmpeg /usr/bin/")
    os.system("chown xtreamcodes:xtreamcodes -R /home/xtreamcodes 2>&1 >/dev/null")
    os.system("chmod -R 0777 /home/xtreamcodes > /dev/null")
    os.system("chmod +x /home/xtreamcodes/iptv_xtream_codes/start_services.sh 2>&1 >/dev/null")
    os.system("chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb 2>&1 >/dev/null")
    os.system("mount -a")
    if not "api.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    api.xtream-codes.com" >> /etc/hosts')
    if not "downloads.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    downloads.xtream-codes.com" >> /etc/hosts')
    if not " xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')
    printc("Installing latest updates")
    os.system('apt-get install unzip e2fsprogs python-paramiko -y 2>&1 >/dev/null && chmod +x /home/xtreamcodes/iptv_xtream_codes/permissions.sh && chmod +x /home/xtreamcodes/iptv_xtream_codes/start_services.sh && /home/xtreamcodes/iptv_xtream_codes/permissions.sh')
    os.system("sed -i 's|echo \"XtreamPlus\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamcodes/iptv_xtream_codes/wwwdir/index.php")
    printc("Installing YouTube-dl")
    os.system("sudo wget -q https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl")
    os.system("sudo chmod a+rx /usr/local/bin/youtube-dl")
    printc("Installing Glances")
    os.system("sudo python -m pip install -U pip > /dev/null")
    os.system("sudo python -m pip install -U setuptools > /dev/null")
    os.system("wget -q -O- https://bit.ly/glances | /bin/bash")

def start(first=True):
    if first: printc("Starting XtreamPlus Service")
    else: printc("Restarting XtreamPlus Service")
    os.system("service xtreamplus start")
    os.system("chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb")

def qsv():
    printc("Detecting GPU Hardware")
    printc("Skipping for now...")
    #os.system("apt-get install linux-base flussonic-qsv -y > /dev/null")
    #os.system("sudo ln -s /usr/share/phpmyadmin /home/xtreamcodes/iptv_xtream_codes/admin > /dev/null")

def replacePorts(admin="25500", client="80", streaming="25461"):
    printc("Starting XtreamPlus Ports")
    os.system('mysql -u root -e "USE xtream_iptvpro; UPDATE streaming_servers SET http_broadcast_port = \'%s\';" 2>&1 >/dev/null' % streaming)
    filein = "/home/xtreamcodes/iptv_xtream_codes/nginx/conf/nginx.conf"
    replacements = {'__adminport__':admin, '__clientport__':client, '__streamport__':streaming}
    lines = []
    with open(filein) as infile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            lines.append(line)
    with open(filein, 'w') as outfile:
        for line in lines:
            outfile.write(line)

if __name__ == "__main__":
    os.system("clear")
    print logo
    print " "
    printd("XtreamPlus Installation Interface", col.OKGREEN, 2)
    printd("Please enter your license code : ", col.WARNING)
    if raw_input("  ").upper() == "DEVELOPER":
        printc("Enter Admin Panel port (25500)")
        admin = raw_input("  ")
        printc("Enter Client Panel port (80)")
        client = raw_input("  ")
        printc("Enter Streaming port (25461)")
        streaming = raw_input("  ")
        rType = "MAIN"
        if rType.upper() in ["MAIN", "LB"]:
            rHost = "127.0.0.1"
            rPassword = generate()
            rServerID = 1
            rUsername = "user_iptvpro"
            rDatabase = "xtream_iptvpro"
            rPort = 7999
            if len(rHost) > 0 and len(rPassword) > 0 and rServerID > -1:
                os.system("clear")
                info("IP Address: %s" %  getIP(),"Admin Panel Port: %s" % admin,"Client Panel Port: %s" % client,"Streaming Port: %s"% streaming,col.WARNING)
                printd("Start installation? Y/N", col.WARNING)
                if raw_input("  ").upper() == "Y":
                    print " "
                    rRet = prepare(rType.upper())
                    if not install(rType.upper()): sys.exit(1)
                    encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
                    configure()
                    if rType.upper() == "MAIN":
                        if not mysql(rUsername, rPassword): sys.exit(1)
                    printc("Install GPU Transcoding? Y/N")
                    if raw_input("  ").upper() == "Y":
                        qsv()
                    replacePorts(admin,client,streaming)
                    start()
                    os.system("clear")
                    print logo
                    print " "
                    printd("XtreamPlus Installation Completed!", col.OKGREEN, 2)
                    printa("Admin UI: http://%s:%s" % (getIP(),admin), "Username: admin / Password: admin")
                    printd("Client UI: http://%s" % getIP())
                    if rType.upper() == "MAIN":
                        printa("Please store your MySQL password!", "MySQL password : %s" % rPassword)
                else: printc("Installation cancelled", col.FAIL)
            else: printc("Invalid entries", col.FAIL)
        else: printc("Invalid installation type", col.FAIL)
    else:printc("Invalid license.", col.FAIL)
