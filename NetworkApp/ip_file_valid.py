import os.path
import sys

# Checking ip file content and validity

def ip_file_valid():

    ip_file = input("\n# Enter IP file path and name : ")
    
    # Check if ip_file is in the location
    if os.path.isfile(ip_file) == True :
        print("\n IP file is valid ! \n")
        
    else :
        print("The file {} does not exist. Please check and try again. \n". format(ip_file))
        sys.exit()
    
    # open ip_file in read mode
    # read ("file_name","r")
    selected_ip_file = open(ip_file,'r')
     
    #file_name.seek(0) To set the cursor from the beginning of the file
    selected_ip_file.seek(0)
    
    #readlines()= save in a list
    ip_list = selected_ip_file.readlines()
    
    #close the file
    selected_ip_file.close()
    
    return ip_list

#ip_file_valid()