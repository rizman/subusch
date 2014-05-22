#!/usr/bin/env python
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

"""
Entry point for subusch - the subtitle downloader
"""

import argparse
import logging

from config import DEFAULT_FILE_EXT, PREFERRED_LANG, PROVIDERS, LOG_FILE
from subusch.scanner import Scanner

def init_logging(verbose):
    logformat = '%(asctime)s %(name)-35s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=logformat,
                        filename=LOG_FILE,
                        filemode='w')
    logger = logging.getLogger('')
    if verbose:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(logformat))
        logger.addHandler(console)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='subusch',
        description=u'subusch - Copyright (C) 2014 - Gilles RADRIZZI\n'
                    u'This program comes with ABSOLUTELY NO WARRANTY\n'
                    u'This is free software, and you are welcome to redistribute it under certain conditions;\n'
                    u'It is licensed under the GNU General Public License v3. For details see the LICENSE file.\n'
                    u'Description: Scan a folder for files and try to download subtitles for them from '
                    u'different providers ',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'path',
        help='The folder to scan'
    )
    parser.add_argument(
        '-r',
        '--recursive',
        help='Scan the chosen folder recursively',
        action='store_true'
    )
    parser.add_argument(
        '-e',
        '--ext',
        help='File extensions to scan. Default is ' + DEFAULT_FILE_EXT,
        type=str,
        default=DEFAULT_FILE_EXT
    )
    parser.add_argument(
        '-l',
        '--lang',
        help='The language for which subtitles should be '
             'downloaded. Default is ' + PREFERRED_LANG,
        type=str,
        default=PREFERRED_LANG
    )
    parser.add_argument(
        '-p',
        '--prov',
        help='The subtitle providers to use. Default is ' + PROVIDERS,
        type=str,
        default=PROVIDERS
    )

    parser.add_argument(
        '-f',
        '--force',
        help='Forces the download of subtitles, even if they are already present '
             'on the filesystem',
        action='store_true'
    )

    parser.add_argument(
        '--logfile',
        help='Path to the log file. Default is ' + LOG_FILE,
        type=str,
        default=LOG_FILE
    )

    parser.add_argument(
        '-v',
        '--verbose',
        help='Verbose output to console',
        action='store_true'
    )

    args = parser.parse_args()

    init_logging(args.verbose)
    logger = logging.getLogger('subusch')
    logger.info('=' * 80)
    logger.info("Subusch started...")

    logger.info("Starting in directory %s", args.path)
    if args.recursive:
        logger.info("Recursive: True")
    if args.prov:
        logger.info("Providers to check: %s", args.prov)
    if args.lang:
        logger.info("Preferred languages: %s", args.lang)
    if args.ext:
        logger.info("Extension to include: %s", args.ext)
    if args.force:
        logger.info("Forcing download of existing subtitle files")
    logger.info('Logging to: %s', args.logfile)
    scanner = Scanner(args.path, args.ext, args.lang, args.prov, args.recursive, args.force)
    scanner.start_scan()
    logger.info("Scanned %s files in %s directories", scanner.total_files_scanned, scanner.total_directories_scanned)
    logger.info("Subusch finished...")
    logger.info("=" * 80 + "\n\n")