import os
import sys
import vlc

def openFile(filepath):
    movie = os.path.expanduser(filepath)
    if 'http://' not in filepath:
        if not os.access(movie, os.R_OK):
            print ( 'Error: %s file is not readable' % movie )
            sys.exit(1)
    instance = vlc.Instance()
    #"--sout=#duplicate{dst=file{dst=example.mpg},dst=display}"
    try:
        media = instance.media_new(movie)
    except NameError:
        print ('NameError: % (%s vs Libvlc %s)' % (sys.exc_info()[1],
                       vlc.__version__, vlc.libvlc_get_version()))
        sys.exit(1)
    player = instance.media_player_new()
    player.set_media(media)
    player.play()

    #dont exit!
    while(1):
        continue
if __name__ == '__main__':
    filepath = 'http://free.anbient.net/Log-Horizon/Log_Horizon_01_FF-Anbient.mkv'
    openFile(filepath)

