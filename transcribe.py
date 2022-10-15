from pytube import Playlist
from pytube import YouTube

# this is the twiml AI podcast playlist - all episodes
#p = Playlist('https://www.youtube.com/playlist?list=PLILZm3MRkvH83C46bZ4rPmB-jKWBltWkP')

TWIML_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLILZm3MRkvH83C46bZ4rPmB-jKWBltWkP"
PATH = "twiml-episodes"

# # from a youtube playlist, get all the video urls and titles and print them to the console
# for url in p.video_urls:
#     yt = YouTube(url)
#     print(yt.title)
#     #print(yt.streams.filter(only_audio=True).first().download())



# from a youtube playlist, get all the video urls, titles, and episode numbers and save them to a text file
def savePlaylistToFile(playlist_url):
    p = Playlist(playlist_url)
    with open('twiml-playlist.txt', 'w', encoding="utf8") as f:
        for index, url in enumerate(p.video_urls, start=1):
            yt = YouTube(url)
            print(index, '|' + yt.title + '|' + url )
            f.write(str(index) + '|' + yt.title + '|' + url + '\n')
        print("Playlist saved to file twiml-playlist.txt with " + str(index) + " episodes.")

# from a youtube playlist, get the video url, title, and save it as a mp3 file
def downloadVideoFromPlaylist(playlist_url, path):
    playlist = Playlist(playlist_url)
    for index, video in enumerate(playlist.videos, start=1):
        print("Downloading #" + str(index) + " ... " + video.title)
        try:
            tempFileName = validFilename(str(index) + '_ ' + video.title + ".mp3")
            video.streams.filter(only_audio=True).first().download(output_path=PATH, filename=tempFileName)
        except IOError:
            print("Error: can\'t save the following file. Most likely it has an invalid character in the name.")
            print("File: " + tempFileName)
    print("Download complete. Number of episodes downloaded: " + str(index))


# download mp3 from youtube video url
def downloadVideoFromURL(video_url, path):
    yt = YouTube(video_url)
    tempFileName = validFilename(yt.title + ".mp3")
    yt.streams.filter(only_audio=True).first().download(output_path=PATH, filename=yt.title + ".mp3")
    print("File downloaded: " + yt.title+".mp3")

# check if a filename is valid
def is_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return all(c.isalnum() or c in "._-()" for c in s)

def validFilename(s):
    s = str(s).strip().replace(' ', '_')
    s = str(s).strip().replace('/', '-')
    return s
    #return all(c.isalnum() or c in "._-()" for c in s)

#savePlaylistToFile(TWIML_PLAYLIST_URL)
#downloadVideoFromURL("https://www.youtube.com/watch?v=YgQxlKPeC-g", PATH)
downloadVideoFromPlaylist(TWIML_PLAYLIST_URL, PATH)
