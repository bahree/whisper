# If you don't have pytube installed, then install it first using the following command: # pip install pytube
import sys
from time import process_time_ns
from turtle import width
from pytube import Playlist
from pytube import YouTube
from pytube.cli import on_progress
from pytube.exceptions import VideoUnavailable

# this is the twiml AI podcast playlist - all episodes
TWIML_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLILZm3MRkvH83C46bZ4rPmB-jKWBltWkP"
MP3_PATH = "twiml-episodes"
MP3_PATH_TEST = "twiml-episodes-test"
TWIML_PLAYLIST_FILENAME = "twiml-playlist.txt"

# We use basic ANSI escape codes to color the output. These are all foreground colors.
class textColors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    MAGENTA = '\x1b[35m'
    CYAN = '\x1b[36m'
    BLACK = '\x1b[30m'
    WHITE = '\x1b[37m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    UNDERLINE = '\033[4m' 

# Callback function to show a simple progress bar for the file download
def show_progress_bar(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = (bytes_downloaded / total_size) * 100
        print(f"\t{textColors.GREEN}Downloaded {percentage_of_completion:.2f}%{textColors.RESET}")

# Callback function to show a fancier progress bar for the file download
def fancy_progress_bar(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = (bytes_downloaded / total_size) * 100
        width = int(percentage_of_completion / 4)
        bar = "[" + "#" * width + " " * (25 - width) + "] " + str(int(percentage_of_completion)) + "%"
        sys.stdout.write(u"\u001b[1000D" +  bar)
        sys.stdout.flush()

# For a given youtube playlist, get all the video urls, titles, and episode numbers and save them to a text file
def savePlaylistToFile(playlist_url, playlist_filename):
    p = Playlist(playlist_url)
    with open(playlist_filename, 'w', encoding="utf8") as f:
        for index, url in enumerate(p.video_urls, start=1):
            yt = YouTube(url)
            print(index, '|' + yt.title + '|' + url )
            f.write(str(index) + '|' + yt.title + '|' + url + '\n')
        print("Playlist saved to file" + playlist_filename + " with " + str(index) + " episodes.")


# Download all the videos from a youtube playlist, and save it as a mp3 file
def downloadVideoFromPlaylist(playlist_url, path):
    playlist = Playlist(playlist_url)
    fileSaved = 0
    for index, video in enumerate(playlist.videos, start=1):
        # if index < 286:
        #     continue
        print("\nDownloading #" + str(index) + " ... " + video.title)
        try:
            tempFileName = validFilename(str(index) + '_' + video.title + ".mp3")
            video.register_on_progress_callback(fancy_progress_bar)
            video.streams.filter(only_audio=True).first().download(output_path=MP3_PATH, filename=tempFileName)
            fileSaved += 1        
        except IOError:
            print(f"{textColors.FAIL}Error: can\'t save the following file. Most likely it has an invalid character in the name.{textColors.RESET}")
            print("File: " + tempFileName)
        except VideoUnavailable:
            print("{textColors.FAIL}Video: " + tempFileName + " is unavailable, skipping.{textColors.RESET}")
        except:
            print("{textColors.FAIL}Unexpected error: " + sys.exc_info()[0] + "{textColors.RESET}")
    print("Download complete. Number of episodes saved: " + str(fileSaved))

        
#testing ignore
# from a youtube playlist, get the video url, title, and save it as a mp3 file
# def new_downloadVideoFromPlaylist(playlist_url, path):
#     playlist = Playlist(playlist_url)
#     length = playlist.length
#     print(f"{textColors.CYAN}" + str(length) + f"{textColors.RESET} episodes found. Starting download...")
#     for index, video in enumerate(playlist.videos, start=1):
#         print("\nDownloading #" + str(index) + "/" + str(length) + " ... " + video.title)
#         try:
#             tempFileName = validFilename(str(index) + '_' + video.title + ".mp3")
#             video.register_on_progress_callback(fancy_progress_bar)
#             video.streams.filter(only_audio=True).first().download(output_path=MP3_PATH_TEST, filename=tempFileName)
#         except IOError:
#             print(f"{textColors.FAIL}Error: can\'t save the following file. Most likely it has an invalid character in the name.{textColors.RESET}")
#             print("File: " + tempFileName)
#         except VideoUnavailable:
#             print(f"{textColors.FAIL}Video: " + tempFileName + " is unavailable, skipping.{textColors.RESET}")
#     print("Download complete. Number of episodes downloaded: " + str(index))


# download mp3 from youtube video url
def downloadVideoFromURL(video_url, path):
    yt = YouTube(video_url)
    yt.register_on_progress_callback(fancy_progress_bar)
    tempFileName = validFilename(yt.title + ".mp3")
    yt.streams.filter(only_audio=True).first().download(output_path=MP3_PATH, filename=tempFileName)
    print("\nFile downloaded: " + tempFileName)

# convert a string to a valid filename
def validFilename(s):
    s = str(s).strip().replace(' ', '_')
    s = str(s).strip().replace('/', '-')
    s = str(s).strip().replace('&', 'and')
    s = str(s).strip().replace('\'', '')
    s = str(s).strip().replace('"', '')
    s = str(s).strip().replace(':', '-')
    s = str(s).strip().replace('*', '')
    s = str(s).strip().replace('?', '')
    return s

# This is equivalent to main() where the program starts.
# Main menu - choose what we want to do:
print("What you want to do?")
print("1. For a given playlist, save the details of the episodes (metadata) to a file ")
print("2. Download and save as mp3 files, all the episode for a playlist")
print("3. Download a single video and save as mp3 (for a given URL)")
print("0. I changed my mind, I don't want to do anything")

# This is clunky, but the intent is to make it simple.
try:
    choice = int(input(f"{textColors.MAGENTA}Enter your choice (1-3):{textColors.RESET} "))
except ValueError:
    print(f"{textColors.WARNING}That's not an integer! Exiting...{textColors.RESET}")
    sys.exit(1)

if choice == 0:
    print(f"{textColors.OK}No worries. Exiting.{textColors.RESET}")
    sys.exit(0)
elif choice == 1:
    print("\n\nSaving details of the following playlist:" + TWIML_PLAYLIST_URL + "\n to the file:" + TWIML_PLAYLIST_FILENAME)
    answer = input("Are you sure you want to do this? [default: n] (y/n):")
    if answer == 'y':
        savePlaylistToFile(TWIML_PLAYLIST_URL, TWIML_PLAYLIST_FILENAME)
    else:
        print("Skipping. Thanks for playing...")
        sys.exit(0)
elif choice == 2:
    print("\n\nDownloading all episodes from playlist:" + TWIML_PLAYLIST_URL + "\nand saving to this location:" + MP3_PATH)
    answer = input(f"{textColors.WARNING}This can take a *long* time, and possibly gobble up a lot of *bandwidth*. \nContinue? [default: n] (y/n): {textColors.RESET}")
    if answer == 'y':
        downloadVideoFromPlaylist(TWIML_PLAYLIST_URL, MP3_PATH)
    else:
        print("Skipping. Thanks for playing...")
        sys.exit(0)
elif choice == 3:
    print("\n\nEnter the URL of the episode you want to download:")
    url = input()
    print("Downloading episode from URL: " + url + "\nand saving to this location:" + MP3_PATH)
    downloadVideoFromURL(url, MP3_PATH)
else:
    print(f"{textColors.WARNING}Invalid choice. Exiting.{textColors.RESET}")
