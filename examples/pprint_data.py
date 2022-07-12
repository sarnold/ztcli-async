"""Get data from local ZT node API, print formatted output."""

import asyncio

import aiohttp

from ztcli_api import ZeroTier, ZeroTierConnectionError
from ztcli_api.utils import get_token, pprint


async def main():
    """Example code to retrieve data from a ZeroTier node."""
    async with aiohttp.ClientSession() as session:
        ZT_API = get_token()
        client = ZeroTier(ZT_API, loop, session)

        try:
            # get status details of the local node
            await client.get_data('status')
            print('Node status:')
            pprint(client.data)
            print(client.data.get('online'))

            # get status details of the node peers
            await client.get_data('peer')
            print('Peers found:')
            pprint(client.data)

            # get/display all available network data
            await client.get_data('network')
            print('Networks found:')
            pprint(client.data)
            for network in client.data:
                my_id = network.get('id')
                print(my_id)
                # Get details about each network
                await client.get_data('network/{}'.format(my_id))
                pprint(client.data)

                # Set a toggle for an existing network
                await client.set_value({'allowGlobal': True},
                                       'network/{}'.format(my_id))
                await client.get_data('network/{}'.format(my_id))
                print(network.get('allowGlobal'))

        except ZeroTierConnectionError as exc:
            print(str(exc))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
