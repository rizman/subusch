# subusch - The python subtitle downloader
# Copyright (C) 2014 - Gilles RADRIZZI
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import xmlrpc.client
import http.client


class ProxiedTransport(xmlrpc.client.Transport):
    def set_proxy(self, proxy):
        self.proxy = proxy

    def make_connection(self, host):
        self.realhost = host
        h = http.client.HTTPConnection(self.proxy)
        return h

    def send_request(self, host, handler, request_body, debug=True):
        connection = self.make_connection(host)
        headers = self._extra_headers[:]
        connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))
        # connection.endheaders(request_body)
        headers.append(("Content-Type", "text/xml"))
        self.send_headers(connection, headers)
        self.send_content(connection, request_body)
        return connection

    def send_host(self, connection, host):
        connection.putheader('Host', self.realhost)
