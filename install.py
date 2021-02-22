#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess, os, random, string, sys, shutil, socket
from itertools import cycle, izip

rDownloadURL = {"main": "https://www.dropbox.com/s/sdik24gd41cz0g1/main_xtreamplus_reborn.tar.gz?dl=0", "sub": "https://www.dropbox.com/s/rv5k3l1yt2v6ccy/sub_xtreamplus_reborn.tar.gz?dl=0"}
rPackages = ["libcurl3", "libxslt1-dev", "libgeoip-dev", "e2fsprogs", "wget", "mcrypt", "nscd", "htop", "zip", "unzip", "mc", "mysql-server"]
rInstall = {"MAIN": "main", "LB": "sub"}
rMySQLCnf = "IyBYdHJlYW1QbHVzIG15c3FsIGNvbmZpZwoKW2NsaWVudF0KcG9ydCAgICAgICAgICAgID0gMzMwNgoKW215c3FsZF9zYWZlXQpuaWNlICAgICAgICAgICAgPSAwCgpbbXlzcWxkXQp1c2VyICAgICAgICAgICAgPSBteXNxbApwb3J0ICAgICAgICAgICAgPSA3OTk5CmJhc2VkaXIgICAgICAgICA9IC91c3IKZGF0YWRpciAgICAgICAgID0gL3Zhci9saWIvbXlzcWwKdG1wZGlyICAgICAgICAgID0gL3RtcApsYy1tZXNzYWdlcy1kaXIgPSAvdXNyL3NoYXJlL215c3FsCnNraXAtZXh0ZXJuYWwtbG9ja2luZwpza2lwLW5hbWUtcmVzb2x2ZT0xCgpiaW5kLWFkZHJlc3MgICAgICAgICAgICA9ICoKa2V5X2J1ZmZlcl9zaXplID0gMTI4TQoKbXlpc2FtX3NvcnRfYnVmZmVyX3NpemUgPSA0TQptYXhfYWxsb3dlZF9wYWNrZXQgICAgICA9IDY0TQpteWlzYW0tcmVjb3Zlci1vcHRpb25zID0gQkFDS1VQCm1heF9sZW5ndGhfZm9yX3NvcnRfZGF0YSA9IDgxOTIKcXVlcnlfY2FjaGVfbGltaXQgICAgICAgPSA0TQpxdWVyeV9jYWNoZV9zaXplICAgICAgICA9IDI1Nk0KCgpleHBpcmVfbG9nc19kYXlzICAgICAgICA9IDEwCm1heF9iaW5sb2dfc2l6ZSAgICAgICAgID0gMTAwTQoKbWF4X2Nvbm5lY3Rpb25zICA9IDIwMDAwCmJhY2tfbG9nID0gNDA5NgpvcGVuX2ZpbGVzX2xpbWl0ID0gMjAyNDAKaW5ub2RiX29wZW5fZmlsZXMgPSAyMDI0MAptYXhfY29ubmVjdF9lcnJvcnMgPSAzMDcyCnRhYmxlX29wZW5fY2FjaGUgPSA0MDk2CnRhYmxlX2RlZmluaXRpb25fY2FjaGUgPSA0MDk2CgoKdG1wX3RhYmxlX3NpemUgPSAxRwptYXhfaGVhcF90YWJsZV9zaXplID0gMUcKCmlubm9kYl9idWZmZXJfcG9vbF9zaXplID0gMTBHCmlubm9kYl9idWZmZXJfcG9vbF9pbnN0YW5jZXMgPSAxMAppbm5vZGJfcmVhZF9pb190aHJlYWRzID0gNjQKaW5ub2RiX3dyaXRlX2lvX3RocmVhZHMgPSA2NAppbm5vZGJfdGhyZWFkX2NvbmN1cnJlbmN5ID0gMAppbm5vZGJfZmx1c2hfbG9nX2F0X3RyeF9jb21taXQgPSAwCmlubm9kYl9mbHVzaF9tZXRob2QgPSBPX0RJUkVDVApwZXJmb3JtYW5jZV9zY2hlbWEgPSAwCmlubm9kYi1maWxlLXBlci10YWJsZSA9IDEKaW5ub2RiX2lvX2NhcGFjaXR5PTIwMDAwCmlubm9kYl90YWJsZV9sb2NrcyA9IDAKaW5ub2RiX2xvY2tfd2FpdF90aW1lb3V0ID0gMAppbm5vZGJfZGVhZGxvY2tfZGV0ZWN0ID0gMAoKCnNxbC1tb2RlPSJOT19FTkdJTkVfU1VCU1RJVFVUSU9OIgoKW215c3FsZHVtcF0KcXVpY2sKcXVvdGUtbmFtZXMKbWF4X2FsbG93ZWRfcGFja2V0ICAgICAgPSAxNk0KCltteXNxbF0KCltpc2FtY2hrXQprZXlfYnVmZmVyX3NpemUgICAgICAgICAgICAgID0gMTZNCg==".decode("base64")
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

