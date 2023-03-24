import paramiko
import os.path
import re
import time
import sys

#Checking username and password file
user_file = input("\n# Enter user file path and name : ")

if os.path.isfile(user_file) == True :
    print("\n* Username/password file is valid ! \n")
else:
    print("\n* The file {} does not exist. Please check and try again ".format(user_file))
    sys.exit()
    
#Checking commands file
cmd_file = input("\n# Enter commands file path and name : ")

#checking validity
if os.path.isfile(cmd_file) == True :
    print("\n* Command file is valid ! \n")
else:
    print("\n* Command file {} is invalid. Please check and try again ".format(cmd_file))
    sys.exit()

#Open SSHv2 connection to the device
def ssh_connection(ip):
    global user_file
    global cmd_file
    
    #Creating SSH connection
    try:
        #Define SSH parameters
        selected_user_file = open(user_file, 'r')
        selected_user_file.seek(0) #Setting cursor at the beginning of the file
        #Reading username from the file
        username = selected_user_file.readlines()[0].split(',')[0].rstrip("\n")
        selected_user_file.seek(0)
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        
        #Logging into device
        session = paramiko.SSHClient()
        
        #For testing purposes, this allows auto-accepting unknown host keys 
        #Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Connecting to device using username and password
        session.connect(ip.rstrip("\n"), username = username, password = password)
        #start and interactive shell session on the router
        connection = session.invoke_shell()
        
        #Setting terminal length for entire output - disable pagination
        connection.send("enable\n")
        connection.send("terminal length 0\n") #for commands having longer output
        time.sleep(1)
        
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        
        selected_cmd_file = open(cmd_file, 'r')
        selected_cmd_file.seek(0)
        
        #Writing each line in the commands file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
            
        #Closing used files
        selected_user_file.close()
        selected_cmd_file.close()
        
        #Checking command output for IOS syntax errors
        router_output = connection.recv(65535)
        
        if re.search(b"% Invalid input",router_output):
            print("\n* There was atleast one IOS syntax error on device {} ".format(ip))
        else:
            print("\n Done for device {} \n".format(ip))
        
        #Test for reading command output
        print(str(router_output) + "\n")  #Desired parameters can be extracted from router output
        
        
        #Closing the connection
        session.close()
        
    except paramiko.AuthenticationException:
        print("* Invalid username or password. Please check the username and password file or the device configuration")
        print("Closing the program.............")
        
        