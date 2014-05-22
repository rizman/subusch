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
from _socket import timeout
import logging

import os
from subusch.providers.baseprovider import BaseProvider


class VideoFile():
    __path = ''
    __filename = ''
    __extension = ''
    __preferred_langs = []
    __missing_langs = []
    __found_langs = []
    __providers = None
    __force = False

    def __init__(self, path, filename, langs, prov, force):
        self.__path = path
        self.__filename = filename
        self.__preferred_langs = langs
        self.__providers = prov
        self.__force = force
        self.__found_langs = []
        self.__missing_langs = []
        if not self.__force:
            self.__get_subtitles_on_filesystem()

    def __get_subtitles_on_filesystem(self):
        """
        Scan filesystem for already existing subtitle files
        :return: List if existing subtitle languages
        :rtype: list
        """
        for lang in self.__preferred_langs:
            subfilename = self.__get_subfilename(lang)
            if os.path.isfile(subfilename):
                self.__found_langs.append(lang)

    def __get_subfilename(self, lang):
        """
        Build a string containing the name of the subtitle file. The language is encoded.
        e.g. u'c:\\Users\\SomeRandomUser\\Documents\\Videos\\Breaking Bad\\Season 1\\Breaking.Bad.S01E01.Pilot.en.srt'
        :param lang: The language for which the subtitle filename should be build
        :type lang: str
        :return: The subtitle filaneme
        :rtype: str
        """
        subfilename, _ = os.path.split(self.__path)
        subfilename = ".".join([os.path.join(subfilename, os.path.splitext(self.__filename)[0]), lang, 'srt'])
        return subfilename

    def get_subtitles(self):
        self.__missing_langs = [x for x in self.__preferred_langs if not x in self.__found_langs]
        logger = logging.getLogger(__name__)
        if not self.__missing_langs:
            logger.info('\t\tAll subtitle files are already present in the destination directory. Nothing to be done')
            return self.__missing_langs
        else:
            logger.info('\t\tNeed to download ' + ', '.join(self.__missing_langs))

        for prov in self.__providers:
            provider = None
            if not self.__missing_langs:
                logger.info('\t\tAll missing subtitles have been downloaded. Nothing more to be done')
                return self.__missing_langs
            provider_class = BaseProvider.get_provider_class(prov)
            if provider_class:
                provider = provider_class(self.__path)

            if provider:
                try:
                    langs_downloaded = provider.get_subtitles(self.__missing_langs)
                    if langs_downloaded:
                        for lang in langs_downloaded:
                            if lang in self.__missing_langs:
                                self.__missing_langs.remove(lang)
                    else:
                        logger.info('\t\tNo missing subtitles found on %s', prov)
                except timeout as ex:
                    logger.warning('Timeout')

        if self.__missing_langs:
            logger.info('\t\tFailed to get subtitles for ' + ', '.join(self.__missing_langs))
        else:
            logger.info('\t\tGot all subtitles')

        return self.__missing_langs