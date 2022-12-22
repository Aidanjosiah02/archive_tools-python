# Used to create a playlist file out of the text files generated from: 
# --print-to-file after_move:"../../%(channel)s - [%(channel_id)s]/%(playlist_title)s - [%(playlist_id)s]/%(upload_date)s - %(title)s - [%(id)s] - %(resolution)s.%(ext)s" "%(playlist_uploader)s - [%(playlist_uploader_id)s]/%(playlist_title)s - [%(playlist_id)s]/- %(playlist_title)s - [%(playlist_id)s]-playlist.txt".
# To view the file(s) that this script refers to, enter the directory of any Youtube channel's playlist. In there you should find a file named as: 
# "- %(playlist_title)s - [%(playlist_id)s]-playlist.txt"

import pathlib
import re
import xml.etree.ElementTree as xml

DIRECTORY = pathlib.Path(".")
regex_pattern = r'([^/\\]+)(-playlist.txt)$'

class Playlist: # Build xml playlist
	def __init__(self): # tree structure
		self.playlist = xml.Element('playlist')
		self.tree = xml.ElementTree(self.playlist)
		self.playlist.set('xmlns','http://xspf.org/ns/0/')
		self.playlist.set('xmlns:vlc','http://www.videolan.org/vlc/playlist/ns/0/')
		self.playlist.set('version', '1')
		self.title = xml.Element('title')
		self.playlist.append(self.title)
		self.title.text = 'Playlist'
		self.trackList = xml.Element('trackList')
		self.playlist.append(self.trackList)

	def add_track(self, path):  # Add tracks to xml tree (within trackList).
		track = xml.Element('track')
		location = xml.Element('location')
		location.text = path
		track.append(location)
		self.trackList.append(track)
	
	def get_playlist(self): # Return complete playlist with tracks.
		return self.playlist

def write_playlist(path_list):
	playlist = Playlist()
	for path in path_list:
		playlist.add_track(path)
	playlist_xml = playlist.get_playlist()
	with open('songs.xspf','w') as playlist_file:
		playlist_file.write(xml.tostring(playlist_xml).decode('utf-8'))





path_list = []
fail_list = []
file_list = {file for file in DIRECTORY.iterdir() if file.is_file()}
for file in file_list:
    match = re.match(regex_pattern, str(file))
    if match:
        with open(file, 'r') as dir_index:  # file closes itself when done
            contents_dir = dir_index.read().splitlines()
            for line in contents_dir:
                if pathlib.Path(line).exists():
                    path_list.append(line)
                else:
                    fail_list.append(line)
                    print("fail on line " + str(contents_dir.index(line)))

if len(fail_list)==0 and len(path_list) != 0:
    write_playlist(path_list)
else:
    print("Some lines are not recognized as valid directories, and thus no playlist file has been created.")
    while True:
        try:
            q_continue = input("Do you wish to create one anyway despite potentially missing " + str(len(fail_list)) + " file(s)? (y/n): ")
            if q_continue == "y":
                write_playlist(path_list)
                break
            elif q_continue == "n":
                exit()
            else:
                print("\"" + str(q_continue) + "\"" + " is not a valid input. Please try again.")
        except ValueError:
            continue