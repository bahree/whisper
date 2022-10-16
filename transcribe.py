# If you don't have pytube installed, then install it first using the following command: # pip install pytube

from pytube import Playlist
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

# this is the twiml AI podcast playlist - all episodes
TWIML_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLILZm3MRkvH83C46bZ4rPmB-jKWBltWkP"
MP3_PATH = "twiml-episodes"
TWIML_PLAYLIST_FILENAME = "twiml-playlist.txt"

# from a youtube playlist, get all the video urls, titles, and episode numbers and save them to a text file
def savePlaylistToFile(playlist_url, playlist_filename):
    p = Playlist(playlist_url)
    with open(playlist_filename, 'w', encoding="utf8") as f:
        for index, url in enumerate(p.video_urls, start=1):
            yt = YouTube(url)
            print(index, '|' + yt.title + '|' + url )
            f.write(str(index) + '|' + yt.title + '|' + url + '\n')
        print("Playlist saved to file" + playlist_filename + " with " + str(index) + " episodes.")


# from a youtube playlist, get the video url, title, and save it as a mp3 file
def downloadVideoFromPlaylist(playlist_url, path):
    playlist = Playlist(playlist_url)
    for index, video in enumerate(playlist.videos, start=1):
        # if index < 286:
        #     continue
        print("Downloading #" + str(index) + " ... " + video.title)
        try:
            tempFileName = validFilename(str(index) + '_' + video.title + ".mp3")
            video.streams.filter(only_audio=True).first().download(output_path=MP3_PATH, filename=tempFileName)
        except IOError:
            print("Error: can\'t save the following file. Most likely it has an invalid character in the name.")
            print("File: " + tempFileName)
        except VideoUnavailable:
            print("Video: " + tempFileName + " is unavaialable, skipping.")
    print("Download complete. Number of episodes downloaded: " + str(index))


# download mp3 from youtube video url
def downloadVideoFromURL(video_url, path):
    yt = YouTube(video_url)
    tempFileName = validFilename(yt.title + ".mp3")
    yt.streams.filter(only_audio=True).first().download(output_path=MP3_PATH, filename=tempFileName)
    print("File downloaded: " + tempFileName)


# check if a filename is valid
def is_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return all(c.isalnum() or c in "._-()" for c in s)


# convert a string to a valid filename
def validFilename(s):
    s = str(s).strip().replace(' ', '_')
    s = str(s).strip().replace('/', '-')
    s = str(s).strip().replace('&', 'and')
    s = str(s).strip().replace('\'', '')
    s = str(s).strip().replace('"', '')
    s = str(s).strip().replace(':', '-')
    s = str(s).strip().replace('*', '')
    return s


# Choose what we want to do; this can be improved using a menu option but for now too lazy to do that

#savePlaylistToFile(TWIML_PLAYLIST_URL, TWIML_PLAYLIST_FILENAME)
#downloadVideoFromPlaylist(TWIML_PLAYLIST_URL, MP3_PATH)
#downloadVideoFromURL("https://www.youtube.com/watch?v=YgQxlKPeC-g", MP3_PATH)