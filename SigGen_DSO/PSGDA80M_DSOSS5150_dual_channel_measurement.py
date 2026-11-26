####################
## Author: RF Seeker/Het Pranav Trivedi (KJ5BEI)
## Find me: https://www.linkedin.com/company/rf-seeker/
## This code sweeps signal generator frequencies and records the output from DSO
## If this code helps you then, cheers!
####################

####################
## First thing to do is to import libraries
## Import Libraries begins. Block 1 begins

import os

import pyvisa

import serial

import time

import pandas as pd

## Done importing libraries, ready to start with code. Block 1 ends
####################

####################
## Next find out where the script is located
## This is for sanity check
## Block 2 begins

start_timestamp = time.perf_counter()
simulation_path = os.getcwd() # This command gets the current working directory and saves it to the variable names Simulation_path
print(simulation_path) # Debug step

## Found and assigned location of script. Block 2 ends 
####################

####################
## Setup necessary variables for simulation
## Block 3 begins

## Variables for signal generator

PORT = "COM3" # Set the PORT variable to COM4 after viewing in device manager
BAUDRATE = 115200 # Set the BUADRATE variable as per the instruction manual received from the equipment vendor
initial_condition = [":w10=1,0.",":w15=200."] # command variable stores the command (in string format). : starts the command, r tells it is a read operaiton, 1 is channel 1 and 3 is for frequency, = 0 tells to output \r\n are command end characters.\r is return to begining of current line and \n is new line feed
frequency_sweep_Hz = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000] # Frequency sweep in Hz
#frequency_sweep_Hz = [20000, 50000, 100000] # Frequency sweep in Hz
for index in range(len(frequency_sweep_Hz)): # Required to convert the values in mHz as accepted by ,0 by the signal generator
    frequency_sweep_Hz[index] = 1000*frequency_sweep_Hz[index] # Multiply all values in the list by 1000

#print(frequency_sweep_Hz) # Debug step

## Variables for DSO

resource_manager = pyvisa.ResourceManager("@py") # Object that manages communication with measurement instruments. It helps to discover instruments, open session, manage instruments and close the session
# PyVISA >>>>PvVISA-py indicated by the @py>>>>PyUSB/libusb>>>>Windows USB syubsytem>>>>VAR TECH DSO
resource = "USB0::1183::20574::CN2439029079400::0::INSTR" # From previous resource list finding
vertical_scale_set_ch1 = 100 # vertical scale minimum for channel 1
vertical_scale_set_ch2 = 1000 # Vertical scale miinimumm for channel 2
averaging = 8

## Empty list initialization

time_scale_list = [] # Initialize list for storing values 
vertical_scale_list = []
vpp_measure_ch1_list = []
vpp_measure_ch2_list = []
frequency_sweep_list = []
frequency_measure_ch1_list = []
frequency_measure_ch2_list = []
rising_delay_ch1_list = []
rising_delay_ch2_list = []

## Variables are set or initialized. Block 3 ends 
####################

####################
## Initialize serial communication for signal generator and resouce for DSO
## Block 4 begins

ser_comm = serial.Serial( # .Serial is a class inside module called serial
        port=PORT, # Use the port which is stored inside variable called PORT
        baudrate=BAUDRATE,# Set the buadarate to be the value stored inside variable called BUADRATE
        bytesize=serial.EIGHTBITS, # serial.EIGHTBITS is predefined constant which has 8 data bits within the PySerial module
        parity=serial.PARITY_NONE, # serial.PARITY_NONE is predefined constant which mean no parity within the PySerial module
        stopbits=serial.STOPBITS_ONE, # serial.PARITY_NONE is predefined constant which means that end of transmission data frame will be with 1 bit within the PySerial module
        timeout=0.5, # The maximum time that the read operates wait for the incoming data
        write_timeout=1) # The maximum time that the write operation waits for the data to be transmitted

test = resource_manager.open_resource(resource) # Attempts to open the specific resource and store it in test. test now becomes object through which we communicate with DSO

## Variables are set or initialized. Block 4 ends
####################

####################
## Write initial condition to signal generator
## Decode it to read it
## Block 5 begins

