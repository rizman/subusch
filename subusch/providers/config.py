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

# Timeout to wait for a response from the subtitle sites.
BASE_TIMEOUT = 2

# CLIENT_VERSION, CLIENT_NAME and CLIENT_URL are used to form the user-agent
# string required by TheSubDB - see here for details: http://thesubdb.com/api/
TSDB_API_URL = 'http://sandbox.thesubdb.com/'
# TSDB_API_URL = 'http://api.thesubdb.com/'
TSDB_CLIENT_VERSION = '0.1'
TSDB_CLIENT_NAME = 'subusch'
TSDB_CLIENT_URL = 'http://github.com/rizman/subusch'

OST_API_URL = 'http://api.opensubtitles.org/xml-rpc'

# Map the given provider to its implementing class. This should only
# be changed when a new provider is implemented.
PROVIDER_TO_CLASS_MAP = {
    'tsdb': 'subusch.providers.thesubdb.TheSubDb',
    'ost': 'subusch.providers.opensubtitles.OpenSubTitles'
}

LANGUAGES = {
    # Full Language name[0]     ISO 639-1[1]    ISO 639-1 Code[2]
    'en':   ('English',         'en',           'eng'),
    'de':   ('German',          'de',           'ger'),
    'fr':   ('French',          'fr',           'fre'),
    'nl':   ('Dutch',           'nl',           'dut'),
    'pt':   ('Portuguese',      'pt',           'por'),
    'es':   ('Spanish',         'es',           'spa')
}