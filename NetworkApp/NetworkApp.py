import paramiko
import sys
import os.path
import re

from ip_file_valid import ip_file_valid
from ip_addr_valid import ip_addr_valid
from ip_reach import ip_reach
from ssh_connection import ssh_connection
from create_threads import create_threads

#Saving the list of IP addresses in ip.txt to a variable
ip_list = ip_file_valid()

#Verifying validity of each ip
try:
    ip_addr_valid(ip_list)
except KeyboardInterrupt :
    print("\n* Program aborted by user. Exiting....")
    sys.exit()
    
#Verifying reachability
try: 
    ip_reach(ip_list)
except KeyboardInterrupt:
    print("\n* Program aborted by user. Exiting....")
    sys.exit()
    
#Calling threads creation function for multiple SSH connections
create_threads(ip_list, ssh_connection)

#END