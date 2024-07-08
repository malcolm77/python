import asyncio
import os
import os
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = "malcolmchalmers@hotmail.com" # os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = "Stargat3" # os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"


async def main():
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD, api_base_url="https://iot.meross.com")

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS310 devices that are registered on this account
    await manager.async_device_discovery()
    plugs = manager.find_devices(device_type="mss210")
    pplugs = manager.find_devices(device_type="mss210p")

    if len(plugs) < 1:
        print("No MSS310 plugs found...")
    else:
        # Turn it on channel 0
        # Note that channel argument is optional for MSS310 as they only have one channel
        dev = plugs[0]

        # Update device status: this is needed only the very first time we play with this device (or if the
        #  connection goes down)
        await dev.async_update()

        # Smart Plug #4 (mss210): OnlineStatus.ONLINE ( 2201055377768890865248e1e98469d4 )
        # Smart Plug #1 Party Lights (mss210): OnlineStatus.ONLINE ( 2106075239879690852248e1e9722751 )
        # Smart Plug #3 Werebear (mss210): OnlineStatus.ONLINE ( 2106074309706690852248e1e97229bb )
        # Smart Plug #2 DL360 (mss210p): OnlineStatus.ONLINE ( 2309069934761851070348e1e9d98391 )
        # Smart Plug #6 (mss210p): OnlineStatus.ONLINE ( 2311169817714451070148e1e9e1eb9c )
        # Smart Plug #5 heater (mss210p): OnlineStatus.ONLINE ( 2311165157777351070148e1e9e1ed4a )

        WEREBEAR = "2106074309706690852248e1e97229bb"
        PLUG6 = "2311169817714451070148e1e9e1eb9c"

        for plug in pplugs: 
          print(plug.uuid)
          if (plug.uuid == PLUG6):
              print(f"------------- PLUG6 -------------------------------------")
              print(f"Turning off {dev.name}...")
              await plug.async_turn_off(channel=0)
              print("Waiting a bit before turing it on")
              await asyncio.sleep(5)
              print(f"Turing on {dev.name}")
              await plug.async_turn_on(channel=0)

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.stop()
