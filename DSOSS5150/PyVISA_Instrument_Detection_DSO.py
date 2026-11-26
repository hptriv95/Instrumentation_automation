####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code will confirm the working of PyUSB and libusb-1 for DSO detection
## it lists connected USB devices Vendor and Product IDs to match to DSO
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os


import usb.core
import usb.backend.libusb1

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
## Find out if DSO gets detected using its VID and PID
## Block 3 begins


backend = usb.backend.libusb1.get_backend() # .backend provides the interface between PyUSB and the USB library on PC. .libusb1 is the backend implementaiton which we want. It handles discovery of USB devices, accessing interfaces, transfering data, etc. .backend() searches for the libusb-1.0 , loads it and creates backend interfacev 

if backend is None:
    print("ERROR: libusb1 backend unavailable") # If the attempt to load libusb library fails then backend is None
else:
    print("libusb1 backend loaded successfully") # If the backend object got created successfully

    devices = usb.core.find( # Funciton searches for the USB devices connected to computer
        find_all=True, # Return all USB devices 
        backend=backend # Tells which backend to use for USB communication
    )

    print("\nConnected USB devices:\n") # Print the heading

    found = False # Initializes a boolean variable to flag the discovery of our DSO

    for instrument in devices: # Loop through the devices
        print(f"VID: {instrument.idVendor:04X} | PID: {instrument.idProduct:04X}") # Print the respective Vendor ID and Product ID in 4 digit hexadecimal format

        if instrument.idVendor == 0x049F and instrument.idProduct == 0x505E: # If the Vendor ID and Product ID match 
            found = True
            print("\nVAR TECH SS-5150 DSO FOUND!")
            print(f"Serial number: {instrument.serial_number}\n")

    if not found: # If found variable is still 0
        print("\nVAR TECH DSO not found.")


## Final block ends.Enjoy!
####################
