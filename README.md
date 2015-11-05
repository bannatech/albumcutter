# albumcutter

albumcutter is a tool to download albums on youtube and break the audio into
individual tracks based on a tracklist containing timestamps.

## How to use

Specify the URL of the audio you wish to download, and copy the tracklist into
your clipboard and invoke the command like so:

    ac -d Top_20_Kevin_MacLeod https://www.youtube.com/watch?v=z6CLOO0qIx4

`ac` will ask you to confirm the contents of the clipboard in case you made a
mistake.

In this example, you can rip the tracklist off of the video description. (pasted below for reference):

    1. Cipher 0:00
    2. Who Likes to Party 3:51
    3. Scheming Weasel (faster version) 8:09
    4. Sneaky Snitch 9:38
    5. Wallpaper 11:55
    6. Spazzmatica Polka 15:35
    7. Pixel Peeker Polka - faster 17:10
    8. Gaslamp Funworks 20:33
    9. Merry Go 23:01
    10. Fluffing a Duck 25:02
    11.Hall of the Mountain King 26:09
    12. Cut and Run 28:42
    13. Mechanolith 32:17
    14. Killing Time 33:12
    15. At Rest 36:36
    16. Pop Goes the Weasel 40:03
    17. The House of Leaves 41:12
    18. There It Is 44:38
    19. Sovereign 45:28
    20. Heartbreaking 51:21 - 52:56

## dependencies

 * Python 2.7

 * [youtube-dl](https://github.com/rg3/youtube-dl)
   (latest version is reccomended, if not required)
 * [pydub](https://github.com/jiaaro/pydub)

## installation

To install albumcutter, run `setup.sh` with elevated permissions.

Alternatively, if you do not want to install and/or you are on windows, move
`bin/ac` to `albumcutter/ac.py` and run with `python albumcutter/ac.py`

