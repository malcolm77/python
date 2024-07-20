#!/usr/bin/env python3
import asyncio
import os
import os
import logging
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = "malcolmchalmers@hotmail.com" # os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = "Stargat3" # os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"

meross_root_logger = logging.getLogger("meross_iot")
meross_root_logger.setLevel(logging.ERROR)

plug_state = True

async def get_state():
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

        Smart_Plug_4 = "2201055377768890865248e1e98469d4"

        for plug in plugs: 
            if (plug.uuid == Smart_Plug_4):
                await plug.async_update()
                global plug_state 
                plug_state = plug.is_on(channel=0)
                print( "get_state: " + str(plug_state) )


def main():
    asyncio.run( get_state() )
    print( "main: " + str(plug_state) ) 

if __name__ == '__main__':
    main()
