# subusch

subusch is a simple python program used from the command line which allows you to download subtitle files for your favorite TV Shows and Movies from different subtitle providers.

This is a very early version.

## Dependencies
subusch requires at least python 3.4. You can download python from https://www.python.org/ for all major platforms (Windows, OSX, *nix and others)

For Linux users, check your distros package manager for a precompiled package of python 3.4.

No other dependencies are required.

## Supported providers
Currently supported:
- [TheSubDb](http://www.thesubdb.com).
- [Opensubtitles](http://www.opensubtitles.org) (only partially implemented)
Other providers are planned.

## Usage
Just run subusch.py 'path' from the command line. If 'path' is a directory, subusch will search for subtitles for every video file inside 'path'. 
If 'path' is a file, subusch will download subtitles just for that file and ignore the -r switch (recursive scanning of directories)

To get help, specify the -h or --help switch
```
python subusch.py -h
```
This yields the following output

```
usage: subusch [-h] [-r] [-e EXT] [-l LANG] [-p PROV] [-f] path

Scan a folder for files and try to download subtitles for them from different
sources like www.thesubdb.com

positional arguments:
  path                  The folder to scan

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       Scan the chosen folder recursively
  -e EXT, --ext EXT     File extensions to scan. Default is avi, mkv, mp4, mwv
  -l LANG, --lang LANG  The language for which subtitles should be downloaded.
                        Default is en
  -p PROV, --prov PROV  The subtitle providers to use. Default is tsdb, ost
  -f, --force           Forces the download of subtitles, even if they are
                        already present on the filesystem
```

## Configuration
Some default values like preferred language, preferred providers etc. can be set in the file config.py. Read the file carefully for instructions.