#!/usr/bin/env python3
#
# test_maasclient.py - Unittests for MaaS REST api
#
# Copyright 2014 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import unittest
import sys
sys.path.insert(0, '../maasclient')

from maasclient import MaasClient

from unittest.mock import MagicMock, patch, PropertyMock, sentinel


def setup_mock_response(mock_requests_mod, op='get', ok=True, response=None):
    mock_response = MagicMock()
    p_ok = PropertyMock(return_value=ok)
    type(mock_response).ok = p_ok
    p_text = PropertyMock(return_value=response)
    type(mock_response).text = p_text
    if op == 'get':
        mock_requests_mod.get.return_value = mock_response
    elif op == 'post':
        mock_requests_mod.post.return_value = mock_response
    else:
        raise Exception("not mocking {} yet".format(op))

ONE_MACHINE_JSON_NOTAGS = """
[   {
        "status": 0,
        "macaddress_set": [
            {
                "resource_uri": "/MAAS/api/1.0/nodes/fake-uri",
                "mac_address": "ec:a8:6b:fb:34:d6"
            }
        ],
        "hostname": "m6mm9.maas",
        "zone": {
            "resource_uri": "/MAAS/api/1.0/zones/default/",
            "name": "default",
            "description": ""
        },
        "routers": [],
        "netboot": false,
        "cpu_count": 4,
        "storage": 115880,
        "owner": "root",
        "system_id": "node-01",
        "architecture": "amd64/generic",
        "memory": 8192,
        "power_type": "amt",
        "tag_names": [
        ],
        "ip_addresses": [
            "10.0.100.4"
        ],
        "resource_uri": "/MAAS/api/1.0/nodes/node-01/"
    }
]
"""


TWO_TAGS_JSON = """
[
    {
        "comment": "",
        "definition": "true()",
        "resource_uri": "/MAAS/api/1.0/tags/tag1/",
        "name": "tag1",
        "kernel_opts": ""
    },
    {
        "comment": "",
        "definition": "",
        "resource_uri": "/MAAS/api/1.0/tags/tag2/",
        "name": "tag2",
        "kernel_opts": ""
    }
]
"""


@patch("maasclient.OAuth1")
@patch("maasclient.requests")
class MaasClientTagTest(unittest.TestCase):
    def setUp(self):
        self.mock_auth = MagicMock()
        self.api_url = 'apiurl'
        url_p = PropertyMock(return_value=self.api_url)
        type(self.mock_auth).api_url = url_p
        self.c = MaasClient(self.mock_auth)

    def test_get_no_tags(self, mock_requests, mock_oauth):
        setup_mock_response(mock_requests, ok=True, response="[]")
        self.assertEqual(self.c.tags, [])

    def test_get_tags(self, mock_requests, mock_oauth):
        setup_mock_response(mock_requests, ok=True,
                            response=TWO_TAGS_JSON)
        self.assertEqual(self.c.tags[0]['name'], 'tag1')
        self.assertEqual(self.c.tags[1]['name'], 'tag2')

    def test_create_tag_existing(self, mock_requests, mock_oauth):
        setup_mock_response(mock_requests, op='get', ok=True,
                            response=TWO_TAGS_JSON)
        setup_mock_response(mock_requests, op='post', ok=True)
        rv = self.c.tag_new('tag1')
        self.assertEqual(rv, False)
        self.assertEqual(mock_requests.post.call_count, 0)

    def test_create_tag_nonexisting(self, mock_requests, mock_oauth):
        setup_mock_response(mock_requests, op='get', ok=True,
                            response=TWO_TAGS_JSON)
        setup_mock_response(mock_requests, op='post', ok=True)

        mock_oauth.return_value = sentinel.OAUTH

        newtag = 'newtag'
        rv = self.c.tag_new(newtag)
        self.assertEqual(True, rv)
        mock_requests.post.assert_called_once_with(url=self.api_url + '/tags/',
                                                   auth=sentinel.OAUTH,
                                                   data=dict(op='new',
                                                             name=newtag))

    def test_tag_name(self, mock_requests, mock_oauth):

        system_id = "node-01"

        with patch('maasclient.MaasClient.tag_new') as mock_tag_new:
            with patch('maasclient.MaasClient.tag_machine') as mock_tag_mach:
                c = MaasClient(self.mock_auth)
                c.tag_name(json.loads(ONE_MACHINE_JSON_NOTAGS))

                mock_tag_new.assert_called_once_with(system_id)
                mock_tag_mach.assert_called_once_with(system_id,
                                                      system_id)

    def test_tag_fpi(self, mock_requests, mock_oauth):

        system_id = "node-01"
        fpi_tag = 'use-fastpath-installer'

        with patch('maasclient.MaasClient.tag_new') as mock_tag_new:
            with patch('maasclient.MaasClient.tag_machine') as mock_tag_mach:
                c = MaasClient(self.mock_auth)
                c.tag_fpi(json.loads(ONE_MACHINE_JSON_NOTAGS))

                mock_tag_new.assert_called_once_with(fpi_tag)
                mock_tag_mach.assert_called_once_with(fpi_tag,
                                                      system_id)


if __name__ == '__main__':
    unittest.main()
