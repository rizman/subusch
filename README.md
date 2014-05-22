# subusch

subusch is a simple python program used from the command line which allows you to download subtitle files for your favorite TV Shows and Movies from different subtitle providers.

This is a very very early version.

## Supported providers
Currently, only [TheSubDb](http://www.thesubdb.com) is supported.

Other providers are in planification

## Usage
Just run subusch.py from the command line. To get help, specify the -h or --help switch
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