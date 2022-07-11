# coding: utf-8
"""A Python async client wrapper for the zerotier-cli node API."""
import json
import logging
import asyncio

import aiohttp
import async_timeout

from .exceptions import ZeroTierError
from .exceptions import ZeroTierConnectionError
from .exceptions import ZeroTierNoDataAvailable


__all__ = [
    'WRITABLE_NETWORK',
    'WRITABLE_MEMBER',
    'WRITABLE_NODE',
    'ZeroTier',
    'ZeroTierError',
    'ZeroTierConnectionError',
    'ZeroTierNoDataAvailable',
]

WRITABLE_NETWORK = [
    'name',
    'private',
    'enableBroadcast',
    'v4AssignMode',
    'v6AssignMode',
    'mtu',
    'multicastLimit'
    'routes',
    'ipAssignmentPools',
    'rules',
    'capabilities',
    'tags',
    'remoteTraceTarget',
    'remoteTraceLevel',
]

WRITABLE_MEMBER = [
    'authorized',
    'activeBridge',
    'ipAssignments',
]

WRITABLE_NODE = [
    'allowManaged',
    'allowGlobal',
    'allowDefault',
]


class ZeroTier:
    """
    Async class to create a ZeroTier-cli connection object to get, set,
    and delete endpoint-specific data. Writable items for each endpoint
    are exported.
    """

    def __init__(self, api_token, loop, session, host='localhost', port=9993):
        """Initialize the connection."""
        self._loop = loop
        self._session = session
        self.headers = {'X-ZT1-Auth': api_token}
        self.data = None
        self.url = f'{host}:{port}'

    async def get_data(self, endpoint):
        """Send a GET request to JSON API ``endpoint``."""
        try:
            with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(
                    f'http://{self.url}/{endpoint}',
                    headers=self.headers)

            logging.debug("Response status: %s", response.status)
            self.data = await response.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as exc:
            logging.debug("Cannot load data from ZeroTier node")
            raise ZeroTierConnectionError('Cannot connect to ZeroTier API') from exc

    async def set_value(self, cfg_dict, endpoint):
        """Send a POST request to JSON API ``endpoint``."""
        payload = json.dumps(cfg_dict, separators=(',', ':'))
        logging.debug("Using payload: %s", payload)
        try:
            with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.post(
                    f'http://{self.url}/{endpoint}',
                    headers=self.headers, data=payload)

            logging.debug("Response status: %s", response.status)
            self.data = await response.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as exc:
            logging.debug("Cannot update entry of ZeroTier node")
            raise ZeroTierConnectionError('Cannot connect to ZeroTier API') from exc

    async def delete_thing(self, endpoint):
        """Send a DELETE request to JSON API ``endpoint``."""
        try:
            with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.delete(
                    f'http://{self.url}/{endpoint}',
                    headers=self.headers)

            logging.debug("Response status: %s", response.status)
            self.data = await response.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as exc:
            logging.debug("Cannot delete entry from ZeroTier node")
            raise ZeroTierConnectionError('Cannot connect to ZeroTier API') from exc