try: # If the code can cause an error or crash, then use this with the except 

    for command in initial_condition: # Write the initial condition commands to the signal generator

        ser_comm.reset_input_buffer() # This buffer stores data received from the signal generator. Command clears the temporary menmory which holds data to be transferred

        ser_comm.write((command + "\r\n").encode("ascii")) # The command we created was in string, this will encode the data in ASCII bytes and pass the data through serial.write
        ser_comm.flush() # This will makes sure that the transmitter thas finished transmission

        response = ser_comm.read_until(b"\n") # read_untiol is method to read unitl there is a new byte line

        print(f"Transmit: {command}") # Print transmitted command. Debug step
        print(f"Recevied: {response.decode('ascii', errors='replace').strip()}") # Will print of ASCII decoded string format and will replace any error with � and will remove any whitespace characters from begining or end. Removes spaces, tab, \r, \n 
        print("*" * 50) # For differentiating between continous print statements

        time.sleep(0.1) # Sleep for 100 ms

except Exception as crash:
    print("Communication failed:")
    print(type(crash).__name__, crash) # Extracts name of exception class and prints it
    test.close()
    resource_manager.close()
    
## Initial conditions are set. Block 5 ends
####################

####################
## Write initial condition to DSO
## Decode it to read it
## Block 6 begins

try: # If the code can cause an error or crash, then use this with the except 

    # Channel 1 settings
    test.write(":CHANnel1:DISPlay ON") # Turn on/Enable display for channel 1
    test.write(":CHAN1:BWL 1") # Turn on the bandwidth limit and attenuate signalsabove 20 MHz
    test.write(":CHAN1:COUP AC") # Make sure AC coupling is the mode. DC components will be blocked
    test.write(f":CHAN1:SCALe {vertical_scale_set_ch1}mV") # Each block on display will have vertical grid as 500 mV
    test.write(":TRIGger:EDGe:SOURce CHANnel1") # Channel to be considered as trigger source
    test.write(":TRIGger:MODE EDGE") # Set the trigger mode to edge trigger
    test.write(":TRIGger:EDGe:SLOPe RISIng") # Direction in which the signal should cross the trigger threshold - Rising edge
    test.write(":TRIGger:EDGe:LEVel 0.0") # Set the trigger voltage threshold

    # Time scale settings
    test.write(":TIMebase:SCALe 1") # Each block on display will have horizontal grid as 1 second
    
    # Channel 2 settings
    test.write(":CHANnel2:DISPlay ON") # Turn on/Enable display for channel 1
    test.write(":CHAN2:BWL 2") # Turn on the bandwidth limit and attenuate signals above 20 MHz
    test.write(":CHAN2:COUP AC") # Make sure AC coupling is the mode. DC components will be blocked
    test.write(f":CHAN2:SCALe {vertical_scale_set_ch2}mV") # Each block on display will have vertical grid as 500 mV
    #test.write(":TRIGger:EDGe:SOURce CHANnel2") # Channel to be considered as trigger source
    #test.write(":TRIGger:MODE EDGE") # Set the trigger mode to edge trigger
    #test.write(":TRIGger:EDGe:SLOPe RISIng") # Direction in which the signal should cross the trigger threshold - Rising edge
    #test.write(":TRIGger:EDGe:LEVel 0.0") # Set the trigger voltage threshold
    
    test.write(":MEASure:ENABle ON") # Enable measurments
    test.write(":ACQuire:TYPE HRESolution") # Acquistion mode is set to high resolution for frequencies less than 20 KHz

    bandwidth_limit_ch1 = test.query(":CHAN1:BWL?").strip() # Query with ?, read the value and store the value of bandwidth limit. .query() can read as well as write 
    coupling_ch1 = test.query(":CHAN1:COUP?").strip()
    time_scale_ch1 = test.query(":TIMebase:SCALe?").strip()
    vertical_scale_ch1 = test.query(":CHAN1:SCALe?").strip()
    

    print("Channel 1 bandwidth limit:", bandwidth_limit_ch1)
    print("Channel 1 coupling:", coupling_ch1)
    print("Time scale", time_scale_ch1)
    print("Channel 1 vertical scaling", vertical_scale_ch1)

    bandwidth_limit_ch2 = test.query(":CHAN2:BWL?").strip() # Query with ?, read the value and store the value of bandwidth limit. .query() can read as well as write 
    coupling_ch2 = test.query(":CHAN2:COUP?").strip()
    time_scale_ch2 = test.query(":TIMebase:SCALe?").strip()
    vertical_scale_ch2 = test.query(":CHAN2:SCALe?").strip()

    print("Channel 2 bandwidth limit:", bandwidth_limit_ch2)
    print("Channel 2 coupling:", coupling_ch2)
    print("Time scale", time_scale_ch2)
    print("Channel 2 vertical scaling", vertical_scale_ch2)

    acquisition_type = test.query(":ACQuire:TYPE?").strip()
    print("Acquisition type is", acquisition_type)

    test.write(":RUNning ON")

    time.sleep(1) # Sleep for 1 second
    
