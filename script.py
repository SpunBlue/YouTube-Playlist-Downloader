import os
import shutil
from pytube import Playlist
from moviepy.editor import *

# Get the link to the YouTube playlist
playlist_url = input("Enter the YouTube playlist URL: ")

# Create a Playlist object
playlist = Playlist(playlist_url)

# Create a folder for the downloaded videos
folder_name = playlist.title
forced_name = input("Folder Name (Leave Blank for Playlist Title):")

# Specify resolution
specified_reso = input("Specific Resolution for Videos (1080p is the max)\nExample: '720p', Leave blank for automatic, or type 'quick' for quickest\nWarning! Specific resolutions are slower to download\nResolution: ")

# Lol
if (specified_reso == '360p' or specified_reso == '240p' or specified_reso == '144p'):
    print("Seriously? " + specified_reso + "???")

if (forced_name != ""):
    folder_name = forced_name

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Create Temporary Folder for Conversion 
temp_folder = os.path.join(folder_name, "temp")
    
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)
    
def downloadConv(video, reso:str):
        print("Downloading " + reso +  " Video, but we will have to do some converting...")
        # Do some converting bullshit so the video will actually contain audio
        video_file = video.streams.filter(res=reso).first().download(output_path=temp_folder)
        
        # Don't remember why I made it save like this, but it doesn't matter.
        audio_stream = video.streams.filter(adaptive=True, only_audio=True).first()
        audio_file = audio_stream.download(output_path=os.path.join(temp_folder, "audio"))
        
        video = VideoFileClip(video_file)
        audio = AudioFileClip(audio_file)
        
        # Write audio to video and save video.
        final_video = video.set_audio(audio) # The fact you have to do it like this is so fucking retarded.
        final_video.write_videofile(os.path.join(folder_name, os.path.basename(video_file)), codec='libx264')
        
        # Remove junk
        try:
            os.remove(video_file)
            os.remove(audio_file)
        except Exception as e:
            print("Error: ", str(e))
        
        print("Converting complete!")
        return

# Download each video in the playlist
for video in playlist.videos:
    # Download the highest resolution video to the main folder
    if specified_reso.lower() == "quick" or specified_reso == "720p":
        print("Downloading...")
        video.streams.get_highest_resolution().download(output_path=folder_name)
    elif specified_reso != "" and video.streams.filter(res=specified_reso).first() is not None:
        downloadConv(video, specified_reso)
    elif video.streams.filter(res="1080p").first() is not None:
        if (specified_reso != ""):
            print(specified_reso + " is not avaliable.")
        
        downloadConv(video, "1080p")
    else:
        print("1080p Video not avaliable, Downloading highest resolution avaliable.")

        video.streams.get_highest_resolution().download(output_path=folder_name)
    
try:
    shutil.rmtree(temp_folder) # Wouldn't delete with os.removedirs for some reason.
except Exception as e:
    print("Error: ", str(e))

print("Download complete!")