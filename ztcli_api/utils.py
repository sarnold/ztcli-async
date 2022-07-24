"""ZT platform and JSON/file handling utilities."""

import json
import os
import random
import string
import sys
from pathlib import Path


def pprint(obj):
    """
    Pretty printer for JSON.

    :param opj: JSON obj
    """
    print(json.dumps(obj, indent=2, separators=(',', ': ')))


def json_dump_file(endpoint, data, dirname=None):
    """
    Dump JSON endpoint data to a named file and, optionally, to a target
    directory.

    :param endpoint: ZT endpoint name => filename
    :param data: endpoint data to dump
    :param dirname: target directory name
    """
    if dirname:

        def opener(dirname, flags):
            return os.open(dirname, flags, dir_fd=dir_fd)

        dir_fd = os.open(dirname, os.O_RDONLY)
    else:
        opener = None

    dump_json(endpoint, data, opener=opener)


def json_load_file(endpoint, dirname=None):
    """
    Load JSON endpoint data from a named file and, optionally, a target
    directory.

    :param endpoint: ZT endpoint name => filename
    :param dirname: target directory name
    """
    if dirname:

        def opener(dirname, flags):
            return os.open(dirname, flags, dir_fd=dir_fd)

        dir_fd = os.open(dirname, os.O_RDONLY)
    else:
        opener = None

    data = load_json(endpoint, opener=opener)
    return data


def dump_json(endpoint, data, opener=None):
    """Dump JSON endpoint data to a file using optional ``opener``."""
    with open(endpoint + '.json', 'w', encoding='utf-8', opener=opener) as f_ptr:
        json.dump(data, f_ptr)
    print(f'{endpoint} data saved to {endpoint}.json')


def load_json(endpoint, opener=None):
    """Load JSON endpoint data from a file using optional ``opener``."""
    with open(endpoint + '.json', 'r', encoding='utf-8', opener=opener) as f_ptr:
        data = json.load(f_ptr)
    print(f'{endpoint} data read from {endpoint}.json')
    return data


def name_generator(
    size=10, chars=string.ascii_lowercase + string.digits, no_sep=False
):
    """Generate random ZeroTier network names"""
    str1 = ''.join(random.choice(chars) for _ in range(size))
    str2 = ''.join(random.choice(chars) for _ in range(size))
    if no_sep:
        return str1
    return str1 + '_' + str2


def get_token(zt_home=None):
    """
    Get ZeroTier authentication token (requires root or user acl).

    :param zt_home: non-std path to ZT home directory
    :return zt_auth: contents of ZT authtoken file or None
    """
    zt_auth = None

    if not zt_home:
        zt_home = get_platform_path()
    else:
        zt_home = Path(zt_home)
    if zt_home.exists():
        zt_auth = zt_home.joinpath('authtoken.secret').read_text(encoding='utf-8')

    return zt_auth


def get_platform_path():
    """
    Find platform path to ZT home directory (where the authtoken lives).

    :return: path to ZT home as Path obj
    """
    name = sys.platform

    platform_paths = {
        'win32': Path('C:\\ProgramData\\ZeroTier\\One'),
        'linux': Path('/var/lib/zerotier-one'),
        'darwin': Path('/Library/Application Support/ZeroTier/One'),
        'bsd': Path('/var/db/zerotier-one'),
    }

    plat_name = [x for x in platform_paths if x in name]

    return platform_paths[plat_name[0]]
