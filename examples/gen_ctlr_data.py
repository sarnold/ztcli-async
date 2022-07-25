"""
Get data from local ZT node API and create some networks. Requires ZT
node running as network controller
"""

import asyncio

import aiohttp

from ztcli_api import ZeroTier, ZeroTierConnectionError
from ztcli_api.utils import get_token, name_generator, pprint


async def main():
    """
    Generate a bunch of networks on a ZeroTier network controller node.
    """
    async with aiohttp.ClientSession() as session:
        ZT_API = get_token()
        client = ZeroTier(ZT_API, loop, session)

        try:
            await client.get_data('status')
            node_data = client.data
            ctlr_id = node_data.get('address')

            # create some networks
            endpoint = 'controller/network/{}'.format(ctlr_id + '______')
            for N in range(100):
                net_name = name_generator()
                await client.set_value('name', net_name, endpoint)

            # get/display all available network data
            await client.get_data('controller/network')
            print('{} networks found'.format(len(client.data)))
            pprint(client.data)

        except ZeroTierConnectionError as exc:
            print(str(exc))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
