# coding: utf-8
"""Get data from local ZT node API and dump to endpoint-named files."""

import os

import asyncio
import aiohttp

from ztcli_api import ZeroTier, ZeroTierConnectionError
from ztcli_api.utils import pprint, get_token, json_dump_file, json_load_file, dump_json, load_json


VERBOSE = os.getenv('VERBOSE', default='1')


async def main():
    """Example code to retrieve data from a ZeroTier node."""
    async with aiohttp.ClientSession() as session:
        ZT_API = get_token()
        client = ZeroTier(ZT_API, loop, session)

        try:
            # get status details of the local node
            await client.get_data('status')
            json_dump_file('status', client.data)
            status_data = json_load_file('status')
            if VERBOSE:
                pprint(status_data)

            # get status details of the node peers
            await client.get_data('peer')
            dump_json('peer', client.data)
            peer_data = load_json('peer')
            if VERBOSE:
                pprint(peer_data)

            # get/display all available network data
            await client.get_data('network')
            dump_json('network', client.data)
            net_data = load_json('network')
            if VERBOSE:
                pprint(net_data)

        except ZeroTierConnectionError as exc:
            print(str(exc))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
