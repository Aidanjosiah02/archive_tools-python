# Used to create a playlist file out of the text files generated from: 
# --print-to-file after_move:"../../%(channel)s - [%(channel_id)s]/%(playlist_title)s - [%(playlist_id)s]/%(upload_date)s - %(title)s - [%(id)s] - %(resolution)s.%(ext)s" "%(playlist_uploader)s - [%(playlist_uploader_id)s]/%(playlist_title)s - [%(playlist_id)s]/- %(playlist_title)s - [%(playlist_id)s]-playlist.txt".
# To view the file(s) that this script refers to, enter the directory of any Youtube channel's playlist. In there you should find a file named as: 
# "- %(playlist_title)s - [%(playlist_id)s]-playlist.txt"

from sys import platform
from pathlib import Path
import re
import xml.etree.ElementTree as xml

DIRECTORY_REL = Path(".")
DIRECTORY_ABS = Path.cwd()
playlist_pattern = r'([^/\\]+)(-playlist.txt)$'
split_dir = r'(\.\./)(\.\./)(.*\[[0-9]+]/)(.*\[[0-9]+]/)'
split_group = r'(\.\./\.\./.*\[[0-9]+]/.*\[[0-9]+]/)'


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


class Replace_chars:
	def safe(item):
		replace1 = item.replace(r'/+', '_')
		replace2 = replace1.replace(':', ' -')
		replace3 = replace2.replace('?', '')
		return replace3

	def special(item):
		replace1 = item.replace('/', '⧸')
		replace2 = replace1.replace(':', '：')
		replace3 = replace2.replace('?', '？')
		return replace3


def write_playlist(path_list):
	playlist = Playlist()
	for path in path_list:
		playlist.add_track(path)
	playlist_xml = playlist.get_playlist()
	with open('songs.xspf','w',encoding='utf8') as playlist_file:
		playlist_file.write(xml.tostring(playlist_xml, encoding='utf8').decode('utf-8'))


print("The following request for input is in regards to your naming method while using \"yt-dlp\". Select 1. 2. or 3..\n")
print("1. If the applicable files were created on Windows using only the default naming method.")
print("2. If the files were created using \"--compat-options filename-sanitization\", or \"youtube-dl\".")
print("3. If the names of all the applicable files exactly match those mentioned in the file with the suffix \"-playlist.txt\".\n")
user_chars = int(input("Enter 1, 2, or 3: "))
user_path = int(input("Print to file: 1. relative path, 2. absolute path to working directory (Enter 1 or 2): "))


merged_paths = []
fail_path_prep = []
file_list = {file for file in DIRECTORY_REL.iterdir() if file.is_file()}
for file in file_list:
	match = re.match(playlist_pattern, str(file))
	if match:
		try:
			with open(file, 'r', encoding='utf-8') as dir_index:  # file closes itself when done
				contents_dir = dir_index.read().splitlines()
				for line in contents_dir:
					try:
						paths = re.split(split_dir, line)
						replaced_names = []
						all_names = []
						if user_path == 1:
							for dir in paths[1:5]:
								remove_slash = dir[: len(dir) - 1]
								all_names.append(remove_slash)
							all_names.append(paths[5])
							if user_chars == 3:
								for item in all_names:
									replaced_names.append(item)
							else:
								if user_chars == 1:
									for item in all_names:
										replace = Replace_chars.special(item)
										replaced_names.append(replace)
								elif user_chars == 2:
									for item in all_names:
										replace = Replace_chars.safe(item)
										replaced_names.append(replace)

						elif user_path == 2:
							replaced_names.append(str(DIRECTORY_ABS))
							if user_chars == 1:
								replace = Replace_chars.special(paths[5])
								replaced_names.append(replace)
							elif user_chars == 2:
								replace = Replace_chars.safe(paths[5])
								replaced_names.append(replace)
							elif user_chars == 3:
								replaced_names.append(paths[5])
								
						if platform == "win32":
							merged_paths.append("\\".join(replaced_names))
						else:
							merged_paths.append("/".join(replaced_names))
					except:
						fail_path_prep.append(line)
		except IOError:
			print("Failed to open " + str(file))
	


invalid_paths = []
valid_paths = []
for path in merged_paths:
	if Path(path).exists():
		valid_paths.append(path)
	else:
		invalid_paths.append(path)


if len(invalid_paths) == 0 and len(fail_path_prep) == 0 and len(merged_paths) != 0:
	write_playlist(valid_paths)
else:
	print("Some lines are not recognized as valid directories, and thus no playlist file has been created.")
	while True:
		try:
			q_continue = input("Do you wish to create one anyway despite potentially missing " + str(len(fail_path_prep) + len(invalid_paths)) + " file(s)? (y/n): ")
			if q_continue == "y":
				write_playlist(valid_paths)
				break
			elif q_continue == "n":
				break
			else:
				print("\"" + str(q_continue) + "\"" + " is not a valid input. Please try again.")
		except ValueError:
			continue
	while True:
		try:
			q_write_file = input("Do you want to write these failed paths/lines to a file? (y/n): ")
			if q_write_file == "y":
				with open('failed_playlist_paths.txt', 'a') as file_write:
					if len(fail_path_prep) > 0:
						file_write.write("Some problem in processing the string(s):\n")
						for path in fail_path_prep:
							file_write.write(path + "\n")
						if len(invalid_paths) > 0:
							file_write.write("\n")
					if len(invalid_paths) > 0:
						file_write.write("Invalid path(s):\n")
						for path in invalid_paths:
							file_write.write(path + "\n")
					break
			elif q_write_file == "n":
				exit()
			else:
				print("\"" + str(q_write_file) + "\"" + " is not a valid input. Please try again.")
		except ValueError:
			continue