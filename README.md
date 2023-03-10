# archive_tools-python
The tools I use for archive handling.

-

create_playlist.py creates playlists from text files whose contents are solely one path per line, each to one file.
It will also read the line and replace (some) invalid characters internally to match that of the proper file(s). 
These text files can be created from <https://github.com/yt-dlp/yt-dlp> using a Youtube playlist as the input, and using the switch: 

``` --print-to-file after_move:"../../%(channel)s - [%(channel_id)s]/%(playlist_title)s - [%(playlist_id)s]/%(upload_date)s - %(title)s - [%(id)s] - %(resolution)s.%(ext)s" "%(playlist_uploader)s - [%(playlist_uploader_id)s]/%(playlist_title)s - [%(playlist_id)s]/- %(playlist_title)s - [%(playlist_id)s]-playlist.txt" ``` 

This script will only work if the media file is created using: 

``` -o "%(channel)s - [%(channel_id)s]/%(playlist_title)s - [%(playlist_id)s]/%(upload_date)s - %(title)s - [%(id)s] - %(resolution)s.%(ext)s" ```

You can do it in whatever way you please, just make sure your paths match eachother. If your directory count is different, the script can tell. You may also need to change the regex string for detecting seperate directories if you do it different from the switch shown above. If your character replacement method is different from "yt-dlp", you must change that in the script as well.

-

create_symlinks.py will create relative symlinks within folders whose name is specified in a list in a text file. I probably could have used the associated json files for this, but I wanted to try it this way for now.
This text file must be created from https://github.com/mikf/gallery-dl using the "postprocessors" section of the "config.json" file included here. Personal information was removed only from the "deviantart" section. Place your "id", "secret", and "refresh-token" codes there instead. Commands are included in "gallery-dl_commands.txt". I use MS Edge, so just change this to Chrome or Firefox if you use those.
The config file is configured so as to write the list of folders to line 21 in the generated text file. If yours is different, modify the script to choose the correct line.

-

batch_download.py downloads all files of the extension specified if they exist as direct links to files. Modify the script to select the file type you need. If you can inspect a webpage and the links to the files exist in the html, this will retrieve them.