except Exception as crash:
    print("Communication failed:")
    print(type(crash).__name__, crash) # Extracts name of exception class and prints it
    test.close()
    resource_manager.close()
   
## Initial conditions are set. Block 6 ends
####################

####################
## Sweep the frequency in signal generator and measure output in DSO
## Block 7 begins

try: # If the code can cause an error or crash, then use this with the except 

    for frequency in frequency_sweep_Hz: # Sweep the frequency
        
        ser_comm.reset_input_buffer() # This buffer stores data received from the signal generator. Command clears the temporary menmory which holds data to be transferred
        command = f":w13={frequency},0" # Command to control the frequency of channel 1 in Hz
    
        ser_comm.write((command + "\r\n").encode("ascii")) # The command we created was in string, this will encode the data in ASCII bytes and pass the data through serial.write
        ser_comm.flush() # This will makes sure that the transmitter thas finished transmission

        response = ser_comm.read_until(b"\n") # read_untiol is method to read unitl there is a new byte line

        print(f"Transmit: {command}") # Print transmitted command. Debug step
        print(f"Recevied: {response.decode('ascii', errors='replace').strip()}") # Will print of ASCII decoded string format and will replace any error with � and will remove any whitespace characters from begining or end. Removes spaces, tab, \r, \n 
        print("*" * 50) # For differentiating between continous print statements
        time.sleep(1) # Sleep/Wait for 1 s
        
        time_scale_set = 1000/frequency
        test.write(f":TIMebase:SCALe {time_scale_set}") # Each block on display will have horizontal grid as 0.2 ms
        time.sleep(1)
        
        if frequency > 20000000 and frequency <= 100000000:
            test.write(f":CHAN2:SCALe 500mV") # Each block on display will have vertical grid as 400 mV for channel 1
        elif frequency > 100000000 and frequency < 1000000000:
            test.write(f":CHAN2:SCALe 200mV") # Each block on display will have vertical grid as 200 mV for channel 1
        elif frequency >= 1000000000:
            test.write(f":CHAN2:SCALe 100mV") # Each block on display will have vertical grid as 100 mV for channel 1    
        time.sleep(1)

        vertical_scale = test.query(":CHAN2:SCALe?").strip()
        time_scale = test.query(":TIMebase:SCALe?").strip()
        #print("Channel 2 vertical scaling", vertical_scale) # Debug step
        #print("Time scale", time_scale) # Debug step
        #print("Frequency swept", frequency/1000) # Debug step

        vertical_scale_list.append(float(vertical_scale))
        time_scale_list.append(float(time_scale))
        frequency_sweep_list.append(float(frequency/1000))
        #print(vertical_scale_list) # Debug step
        #print(time_scale_list) # Debug step
        #print(frequency_sweep_list) # Debug step
        
        vpp_measure_ch1_list_temp = []
        vpp_measure_ch2_list_temp = []
        frequency_measure_ch1_list_temp = []
        frequency_measure_ch2_list_temp = []
        rising_delay_ch1_list_temp = []
        rising_delay_ch2_list_temp = []

        if frequency < 5000000:

            for index in range(0,averaging):

                test.write(":TRIGger:SWEep SINGle") # Set single trigger sweep for acquistion
                trigger_sweep_status = test.query(":TRIGger:SWEep?").strip() # Find out trigger status
                print("Trigger sweep status:", trigger_sweep_status) # Debug step

                while True: # Always go in this loop. We want to find out when the acquistion is complete and the trigger status changes back to AUTO and waveform is in STOP mode. Only after that we can make reliable measurements 

                    trigger_sweep_status = test.query(":TRIGger:SWEep?").strip() # Find out trigger status

                    #print("Trigger sweep status:", trigger_sweep_status) # Debug step
           
                    if trigger_sweep_status == "AUTO": # If trigger status is AUTO
                        print("Acquisition completed!")
                        break

                    time.sleep(0.1) # Keep polling for status every 100 milliseconds

                
                vpp_measure_ch1 = test.query(":MEASure:CHANnel1:ITEM? VPP").strip()
                frequency_measure_ch1 = test.query(":MEASure:CHANnel1:ITEM? FREQuency").strip()
                vpp_measure_ch2 = test.query(":MEASure:CHANnel2:ITEM? VPP").strip()
                frequency_measure_ch2 = test.query(":MEASure:CHANnel2:ITEM? FREQuency").strip()
                rising_delay_ch1 = test.query(":MEASure:CHANnel1:ITEM? FRR").strip()
                rising_delay_ch2 = test.query(":MEASure:CHANnel2:ITEM? FRR").strip() # Dummy measurement

                print("Measured peak to peak voltage for channel 1", vpp_measure_ch1) # Debug step
                print("Measured peak to peak voltage for channel 2", vpp_measure_ch2) # Debug step
                print("Measured frequency for channel 1", frequency_measure_ch1) # Debug step
                print("Measured frequency for channel 2", frequency_measure_ch2) # Debug step
                print("Rising edge delay for channel 1", rising_delay_ch1) # Debug step
                print("Rising edge delay for channel 2", rising_delay_ch2) # Debug step

                vpp_measure_ch1_list_temp.append(float(vpp_measure_ch1))
                vpp_measure_ch2_list_temp.append(float(vpp_measure_ch2))            
                frequency_measure_ch1_list_temp.append(float(frequency_measure_ch1))
                frequency_measure_ch2_list_temp.append(float(frequency_measure_ch2))
                rising_delay_ch1_list_temp.append(abs(float(rising_delay_ch1))) # Need absolute for ch1 for low frequency
                rising_delay_ch2_list_temp.append(float(rising_delay_ch2))

                print(vpp_measure_ch1_list_temp) # Debug step
                print(vpp_measure_ch2_list_temp) # Debug step
                print(frequency_measure_ch1_list_temp) # Debug step
                print(frequency_measure_ch2_list_temp) # Debug step
                print(rising_delay_ch1_list_temp) # Debug step
                print(rising_delay_ch2_list_temp) # Debug step
        
        

            vpp_measure_ch1_average = min(vpp_measure_ch1_list_temp) # For VPP measurement we are interested in minimum of the list. Due to noise spikes some of the measurements record much higher peak to peak. However, 1 out of 8 is mostly clean
            vpp_measure_ch2_average = min(vpp_measure_ch2_list_temp)
            frequency_measure_ch1_average = sum(frequency_measure_ch1_list_temp)/len(frequency_measure_ch1_list_temp)
            frequency_measure_ch2_average = sum(frequency_measure_ch2_list_temp)/len(frequency_measure_ch2_list_temp)
            rising_delay_ch1_average = sum(rising_delay_ch1_list_temp)/len(rising_delay_ch1_list_temp)
            rising_delay_ch2_average = sum(rising_delay_ch2_list_temp)/len(rising_delay_ch2_list_temp)

            print("Averaged peak to peak voltage for channel 1", vpp_measure_ch1_average) # Debug step
            print("Averaged peak to peak voltage for channel 2", vpp_measure_ch2_average) # Debug step
            print("Averaged frequency for channel 1", frequency_measure_ch1_average) # Debug step
            print("Averaged frequency for channel 2", frequency_measure_ch2_average) # Debug step
            print("Averaged rising edge delay for channel 1", rising_delay_ch1_average) # Debug step
            print("Averaged rising edge delay for channel 2", rising_delay_ch2_average) # Debug step

            vpp_measure_ch1_list.append(float(vpp_measure_ch1_average))
            vpp_measure_ch2_list.append(float(vpp_measure_ch2_average))            
            frequency_measure_ch1_list.append(float(frequency_measure_ch1_average))
            frequency_measure_ch2_list.append(float(frequency_measure_ch2_average))
            rising_delay_ch1_list.append(float(rising_delay_ch1_average))
            rising_delay_ch2_list.append(float(rising_delay_ch2_average))

            time.sleep(0.1)

        else:

            test.write(":RUNning ON")
            trigger_sweep_status = test.query(":TRIGger:SWEep?").strip() # Find out trigger status
            print("Trigger sweep status:", trigger_sweep_status) # Debug step
            
            test.write(":ACQuire:TYPE AVERage")
            test.write(":ACQuire:COUNt 64")
            acquisition_type = test.query(":ACQuire:TYPE?").strip()
            average_count = test.query(":ACQuire:COUNt?").strip()
            print("Acquisition type is", acquisition_type)
            print("Averaging count is", average_count)

            time.sleep(4)

            vpp_measure_ch1 = test.query(":MEASure:CHANnel1:ITEM? VPP").strip()
            frequency_measure_ch1 = test.query(":MEASure:CHANnel1:ITEM? FREQuency").strip()
            vpp_measure_ch2 = test.query(":MEASure:CHANnel2:ITEM? VPP").strip()
            frequency_measure_ch2 = test.query(":MEASure:CHANnel2:ITEM? FREQuency").strip()
            rising_delay_ch1 = test.query(":MEASure:CHANnel1:ITEM? FRR").strip()
            rising_delay_ch2 = test.query(":MEASure:CHANnel2:ITEM? FRR").strip()

            print("Measured peak to peak voltage for channel 1", vpp_measure_ch1) # Debug step
            print("Measured peak to peak voltage for channel 2", vpp_measure_ch2) # Debug step
            print("Measured frequency for channel 1", frequency_measure_ch1) # Debug step
            print("Measured frequency for channel 2", frequency_measure_ch2) # Debug step
            print("Rising edge delay for channel 1", rising_delay_ch1) # Debug step
            print("Rising edge delay for channel 2", rising_delay_ch2) # Debug step
            
            vpp_measure_ch1_list.append(float(vpp_measure_ch1))
            vpp_measure_ch2_list.append(float(vpp_measure_ch2))            
            frequency_measure_ch1_list.append(float(frequency_measure_ch1))
            frequency_measure_ch2_list.append(float(frequency_measure_ch2))
            rising_delay_ch1_list.append(float(rising_delay_ch1))
            rising_delay_ch2_list.append(float(rising_delay_ch2))
            
            
