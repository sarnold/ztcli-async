"""
A Python async client wrapper for the zerotier-cli node API.
"""

import asyncio
import json
import logging

import aiohttp
import async_timeout

from ._version import __version__

__all__ = [
    '__version__',
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
    'multicastLimit',
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


class ZeroTierError(Exception):
    """General ZeroTierError exception occurred."""


class ZeroTierConnectionError(ZeroTierError):
    """Raise when a connection error is encountered."""


class ZeroTierNoDataAvailable(ZeroTierError):
    """Raise when no data is available."""


class ZeroTier:
    """
    Async class to create a ZeroTier-cli connection object to get, set,
    and delete endpoint-specific data. Writable items for each endpoint
    are exported.
    """

    def __init__(self, api_token, loop, session, port=9993):
        """Initialize the connection."""
        self._loop = loop
        self._session = session
        self.headers = {'X-ZT1-Auth': api_token}
        self.data = None
        self.url = f'localhost:{port}'

    async def get_data(self, endpoint):
        """Send a GET request to JSON API ``endpoint``."""
        try:
            with async_timeout.timeout(5):
                response = await self._session.get(
                    f'http://{self.url}/{endpoint}', headers=self.headers
                )

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
            with async_timeout.timeout(5):
                response = await self._session.post(
                    f'http://{self.url}/{endpoint}',
                    headers=self.headers,
                    data=payload,
                )

            logging.debug("Response status: %s", response.status)
            self.data = await response.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as exc:
            logging.debug("Cannot update entry of ZeroTier node")
            raise ZeroTierConnectionError('Cannot connect to ZeroTier API') from exc

    async def delete_thing(self, endpoint):
        """Send a DELETE request to JSON API ``endpoint``."""
        try:
            with async_timeout.timeout(5):
                response = await self._session.delete(
                    f'http://{self.url}/{endpoint}', headers=self.headers
                )

            logging.debug("Response status: %s", response.status)
            self.data = await response.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as exc:
            logging.debug("Cannot delete entry from ZeroTier node")
            raise ZeroTierConnectionError('Cannot connect to ZeroTier API') from exc
