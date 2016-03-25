#!/usr/bin/env python3
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

import pprint
import sys

from maasclient.auth import MaasAuth
from maasclient import MaasClient


def main():
    url = None
    if len(sys.argv) == 3:
        url = sys.argv[1]
        key = sys.argv[2]
        auth = MaasAuth(api_url=url, api_key=key)
    else:
        auth = MaasAuth(api_url=url)
        auth.get_api_key('root')
    maas_client = MaasClient(auth)
    pprint.pprint(maas_client.nodes)
    pprint.pprint(maas_client.get_server_config('maas_name'))
    pprint.pprint(maas_client.server_hostname)

if __name__ == "__main__":
    main()
