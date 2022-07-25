import json
import os
import string
from pathlib import Path

import pytest

from ztcli_api.utils import (
    get_platform_path,
    get_token,
    json_dump_file,
    json_load_file,
    name_generator,
    platform_check,
)


class mock_zt_api_client(object):
    """
    Client API to serve simple GET data endpoints
    """
    def __init__(self):
        self.test_dir = 'test/test_data'
        self.response = '200'

    def get_data(self, endpoint):
        self.endpoint = json_load_file(endpoint, self.test_dir)
        return self.response, self.endpoint


client = mock_zt_api_client()


# special test cases
def json_check(data):
    json_dump = json.dumps(data, indent=4, separators=(',', ': '))
    json_load = json.loads(json_dump)
    assert data == json_load


def load_data():
    _, node = client.get_data('status')
    _, peers = client.get_data('peer')
    _, nets = client.get_data('network')

    return node, peers, nets


def test_dump_and_load_json(tmp_path):
    (node_data, peer_data, net_data) = load_data()
    json_dump_file('node', node_data, tmp_path)
    node_dump = json_load_file('node', tmp_path)
    json_check(node_dump)
    json_check(peer_data)
    json_check(net_data)


def test_dump_and_load_json_not_posix(tmp_path):
    (node_data, peer_data, net_data) = load_data()
    json_dump_file('node', node_data, tmp_path, False)
    node_dump = json_load_file('node', tmp_path, False)
    json_check(node_dump)
    json_check(peer_data)
    json_check(net_data)


def test_name_generator():
    name = name_generator()
    assert len(name) == 21
    assert name.isprintable()


def test_name_generator_no_sep():
    name = name_generator(size=24, no_sep=True)
    assert len(name) == 24
    assert name.isprintable()
    assert '_' not in name


def test_name_generator_chars():
    name = name_generator(size=15, chars=string.hexdigits)
    assert len(name) == 31
    str1, str2 = name.split(sep='_', maxsplit=-1)
    assert all(c in string.hexdigits for c in str1)
    assert all(c in string.hexdigits for c in str2)


def test_get_platform_path():
    zt_platpath = get_platform_path()
    assert isinstance(zt_platpath, Path)
    assert 'zerotier' or 'ZeroTier' in str(zt_platpath)


def test_get_token(tmp_path):
    auth_tok = name_generator(size=24, no_sep=True)
    d = tmp_path / "zerotier-one"
    d.mkdir()
    p = d / "authtoken.secret"
    p.write_text(auth_tok)
    zt_auth = get_token(d)
    assert len(zt_auth) == 24
    assert zt_auth.isprintable()


def test_get_token_not_found(tmp_path):
    zt_auth = get_token()
    assert zt_auth is None


def test_platform_check():
    posix_name = os.name
    iam = platform_check()
    if posix_name == 'posix':
        assert iam
    else:
        assert not iam
