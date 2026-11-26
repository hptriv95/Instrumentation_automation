####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code uses PyVISA to connect and verify access to DSO
## Resource ID finding is the main goal here
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import pyvisa

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
## Find out on if equipment is connected and on which port
## Block 3 begins

resource_manager = pyvisa.ResourceManager("@py") # Object that manages communication with measurement instruments. It helps to discover instruments, open session, manage instruments and close the session
# PyVISA >>>>PvVISA-py indicated by the @py>>>>PyUSB/libusb>>>>Windows USB syubsytem>>>>VAR TECH DSO
print("Available USB resources:")
print(resource_manager.list_resources()) # Print available VISA resources. Vendor ID and Product ID will be printed in decimal rather than hexadecimal. This resource ID would be used to connect

resource_manager.close() # Close the resource manager and release the resource

## Final block ends.Enjoy!
####################
