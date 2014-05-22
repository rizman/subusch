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

import hashlib
from http.client import HTTPResponse
import logging
import os
import io

from urllib.error import URLError
from urllib.request import ProxyHandler
from subusch.providers.baseprovider import BaseProvider
from subusch.providers.config import *


class TheSubDb(BaseProvider):

    """
    Implements the API provided by TheSubDB
    """

    _base_url = TSDB_API_URL

    def __init__(self, file_path):
        """
        TheSubDb constructor. Calls the base class baseprovider constructor
        """
        self._md5_hash = self._get_hash(file_path)
        super().__init__(file_path)

    @property
    def useragent(self):
        """
        Constructs the user-agent string used by TheSubDB.

        For details see here: http://thesubdb.com/api/
        :return: user-agent string.
        :rtype: str
        """
        user_agent = u'SubDB/1.0 ({0:s}/{1:s}; {2:s})'.format(TSDB_CLIENT_NAME, TSDB_CLIENT_VERSION, TSDB_CLIENT_URL)
        return user_agent

    def get_languages(self):
        """
        Calls the TheSubDB action for returning all supported languages.

        :return: Returns a list of language codes
        :rtype: list
        """
        action = '?action=languages'
        url = self._base_url + action
        try:
            res = self._open(url)
            # converts the byte encoded string returned by HTTPResponse.read() to utf8
            lang = str(res.read(), encoding='utf8')
            return lang.split(',')
        except URLError as ex:
            if hasattr(ex, 'code'):
                if ex.code == 400:
                    return ['Malformed']
            elif hasattr(ex, 'reason'):
                if ex.reason.args[0] == 'timed out':
                    return ['Timed out']
                else:
                    return [ex.reason]
            else:
                return ['Unknown error']

    def _download_subtitles(self, hash, languages):
        """
        Calls the TheSubDB action for downloading the subtitles for a given file

        :param file_hash: The MD5 hash of the file to get a subtitle file for
        :type file_hash: str
        :param languages: comma separated list of language codes
        :type languages: str
        :return:
        :rtype:
        """
        action = '?action=download'
        url = self._base_url + action + '&hash=' + hash + '&language=' + languages
        try:
            res = self._open(url)
            sub = str(res.read(), encoding='ISO-8859-9')
            return sub
        except URLError as ex:
            if hasattr(ex, 'code'):
                if ex.code == 400:
                    logging.warning('Malformed URL')
                    return ['Malformed']
                elif ex.code == 404:
                    return ['NotFound']
            elif hasattr(ex, 'reason'):
                if ex.reason.args[0] == 'timed out':
                    return ['Timed out']
                else:
                    return[ex.reason]
            else:
                return ['Unknown error']

    def _search(self, hash, versions='False'):
        """
        Calls the TheSubDB action for returning the a list of available subtitles
        for a given hash.

        :param file_hash: The hash of the file to get subtitles for
        :type file_hash: str
        :param versions: If True, returns how many versions per language of a subtitle TheSubDB has in its database
        :type versions: str
        :return: List of available subtitle languages for the given file
        :rtype: list
        """
        action = '?action=search'
        url = self._base_url + action + '&hash=' + hash
        if versions.lower() == 'true':
            url += '&versions'
        try:
            res = self._open(url)
            # converts the byte encoded string returned by HTTPResonse.read() to utf8
            lang = str(res.read(), encoding='ISO-8859-9')
            return lang.split(',')
        except URLError as ex:
            if hasattr(ex, 'code'):
                if ex.code == 400:
                    return ['Malformed']
                elif ex.code == 404:
                    return ['NotFound']
            elif hasattr(ex, 'reason'):
                if ex.reason.args[0] == 'timed out':
                    return ['Timed out']
                else:
                    return[ex.reason]
            else:
                return ['Unknown error']

    def _get_hash(self, path):
        """
        Compute the md5 hash of a file.

        Computes the md5 hash of a given file according to instructions given
        by theSubDB here: http://thesubdb.com/api/.

        :param path: the complete file system path to the file
        :type path: str
        :return: returns the md5 hash
        :rtype: str
        """
        readsize = 64 * 1024
        with open(path, 'rb') as f:
            size = os.path.getsize(path)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

    def _open(self, url=_base_url) -> HTTPResponse:
        """
        Opens a specified URL
        :param url: The URL to open
        :type url: str
        :return: Returns the response from the opened URL
        :rtype: http.client.HTTPResponse
        """
        self._opener.addheaders = [('User-agent', self.useragent)]
        if any(self._proxy):
            self._opener.add_handler(ProxyHandler(proxies=self._proxy))
        response = self._opener.open(url, timeout=self._timeout)
        return response

    def get_subtitles(self, langs):
        logger = logging.getLogger(__name__)
        available_langs = self._search(self._md5_hash)  #get languages available on TSDB
        langs_to_get = [x for x in available_langs if x in langs]
        langs_downloaded = []
        for lang in langs_to_get:
            try:
                subfilename = self.get_subfilename(lang)
                sub = self._download_subtitles(self._md5_hash, LANGUAGES[lang][1])
                file = io.open(subfilename, 'w', encoding='utf-8')
                file.write(sub)
                file.close()
                logger.info('\t\tGot ' + lang + ' from TheSubDB. Saved to ' + subfilename)
                langs_downloaded.append(lang)
            except URLError as ex:
                logger.warning('\t\tError while getting ' + lang + ' for ' + self._path + ' from TheSubDB')
                # logger.debug(ex.reason)
        return langs_downloaded