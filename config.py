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
#
# ====================================================
# Configuration file for subusch.
# subusch is a python program designed to download
# subtitle files for your video files from different
# sources like www.thesubdb.com
#
# You may adjust the values inside this file as needed
# by your system.
# ====================================================

# Use this to set a proxy to connect to the subtitle providers.
# Useful if you are behind a firewall (in case you like watching
# your episodes at work and you want your subtitles :-) )
HTTP_PROXY = ''

# The file extensions for which the filesystem should be scanned.
# The format is a comma-separated list of extensions
# e.g. avi, mkv, mp4
DEFAULT_FILE_EXT = 'avi, mkv, mp4, mwv'

# The languages for which subtitles should be searched for.
# This can be overridden by the --lang (-l) flag when calling
# subusch.
# The format is a comma-separated list of country codes
# e.g. en, de, fr
PREFERRED_LANG = 'en,fr'

# Specify which subtitle providers subusch should use and in
# which order of preference.
# If your preferred languages are set to 'en, de' and Providers
# are set to 'TSDB, OST', subusch will first try to get an english
# subtitle from TSDB. If none is found, it will try OST until it finds
# a subtitle or none are found. Then it will restart with the german
# subtitle.
#
# TSDB = TheSubDB --> www.thesubdb.com
# OST = OpenSubTitles --> www.opensubtitles.org (provider not yet implemented)
PROVIDERS = 'tsdb,ost'

# Specify the location of the logfile.
LOG_FILE = 'subusch.log'

# Appends the language suffix to the subtitle file
# This defaults to true if more than one subtitle language for a file
# is found.
# NOT USED
# APPEND_LANG_SUFFIX = True