except Exception as crash:
    print("Communication failed:")
    print(type(crash).__name__, crash) # Extracts name of exception class and prints it
    test.close()

finally: # This block will execute regardless which block try or except works. It is made to release the resource
    try:
        test.close() # Release the resource - DSO
    except:
        pass # Do nothing

resource_manager.close() # Close the resource manager. This is responsible for managing all the VISA resources

## Measurments are taken. Block 7 ends
####################

####################
## Convert the generated data into an excel file
## Block 8 begins
    
dataframe_time_scale = pd.DataFrame(time_scale_list, columns=['TIME_SCALE']) # Convert the list to dataframe with specified column name
dataframe_vertical_scale = pd.DataFrame(vertical_scale_list, columns=['VERTICAL_SCALE']) # 
dataframe_vpp_measure_ch1 = pd.DataFrame(vpp_measure_ch1_list, columns=['VPP_MEASURE_CH1'])
dataframe_vpp_measure_ch2 = pd.DataFrame(vpp_measure_ch2_list, columns=['VPP_MEASURE_CH2'])
dataframe_frequency_sweep = pd.DataFrame(frequency_sweep_list, columns=['FREQUENCY_SWEEP'])
dataframe_frequency_measure_ch1 = pd.DataFrame(frequency_measure_ch1_list, columns=['FREQUENCY_MEASURE_CH1'])
dataframe_frequency_measure_ch2 = pd.DataFrame(frequency_measure_ch2_list, columns=['FREQUENCY_MEASURE_CH2'])
dataframe_rising_delay_ch1 = pd.DataFrame(rising_delay_ch1_list, columns=['RISING_DELAY_CH1'])
dataframe_rising_delay_ch2 = pd.DataFrame(rising_delay_ch2_list, columns=['RISING_DELAY_CH2'])

dataframe_combined = pd.concat([dataframe_time_scale, dataframe_vertical_scale, dataframe_vpp_measure_ch1, dataframe_vpp_measure_ch2, dataframe_frequency_sweep, dataframe_frequency_measure_ch1, dataframe_frequency_measure_ch2, dataframe_rising_delay_ch1, dataframe_rising_delay_ch2], axis=1) # Merge the dataframe in a way that columns are side by side
dataframe_combined.to_excel('DSO_data.xlsx', index=False) # Convert the combined dataframe to excel and do not include the index

end_timestamp = time.perf_counter() # Time step at end
time_taken = end_timestamp - start_timestamp # Total time for code run in seconds
print('Time taken by code is {:.6f} seconds'.format(time_taken))

## Final block ends. Enjoy!
####################