def printc(rText, rColour=col.OKBLUE, rPadding=0):
    print "%s > %s%s%s %s" % (rColour, " "*(20-(len(rText)/2)), rText, " "*(40-(20-(len(rText)/2))-len(rText)), col.ENDC)

def printo(rText, rColour=col.OKBLUE, rPadding=0):
    print "%s ┌──────────────────────────────────────────┐ %s" % (rColour, col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s │ %s%s%s │ %s" % (rColour, " "*(20-(len(rText)/2)), rText, " "*(40-(20-(len(rText)/2))-len(rText)), col.ENDC)
    for i in range(rPadding): print "%s │                                          │ %s" % (rColour, col.ENDC)
    print "%s └──────────────────────────────────────────┘ %s" % (rColour, col.ENDC)
    print " "

def prepare(rType="MAIN"):
    global rPackages
    if rType <> "MAIN": rPackages = rPackages[:-1]
    os.system("clear")
    print logo
    print " "
    printc("Preparing Installation")
    #for rFile in ["/var/lib/dpkg/lock-frontend", "/var/cache/apt/archives/lock", "/var/lib/dpkg/lock"]:
        #try: os.remove(rFile)
        #except: pass
    os.system("apt-get update > /dev/null")
    os.system("clear")
    print logo
    print " "
    printc("Removing libcurl4 if installed")
    #os.system("apt-get remove --auto-remove libcurl4 -y > /dev/null")
    #for rPackage in rPackages:
        #printc("Installing %s" % rPackage)
        #os.system("apt-get install %s -y > /dev/null" % rPackage) 
    os.system("clear")
    print logo
    print " "
    printc("Installing libpng")
    #os.system("wget -q -O /tmp/libpng12.deb https://www.dropbox.com/s/bftvb3dzgrqf61w/libpng12-0_1.2.54-1ubuntu1_amd64.deb?dl=1")
    #os.system("dpkg -i /tmp/libpng12.deb > /dev/null")
    #os.system("apt-get install -y > /dev/null") # Clean up above

    #try: os.remove("/tmp/libpng12.deb")
    #except: pass
    #try:
        #subprocess.check_output("getent passwd xtreamplus > /dev/null".split())
    #except:
        # Create User
        #os.system("clear")
        #print logo
        #print " "
        #printc("Creating user xtreamplus")
        #os.system("adduser --system --shell /bin/false --group --disabled-login xtreamplus > /dev/null")
    #if not os.path.exists("/home/xtreamplus"): os.mkdir("/home/xtreamplus")
    return True

def install(rType="MAIN"):
    global rInstall, rDownloadURL
    os.system("clear")
    print logo
    print " "
    printc("Downloading Software")
    #try: rURL = rDownloadURL[rInstall[rType]]
    #except:
        #os.system("clear")
        #print logo
        #print " "
        #printc("Invalid download URL!", col.FAIL)
        #return False
    #os.system('wget -q -O "/tmp/xtreamplus.tar.gz" "%s"' % rURL)
    #if os.path.exists("/tmp/xtreamplus.tar.gz"):
        #os.system("clear")
        #print logo
        #print " "
        #printc("Installing Software")
        #os.system('tar -zxvf "/tmp/xtreamplus.tar.gz" -C "/home/xtreamplus/" > /dev/null')
        #try: os.remove("/tmp/xtreamplus.tar.gz")
        #except: pass
        #return True
    #os.system("clear")
    #print logo
    #print " "
    #printc("Failed to download installation file!", col.FAIL)
    return True

def mysql(rUsername, rPassword):
    global rMySQLCnf
    os.system("clear")
    print logo
    print " "
    printc("Configuring MySQL")
    #rCreate = True
    #if os.path.exists("/etc/mysql/my.cnf"):
        #if open("/etc/mysql/my.cnf", "r").read(14) == "# XtreamPlus mysql config": rCreate = False
    #if rCreate:
        #shutil.copy("/etc/mysql/my.cnf", "/etc/mysql/my.cnf.xc")
        #rFile = open("/etc/mysql/my.cnf", "w")
        #rFile.write(rMySQLCnf)
        #rFile.close()
        #os.system("service mysql restart > /dev/null")
    #os.system("clear")
    #print logo
    #print " "
    #printc("Enter MySQL Root Password:", col.WARNING)
    #for i in range(5):
        #rMySQLRoot = raw_input("  ")
        #print " "
        #if len(rMySQLRoot) > 0: rExtra = " -p%s" % rMySQLRoot
        #else: rExtra = ""
        #printc("Drop existing & create database? Y/N", col.WARNING)
        #if raw_input("  ").upper() == "Y": rDrop = True
        #else: rDrop = False
        #try:
            #if rDrop:
                #os.system('mysql -u root%s -e "DROP DATABASE IF EXISTS xtreamplus; CREATE DATABASE IF NOT EXISTS xtreamplus;" > /dev/null' % rExtra)
                #os.system("mysql -u root%s xtreamplus < /home/xtreamplus/system/database.sql > /dev/null" % rExtra)
                #os.system('mysql -u root%s -e "USE xtreamplus; UPDATE settings SET live_streaming_pass = \'%s\', unique_id = \'%s\', crypt_load_balancing = \'%s\';" > /dev/null' % (rExtra, generate(20), generate(10), generate(20)))
                #os.system('mysql -u root%s -e "USE xtreamplus; REPLACE INTO streaming_servers (id, server_name, domain_name, server_ip, vpn_ip, ssh_password, ssh_port, diff_time_main, http_broadcast_port, total_clients, system_os, network_interface, latency, status, enable_geoip, geoip_countries, last_check_ago, can_delete, server_hardware, total_services, persistent_connections, rtmp_port, geoip_type, isp_names, isp_type, enable_isp, boost_fpm, http_ports_add, network_guaranteed_speed, https_broadcast_port, https_ports_add, whitelist_ips, watchdog_data, timeshift_only) VALUES (1, \'Main Server\', \'\', \'%s\', \'\', NULL, NULL, 0, 25461, 1000, \'%s\', \'eth0\', 0, 1, 0, \'\', 0, 0, \'{}\', 3, 0, 25462, \'low_priority\', \'\', \'low_priority\', 0, 1, \'\', 1000, 25463, \'\', \'[\"127.0.0.1\",\"\"]\', \'{}\', 0);" > /dev/null' % (rExtra, getIP(), getVersion()))
                #os.system('mysql -u root%s -e "USE xtreamplus; REPLACE INTO reg_users (id, username, password, email, member_group_id, verified, status) VALUES (1, \'admin\', \'\$6\$rounds=20000\$xtreamplus\$XThC5OwfuS0YwS4ahiifzF14vkGbGsFF1w7ETL4sRRC5sOrAWCjWvQJDromZUQoQuwbAXAFdX3h3Cp3vqulpS0\', \'admin@website.com\', 1, 1, 1);" > /dev/null'  % rExtra)
            #os.system('mysql -u root%s -e "GRANT ALL PRIVILEGES ON *.* TO \'%s\'@\'%%\' IDENTIFIED BY \'%s\' WITH GRANT OPTION; FLUSH PRIVILEGES;" > /dev/null' % (rExtra, rUsername, rPassword))
            #try: os.remove("/home/xtreamplus/system/database.sql")
            #except: pass
            #return True
        #except: printc("Invalid password! Try again", col.FAIL)
    return True

def encrypt(rHost="127.0.0.1", rUsername="xtreamplus_usr", rPassword="", rDatabase="xtreamplus", rServerID=1, rPort=7999):
    printc("Encrypting...")
    #try: os.remove("/home/xtreamplus/system/config")
    #except: pass
    #rf = open('/home/xtreamplus/system/config', 'wb')
    #rf.write(''.join(chr(ord(c)^ord(k)) for c,k in izip('{\"host\":\"%s\",\"db_user\":\"%s\",\"db_pass\":\"%s\",\"db_name\":\"%s\",\"server_id\":\"%d\", \"db_port\":\"%d\"}' % (rHost, rUsername, rPassword, rDatabase, rServerID, rPort), cycle('5709650b0d7806074842c6de575025b1'))).encode('base64').replace('\n', ''))
    #rf.close()

def phpmyadmin():
    printc("Installing phpmyadmin")
    #os.system("apt-get install phpmyadmin -y > /dev/null")
    #os.system("sudo ln -s /usr/share/phpmyadmin /home/xtreamplus/system/admin > /dev/null")

def qsv():
    printc("Installing Intel Quick Sync Video")
    #os.system("apt-get install phpmyadmin -y > /dev/null")
    #os.system("sudo ln -s /usr/share/phpmyadmin /home/xtreamplus/system/admin > /dev/null")


def configure():
    printc("Configuring System")
    #if not "/home/xtreamplus/system/" in open("/etc/fstab").read():
        #rFile = open("/etc/fstab", "a")
        #rFile.write("tmpfs /home/xtreamplus/system/streams tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=90% 0 0\ntmpfs /home/xtreamplus/system/tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=2G 0 0")
        #rFile.close()
    #if not "xtreamplus" in open("/etc/sudoers").read():
        #os.system('echo "xtreamplus ALL=(root) NOPASSWD: /sbin/iptables, /usr/bin/chattr" >> /etc/sudoers')
    #if not os.path.exists("/etc/init.d/xtreamplus"):
        #rStart = open("/etc/init.d/xtreamplus", "w")
        #rStart.write("#!/bin/bash\n### BEGIN INIT INFO\n# Provides:          xtreamplus\n# Required-Start:    $all\n# Required-Stop:\n# Default-Start:     2 3 4 5\n# Default-Stop:\n# Short-Description: Run /etc/init.d/xtreamplus if it exist\n### END INIT INFO\nsleep 1\n/home/xtreamplus/system/start_services.sh > /dev/null")
        #rStart.close()
        #os.system("chmod +x /etc/init.d/xtreamplus")
        #os.system("update-rc.d xtreamplus defaults")
        #os.system("update-rc.d xtreamplus enable")
    #try: os.remove("/usr/bin/ffmpeg")
    #except: pass
    #if not os.path.exists("/home/xtreamplus/system/tv_archive"): os.mkdir("/home/xtreamplus/system/tv_archive/")
    #os.system("ln -s /home/xtreamplus/system/bin/ffmpeg /usr/bin/")
    #os.system("chown xtreamplus:xtreamplus -R /home/xtreamplus > /dev/null")
    #os.system("chmod -R 0777 /home/xtreamplus > /dev/null")
    #os.system("chmod +x /home/xtreamplus/system/start_services.sh > /dev/null")
    #os.system("chattr -i /home/xtreamplus/system/GeoLite2.mmdb > /dev/null")
    #os.system("mount -a")
    #if not "api.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    api.xtream-codes.com" >> /etc/hosts')
    #if not "downloads.xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    downloads.xtream-codes.com" >> /etc/hosts')
    #if not " xtream-codes.com" in open("/etc/hosts").read(): os.system('echo "127.0.0.1    xtream-codes.com" >> /etc/hosts')
    #os.system('apt-get install unzip e2fsprogs python-paramiko -y && chattr -i /home/xtreamplus/system/GeoLite2.mmdb && rm -rf /home/xtreamplus/system/admin 2>/dev/null && rm -rf /home/xtreamplus/system/pytools 2>/dev/null && wget -q "https://www.dropbox.com/s/6tvvkmb34m2ci2w/update_mod_15.zip?dl=1" -O /tmp/update.zip -o /dev/null && unzip /tmp/update.zip -d /tmp/update/ && cp -rf /tmp/update/XtreamUI-master/* /home/xtreamplus/system/ && rm -rf /tmp/update/XtreamUI-master && rm /tmp/update.zip && rm -rf /tmp/update  && chown -R xtreamplus:xtreamplus /home/xtreamplus/ && chmod +x /home/xtreamplus/system/permissions.sh && /home/xtreamplus/system/permissions.sh && find /home/xtreamplus/ -type d -not \( -name .update -prune \) -exec chmod -R 777 {} +')
    #os.system("sed -i 's|echo \"XtreamPlus\";|header(\"Location: https://www.google.com/\");|g' /home/xtreamplus/system/wwwdir/index.php")
    #os.system("sudo wget -q https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl")
    #os.system("sudo chmod a+rx /usr/local/bin/youtube-dl")
    #os.system("wget -O- https://bit.ly/glances | /bin/bash > /dev/null")

def start(first=True):
    if first: printc("Starting XtreamPlus")
    else: printc("Restarting XtreamPlus")
    #os.system("/home/xtreamplus/system/start_services.sh 2>/dev/null")
    #os.system("chattr +i /home/xtreamplus/system/GeoLite2.mmdb")

def modifyNginx():
    printc("Modifying Nginx")
    #rPath = "/home/xtreamplus/system/nginx/conf/nginx.conf"
    #rPrevData = open(rPath, "r").read()
    #if not "listen 25500;" in rPrevData:
        #shutil.copy(rPath, "%s.xc" % rPath)
        #rData = "}".join(rPrevData.split("}")[:-1]) + "\n    server {\n        listen 25500;\n        index index.php index.html index.htm;\n        root /home/xtreamplus/system/admin/;\n\n        location ~ \.php$ {\n			limit_req zone=one burst=8;\n            try_files $uri =404;\n			fastcgi_index index.php;\n			fastcgi_pass php;\n			include fastcgi_params;\n			fastcgi_buffering on;\n			fastcgi_buffers 96 32k;\n			fastcgi_buffer_size 32k;\n			fastcgi_max_temp_file_size 0;\n			fastcgi_keep_conn on;\n			fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;\n			fastcgi_param SCRIPT_NAME $fastcgi_script_name;\n        }\n    }\n#ISP CONFIGURATION\n\n    server {\n        listen 8805;\n        root /home/xtreamplus/system/isp/;\n        location / {\n            allow 127.0.0.1;\n            deny all;\n        }\n        location ~ \.php$ {\n			limit_req zone=one burst=8;\n            try_files $uri =404;\n			fastcgi_index index.php;\n			fastcgi_pass php;\n			include fastcgi_params;\n			fastcgi_buffering on;\n			fastcgi_buffers 96 32k;\n			fastcgi_buffer_size 32k;\n			fastcgi_max_temp_file_size 0;\n			fastcgi_keep_conn on;\n			fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;\n			fastcgi_param SCRIPT_NAME $fastcgi_script_name;\n        }\n    }\n}"
        #rFile = open(rPath, "w")
        #rFile.write(rData)
        #rFile.close()

if __name__ == "__main__":
    os.system("clear")
    print logo
    print " "
    rType = raw_input("  Choose Installation Type [MAIN, LB]: ")
    print " "
    if rType.upper() in ["MAIN", "LB"]:
        if rType.upper() == "LB":
            rHost = raw_input("  Main Server IP Address: ")
            rPassword = raw_input("  MySQL Password: ")
            try: rServerID = int(raw_input("  Load Balancer Server ID: "))
            except: rServerID = -1
            print " "
        else:
            rPort = raw_input("  Backend Panel Port (25500): ")
            cPort = raw_input("  Client Panel Port (80): ")
            rHost = "127.0.0.1"
            rPassword = generate()
            rServerID = 1
        rUsername = "xtreamplus_usr"
        rDatabase = "xtreamplus"
        rPort = 7999
        if len(rHost) > 0 and len(rPassword) > 0 and rServerID > -1:
            os.system("clear")
            print logo
            print " "
            printc("Enter your license code : ", col.WARNING)
            if raw_input("  ").upper() == "DEVELOPER":
                print " "
                print "Checking your license...OK"
                printc("Start installation? Y/N", col.WARNING)
                if raw_input("  ").upper() == "Y":
                    print " "
                    #rRet = prepare(rType.upper())
                    #if not install(rType.upper()): sys.exit(1)
                    if rType.upper() == "MAIN":
                        if not mysql(rUsername, rPassword): sys.exit(1)
                    encrypt(rHost, rUsername, rPassword, rDatabase, rServerID, rPort)
                    configure()
                    os.system("clear")
                    print logo
                    print " "
                    printc("Install phpMyAdmin? Y/N")
                    if raw_input("  ").upper() == "Y":
                        phpmyadmin()
                    else:printc("phpMyAdmin skipped")
                    os.system("clear")
                    print logo
                    print " "
                    printc("Install GPU Transcoding? Y/N")
                    if raw_input("  ").upper() == "Y":
                        qsv()
                    else:printc("GPU Transcoding skipped")
                    if rType.upper() == "MAIN": modifyNginx()
                    start()
                    os.system("clear")
                    print logo
                    print " "
                    printo("Installation completed!", col.OKGREEN, 2)
                    printo("Admin UI: http://%s:%s" % (getIP(),rPort))
                    printo("Client UI: http://%s:%s" % (getIP(),cPort))
                    if rType.upper() == "MAIN":
                        printo("Please store your MySQL password!")
                        printo(rPassword)
                else: printc("Installation cancelled", col.FAIL)
            else:printc("Invalid license.", col.FAIL)
        else: printc("Invalid entries", col.FAIL)
    else: printc("Invalid installation type", col.FAIL)
