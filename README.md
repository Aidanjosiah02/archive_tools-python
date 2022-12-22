# archive_tools-python
The tools I use for archive handling.

-

create_playlist.py creates playlists from text files whose contents are solely one path per line, each to one file.
These text files can be created from <https://github.com/yt-dlp/yt-dlp> using a Youtube playlist as the input, and using the switch: 

``` --print-to-file after_move:"../../%(channel)s - [%(channel_id)s]/%(playlist_title)s - [%(playlist_id)s]/%(upload_date)s - %(title)s - [%(id)s] - %(resolution)s.%(ext)s" "%(playlist_uploader)s - [%(playlist_uploader_id)s]/%(playlist_title)s - [%(playlist_id)s]/- %(playlist_title)s - [%(playlist_id)s]-playlist.txt" ``` 

This script will only work if the media file is created using: 

``` -o "%(channel)s - [%(channel_id)s]/%(playlist_title)s - [%(playlist_id)s]/%(upload_date)s - %(title)s - [%(id)s] - %(resolution)s.%(ext)s" ```
