# import cherrypy
# from subusch.controllers.home import Home
# from subusch.providers import thesubdb

# if __name__ == '__main__':
    # root = Home()
    # cherrypy.quickstart(root)
    # provider = thesubdb.TheSubDb()
    # hash = provider.get_hash(
    #     r'C:\Users\NYR756\Videos\Doctor Who\Season 07\Doctor Who (2005) - s07e13 - The Name of the Doctor.mp4')
    # print(hash)
    # print(provider.search(hash, 'true'))
    #print(provider.get_languages().read())
    #print(provider.search('ffd8d4aa68033dc03d1c8ef373b9028c', True).read())

import argparse
from subusch.config import DEFAULT_FILES

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='ssubusch',
                                     description='Scan a folder for files and try to download subtitles for them from '
                                                 'different sources like www.thesubdb.com ')
    parser.add_argument('path', help='The folder to scan')
    parser.add_argument('-r', '--recursive', help='Scan the chosen folder recursively', action='store_true')
    parser.add_argument('-t', '--types', help='File types to scan', type=list, default=DEFAULT_FILES)
    args = parser.parse_args()

    print (args.types)