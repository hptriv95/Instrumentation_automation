####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code lists connected ports and finds out if any CH340 device is connected to any port
## This is for signal generator detection
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import serial.tools.list_ports # Scans and lists serial ports

## Done importing libraries, ready to start with code. Block 1 ends
####################

####################
## Next find out where the script is located
## This is for sanity check
## Block 2 begins

simulation_path = os.getcwd() # This command gets the current working directory and saves it to the variable names Simulation_path
print(simulation_path) # Debug step

## Found and assigned location of script. Block 2 ends 
####################

####################
## Setup necessary variables for simulation
## Block 3 begins

ports_list = serial.tools.list_ports.comports()
#print(len(ports_list)) # Debug step
required_port = None # No fixed port is assigned

## Variables are set or initialized. Block 3 ends
####################

####################
## Find out on if equipment is connected and on which port
## Block 4 begins

for ports in ports_list: # for number of elements in the ports_list
    print(f'{ports.device} - {ports.description}') # Fetches the name of the HW on serial port and its description
    if 'CH340' in ports.description: # If 'CH340' is detected in the name of the hardware then store it in a variable called required_port. This is to check detection
        required_port = ports.device

if required_port is None: # If no value is asdsigned to required_port
    print('CH340 is not detected')
    sys.exit() # Exit the script
    

## Final block ends.Enjoy!
####################
