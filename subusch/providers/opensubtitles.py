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
import base64
import gzip
from idlelib.MultiCall import _parse_sequence
import logging
import os
import struct
import io
import xmlrpc.client

from subusch.providers.baseprovider import BaseProvider
from subusch.providers.config import OST_API_URL, LANGUAGES
from subusch.utilities.proxiedtransport import ProxiedTransport


class OpenSubTitles(BaseProvider):
    """
    Implements the Opensubtitles XML-RPC API
    See here for documentation http://trac.opensubtitles.org
    """

    _base_url = OST_API_URL
    _xml = None
    _user_agent = 'OS Test User Agent'
    _token = ''
    _connected = False
    _subsToDownload = {}

    def __init__(self, path):
        super().__init__(path)
        if self._proxy:
            p = ProxiedTransport()
            p.set_proxy(self._proxy['http'])
            self._xml = xmlrpc.client.Server(self._base_url, transport=p)
        else:
            self._xml = xmlrpc.client.ServerProxy(self._base_url)
        self._hash = self._get_hash()
        self._subsToDownload = {}

    def get_subtitles(self, langs):
        self.log_in()
        langs_downloaded = []
        if self.search_subtitles(langs):
            # langs_downloaded = self.download_subtitles()
            pass
        # self.no_operation()
        self.log_out()
        return langs_downloaded

    def server_info(self):
        print(self._xml.ServerInfo())

    def log_in(self):
        if self._connected:
            return True
        resp = self._xml.LogIn('', '', 'en', self._user_agent)
        if resp['status'] == '200 OK':
            self._token = resp['token']
            self._connected = True
            return True
        else:
            return False

    def log_out(self):
        if not self._connected:
            return True
        resp = self._xml.LogOut(self._token)
        if resp['status'] == '200 OK':
            self._token = ''
            self._connected = False
            return True
        else:
            return False

    def parse_search_result(self, result):
        data = result['data']
        if data:
            for subfile in data:
                # y = [self._subsToDownload[x]['lang2'] for x in self._subsToDownload]
                # print(y)
                self._subsToDownload[subfile['IDSubtitleFile']] = {
                    'lang2': subfile['ISO639'],
                    'lang3': subfile['SubLanguageID'],
                    'format': subfile['SubFormat'],
                    'matchedby': subfile['MatchedBy'],
                    'subdownloadlink': subfile['SubDownloadLink'],
                    'SubtitlesLink': subfile['SubtitlesLink']
                }
            return True
        else:
            return False

    def search_subtitles(self, langs):
        if not self._connected:
            self.log_in()
        langlist = []
        for l in langs:
            if LANGUAGES[l]:
                langlist.append(LANGUAGES[l][2])
        found = False
        if self.search_subtitles_by_hash(langlist):
            found = True
        elif self.search_subtitles_by_query(langlist):
            found = True

        return found

    def search_subtitles_by_hash(self, langlist):
        searchlist = [{'sublanguageid': ",".join(langlist), 'moviehash': str(self._hash), 'moviebytesize': str(self._filesize)}]
        resp = self._xml.SearchSubtitles(self._token, searchlist)
        if resp['status'] == '200 OK':
            return self.parse_search_result(resp)
        return False

    def search_subtitles_by_query(self, langlist):
        searchlist = [
            {'sublanguageid': ",".join(langlist), 'query': str('doctor who the rebel flesh')}]
        resp = self._xml.SearchSubtitles(self._token, searchlist)
        if resp['status'] == '200 OK':
            return self.parse_search_result(resp)
        return False

    def download_subtitles(self):
        logger = logging.getLogger(__name__)
        if not self._subsToDownload:
            return False
        if not self._connected:
            self.log_in()
        langs_downloaded = []
        subIds = [x for x in self._subsToDownload]
        resp = self._xml.DownloadSubtitles(self._token, subIds)
        if resp['status'] == '200 OK':
            data = resp['data']
            if data:
                for subfile in data:
                    subfilecontent = subfile['data']
                    lang = self._subsToDownload[subfile['idsubtitlefile']]['lang2']
                    subfilename = self.get_subfilename(lang)
                    b = gzip.decompress(base64.b64decode(subfilecontent))
                    file = io.open(self.get_subfilename(lang), 'wb')
                    file.write(b)
                    file.close()
                    logger.info('\t\tGot ' + lang + ' from Opensubtitles. Saved to ' + subfilename)
                    langs_downloaded.append(lang)
        elif resp['status'] == '407 Download limit reached':
            logger.warning('Daily download limit (200 files) reached for Opensubtitles.org')

        return langs_downloaded

    def no_operation(self):
        if not self._connected:
            self.log_in()
        resp = self._xml.NoOperation(self._token)
        print(resp)

    def _get_hash(self):
        try:
            longlongformat = 'q'
            bytesize = struct.calcsize(longlongformat)

            f = open(self._path, 'rb')
            self._filesize = os.path.getsize(self._path)
            hash = self._filesize

            if self._filesize < 65536 * 2:
                return "SizeError"

            for x in range(int(65536/bytesize)):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash &= 0xFFFFFFFFFFFFFFFF  #to remain as 64bit number

            f.seek(max(0, self._filesize - 65536), 0)
            for x in range(int(65536/bytesize)):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash &= 0xFFFFFFFFFFFFFFFF

            f.close()
            returnedhash = "%016x" % hash
            return returnedhash

        except IOError:
            return "IOError"

