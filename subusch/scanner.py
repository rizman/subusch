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
import logging

import os
import re
from subusch.videofile import VideoFile


class Scanner:

    """
    Scans a root folder (path) for any files with a
    given extension
    """

    total_files_scanned = 0
    total_directories_scanned = 0


    def __init__(self, path, ext, langs, providers, recursive, force_download):
        regex = r'[\w]+'
        self.__path = path
        self.__extensions = re.findall(regex, ext)
        self.__langs = re.findall(regex, langs)
        self.__providers = re.findall(regex, providers)
        self.__recursive = recursive
        self.__force_download = force_download

    def start_scan(self):
        """
        Recursively scan folders starting from path and look for
        files with an extension matching any of the extensions in
        config.DEFAULT_FILE_EXT

        :return: Does not return any value
        :rtype: None
        """
        logger = logging.getLogger(__name__)
        if os.path.isfile(self.__path):
            head, tail = os.path.split(self.__path)
            self.total_directories_scanned += 1
            self._get_subtitles(tail, head)
            return True

        if not os.path.isdir(self.__path):
            logger.info("Directory does not exist. Exiting")
            return False

        for dirpath, dirnames, filenames in os.walk(self.__path):
            if not self.__recursive:
                if dirpath != self.__path:
                    continue
            logger.info('Scanning directory %s', dirpath)
            self.total_directories_scanned += 1
            for file in filenames:
                self._get_subtitles(file, dirpath)

    def _get_subtitles(self, file, dirpath):
        logger = logging.getLogger(__name__)
        _, ext = os.path.splitext(file)
        ext = ext.lstrip('.').rstrip(' ')
        if ext in self.__extensions:
            logger.info('\t %s:', file)
            videoFile = VideoFile(os.path.join(dirpath, file),
                                  file,
                                  self.__langs,
                                  self.__providers,
                                  self.__force_download)
            videoFile.get_subtitles()
            self.total_files_scanned += 1