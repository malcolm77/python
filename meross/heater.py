#!/usr/bin/env python3
import os
import glob
import time
import asyncio
import logging
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

######### SETUP ############ 
EMAIL = "malcolmchalmers@hotmail.com" # os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = "Stargat3" # os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"
meross_root_logger = logging.getLogger("meross_iot")
meross_root_logger.setLevel(logging.ERROR)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
ON  = 1
OFF = 0
plug_state = True
Smart_Plug_4 = "2201055377768890865248e1e98469d4"

MAX = 19      # this or more and the heater turns off
MIN = 18      # less than this and the heater turns on

 
### Get raw temperature ### 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

### Calculate temp based on raw temp ??? ### 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c  # , temp_f

async def toggle_power(pwr_state):
    global plug_state   # make sure to use the global varitable, not create a new local one. stupid python  

    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD, api_base_url="https://iot.meross.com")

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS310 devices that are registered on this account
    await manager.async_device_discovery()
    mss210_plugs = manager.find_devices(device_type="mss210")
    mss210p_plugs = manager.find_devices(device_type="mss210p")
    plugs = mss210_plugs + mss210p_plugs

    if len(plugs) < 1:
        print("No MSS310 plugs found...")
    else:
        dev = plugs[0]
        await dev.async_update()

        for plug in plugs: 
          if (plug.uuid == Smart_Plug_4):
              # print(f"------------- " + plug.name + " -------------------------------------")
            if pwr_state == OFF:
                print(f"!!! Turning OFF {plug.name} !!!")
                await plug.async_turn_off(channel=0)
                await plug.async_update()
                plug_state = plug.is_on(channel=0)

              # print("Waiting a bit before turing it on")
              # await asyncio.sleep(5)
            if pwr_state == ON:
                print(f"!!! Turing on {plug.name} !!!")
                await plug.async_turn_on(channel=0)
                await plug.async_update()
                plug_state = plug.is_on(channel=0)

            if pwr_state == 2:
                await plug.async_update()
                plug_state = plug.is_on(channel=0)
                # print(plug_state)
                # print("local state: " + str(plug_state) )

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

# def show_state(current_state):
#     if current_state == ON:
#         return "ON"
#     else:
#         return "OFF"

def get_state():
    asyncio.run( toggle_power(2) )
    if plug_state == True:
        return "ON"
    elif plug_state == False:
        return "OFF"
    else:
        return "UNKNOWN"


def main():
    # power_state = OFF

    print ("--------------- START ----------------------")
    # asyncio.run( toggle_power(2) ) # get current state and set global variable to value
    print ( "Initial plug state: " + get_state() ) 						# print global value
    print ("----------------- END --------------------")

    while True:
            temperature = read_temp()
            print(f"Current temperature: {temperature:.3f} heater is: {get_state()} ")
        
            if temperature < MIN and plug_state == False: # power_state == OFF: # plug_state == False:
                    print("!!!    Temperature low      !!!")
                    print("!!!   Turning ON heater     !!!") 
                    # power_state = ON
                    asyncio.run( toggle_power(ON) )

            if temperature >= MAX and plug_state == True:   # power_state == ON: # plug_state == True:
                    print("!!!     Temperature high    !!!")
                    print("!!!    turning OFF heater   !!!") 
                    # power_state = OFF
                    asyncio.run( toggle_power(OFF) )

            time.sleep(10)



if __name__ == '__main__':
    main()

# except IOError as e:
#     logging.info(e)
# 
# except KeyboardInterrupt:
#     logging.info("ctrl + c:")
#     epd2in13_V3.epdconfig.module_exit(cleanup=True)
#     exit()

