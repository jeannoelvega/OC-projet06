# MODULES 
# Allows to launch commands with the system
import subprocess

# Allows to use common commands of all OS
import os

# Allows logging and rotation
import logging
import logging.handlers
import time

# Logging settings
logFile = 'projet06.log'

# Set up a specific logger with our desired output level
myLogger = logging.getLogger('projet06.py')
myLogger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(logFile, mode='a', maxBytes=1000, backupCount=2, encoding='utf-8')
handler.setFormatter(formatter)
myLogger.addHandler(handler)

# FUNCTIONS

# Function for cleaning temporary files
def removeTemp():
    if os.path.exists('tempFile.txt'):
        os.remove('tempFile.txt')

    if os.path.exists('yamlFile.yml'):
        os.remove('yamlFile.yml')
    myLogger.info('Cleaning of temporary files done')


# Function that retrieves the IP address of a free pc
def serverChoice():
    word = "free"  # text to search
    try:
        tempFile = open("tempFile.txt", "r")  
        ipfind = False                     # for the moment, we have not found an IP
        for line in tempFile:              # browse tempFile.txt
            if word in line:               # if we find the word "free"...
                ipfind = True              # ...we have an IP address
                global adressIp
                adressIp = line.split()    # split the line into a list of character strings
                adressIp.remove( "free")   # remove the word "free" from the list
                global adrIp
                adrIp = adressIp
                break
        tempFile.close()
    except:
        myLogger.error('an error occurred while retrieving the IP address')

    if ipfind == False:     #  si on n'a pas trouvé d'adresse IP free
        print("there is no more free IP address")
        myLogger.error("there is no more free IP address")
        exit()

    myLogger.info('End of IP address processing')
    return adrIp

# Function that changes the line where the IP was free to IP used
def ipModify(adrIp):                 
    adrIp = ' '.join(adrIp)                     # put adrIp in string format
    word = adrIp  
    try:
        tempFile = open("tempFile.txt", "r")    # open tempFile.txt as read-only
        ipFile = open("ipFile.txt", "w")        # open ipFile.txt for writing
        for line in tempFile:                   # read each line of tempFile.txt in a for loop
            if word in line:                    # if the IP address is in the line...
                adressIp = line.split()         # split the line into a string list
                adressIp.remove( "free")        # remove the word "free" from the list
                adressIp = ' '.join(adressIp)   # transform the list into a string
                adressIp = adressIp + "\n"      # add a line break
                line = adressIp                 # put the IP address alone in the line variable
            ipFile.write(line)                  # write line to ipFile.txt
        tempFile.close()                        # close tempFile.txt
        ipFile.close()                          # close ipFile.txt
    except:
        myLogger.error('Problem with tempFile.txt and/or ipFile.txt')

    myLogger.info('ipFile.txt modified correctly')

# Function that creates the temporary yaml file to launch the Ansible command
def createFichyaml(adrIp):
    try:
        adrIp = ' '.join(adrIp)
        ipFile = open(plbook, "r")              # open yaml template read-only
        line = ipFile.readlines()               # save each line to a list
        ipFile.close()                          # close the yaml template
        line[1] = "- hosts: " + adrIp + "\n"    # modify the second line with the IP address found
    except:
        myLogger.error('invalid path')

    
    try:
        tempFile = open("yamlFile.yml", "w")    # open yamlFile.yml for writing
        tempFile.writelines(line)               # copy the lines
        tempFile.close()                        # close yamlFile.yml
    except:
        myLogger.error("Problem writing to yamlFile.yml file")

    myLogger.info('Creation of temporary file yamlFile.yml completed')

# Function that creates a temporary file for finding
# and changing the state of IP addresses
def copyfile():
# copy the IP addresses file identically to a temporary file
    try:
        ipFile = open("ipFile.txt", "r")
        tempFile = open("tempFile.txt", "w")
        tempFile.write(ipFile.read() )
        ipFile.close()
        tempFile.close()
    except:
        myLogger.error('problem copying ipFile.txt to tempFile.txt')

    myLogger.info('Creation of copy of ipFile.txt completed')

# Function that installs playbooks
def installPlaybook(adrIp):
    try:
        subprocess.call(["ansible-playbook", "/root/yamlFile.yml"])
        print("Service installed at " + str(adrIp) )
        myLogger.info("Service installed at " + str(adrIp) )
    except:
        myLogger.error('Problem with launching yamlFile.yml playbook')

# Main function which launches the other functions in order
def myProgram():

    copyfile()
    ipAdress = serverChoice()
    ipModify(ipAdress)
    createFichyaml(ipAdress)
    installPlaybook(ipAdress)
    removeTemp()

########################## MENU ################################################################

myLogger.info('start of project06.py')
# Creation of empty dictionaries
serviceList = {}
playbookList = {}

# Filling dictionaries with our menu
try:
    fileini = open("config.ini", "r")       # opening our menu configuration file
    for line in fileini :
        key = int(line.split()[0])          # get the number
        name = line.split()[1]              # get the service name
        path = line.split()[2]              # get playbook model path
        serviceList[key] = name             # put the service names in the correct dictionary
        playbookList[key] = path            # put the paths in the correct dictionary
    fileini.close()
except:
    myLogger.error('Problem with config.ini file')

# get the number of items in our menu
sizeDic = len(serviceList)

# displays our menu
print('\n\nAutomatic installation of services\n\n')
for key, val in serviceList.items():
    print(key, " - ", val)

print(0, " - exit")                          # Add program exit

# Choice loop with error handling
inputVal = input("\nChoose a service to install automatically:\n ")
inputVal = int(inputVal)
try:
    if inputVal == 0:
        exit(0)
    elif inputVal > sizeDic:
        print("This choice is not in the list")
    else:
        plbook = playbookList[inputVal]
        myProgram()

except:
    myLogger.error('aborted script')
