# albumcutter

albumcutter is a tool to download albums on youtube and break the audio into
individual tracks based on a tracklist containing timestamps.

## How to use

Specify the URL of the audio you wish to download, and copy the tracklist into
your clipboard and invoke the command like so:

    ac -d Top_20_Kevin_MacLeod https://www.youtube.com/watch?v=z6CLOO0qIx4

`ac` will ask you to confirm the contents of the clipboard in case you made a
mistake.

## dependencies

 * Python 2.7

 * [youtube-dl](https://github.com/rg3/youtube-dl)
   (latest version is reccomended, if not required)
 * [pydub](https://github.com/jiaaro/pydub)

## installation

To install albumcutter, run `setup.sh` with elevated permissions.

Alternatively, if you do not want to install and/or you are on windows, move
`bin/ac` to `albumcutter/ac.py` and run with `python albumcutter/ac.py`

