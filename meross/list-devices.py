import asyncio
import os
import logging

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = "malcolmchalmers@hotmail.com" #os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = "Stargat3" #os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"

meross_root_logger = logging.getLogger("meross_iot")
meross_root_logger.setLevel(logging.WARNING)


async def main():
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD, api_base_url="https://iot.meross.com")

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Discover devices.
    await manager.async_device_discovery()
    meross_devices = manager.find_devices()

    # Print them
    print("I've found the following devices:")
    for dev in meross_devices:
        print(f"- {dev.name} ({dev.type}): {dev.online_status} ( {dev.uuid} )")

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.stop()
