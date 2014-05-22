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

import urllib.request
import os

from subusch.providers.config import *
import config


class BaseProvider:

    def __init__(self, path):
        self._opener = urllib.request.build_opener()
        self._timeout = BASE_TIMEOUT
        self._path = path
        if config.HTTP_PROXY:
            self._proxy = {'http': config.HTTP_PROXY}
        else:
            self._proxy = {}

    def get_subtitles(self, langs):
        pass

    def get_subfilename(self, lang):
        """
        Build a string containing the name of the subtitle file. The language is encoded.
        e.g. u'c:\\Users\\SomeRandomUser\\Documents\\Videos\\Breaking Bad\\Season 1\\Breaking.Bad.S01E01.Pilot.en.srt'
        :param lang: The language for which the subtitle filename should be build
        :type lang: str
        :return: The subtitle filaneme
        :rtype: str
        """
        subfilename, _ = os.path.split(self._path)
        subfilename = ".".join([os.path.join(subfilename, os.path.splitext(self._path)[0]), lang, 'srt'])
        return subfilename

    def _open(self):
        pass

    @staticmethod
    def get_provider_class(provider_name):
        """
        Given the subtitle provider to use, return the corresponding class.

        :param provider_name: the name of the provider as specified in the providers.config.py
        PROVIDER_TO_CLASS_MAP dictionary.
        :type provider_name: str
        :return: A class object
        :rtype: object
        """

        provider_class = PROVIDER_TO_CLASS_MAP[provider_name]
        parts = provider_class.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m


