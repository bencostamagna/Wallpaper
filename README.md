# Wallpaper

This utility downloads the most upvoted image of the day on the subreddit /r/earthporn and sets it as a wallpaper, it also writes the title of the post in a text file to display alongside.

## Usage

./wallpaper.py storage_folder subreddit
ex: ./wallpaper.py /home/ben/.background /R/earthporn

## Setup

the script should be run periodically using anacron or a similar utility.

## Compatibility

### Linux

Runs properly on cinnammon. The image is set as desktop background automatically and the file description can be displayed on desktop using conky.

### Windows

The file is downloaded to a folder, windows can then be set to fetch wallpapers from that folder.
