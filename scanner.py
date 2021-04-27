from multiprocessing import Process
import pyfiglet
import sys
import socket
from datetime import datetime
from time import sleep
import threading

ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

# Defining a target
if len(sys.argv) >= 2:
    target = socket.gethostbyname(sys.argv[1])
else:
	print("Invalid ammount of Argument")
	sys.exit()
if len(sys.argv) >= 3:
	if(sys.argv[2] == "T"):
		debug = True
	else:
		debug = False
else:
	debug = False
if len(sys.argv) == 4:
	timeout = float(sys.argv[3])
else:
	timeout = 2.5

def scan_a_port(port, target):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if(debug == True):
		print("Scanning %s" % (port))
	socket.setdefaulttimeout(0.01)
	result = s.connect_ex((target,port))
	if result ==0:
		print("[*] Port {} is open".format(port))
	s.close()

def run_with_limited_time(func, args, kwargs, time):
    """Runs a function with time limit

    :param func: The function to run
    :param args: The functions args, given as tuple
    :param kwargs: The functions keywords, given as dict
    :param time: The time limit in seconds
    :return: True if the function ended successfully. False if it was terminated.
    """
    p = Process(target=func, args=args, kwargs=kwargs)
    p.start()
    p.join(time)
    if p.is_alive():
        p.terminate()
        return False

    return True

# Add Banner
print("-" * 50)
print("Scanning Target: " + target)
print("Debug: %s" % (debug))
print("Timeout %s" % (timeout))
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)
threads = []
try:
	h = 0
	for port in range(1,65535):
		if(port + h > 65535):
			sys.exit()
		threads.clear()
		for i in range(50):
			prt = port + i + h
			t = threading.Thread(target=run_with_limited_time, args=(scan_a_port, (prt, target,), {}, timeout,))
			t.daemon = True
			threads.append(t)
		for i in range(50):
			threads[i].start()
		for i in range(50):
			threads[i].join()
		h += 50
except KeyboardInterrupt:
        print("\n Exitting Program !!!!")
        sys.exit()
except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()
print(" - " * 50)
print("END");
