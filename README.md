# Wallpaper

This utility downloads the most upvoted image of the day on a subreddit and sets it as a wallpaper, it also writes the title of the post in a text file to display alongside.

## Usage

./wallpaper.py

## Setup

The script should be run periodically using anacron or a similar utility.
A configuration file called wallpaper.ini should be placed in the same folder as wallpaper.py (see sample file)

## Compatibility

### Linux

Runs properly on cinnammon. The image is set as desktop background automatically and the file description can be displayed on desktop using conky.

### Windows

The file is downloaded to a folder, windows can then be set to fetch wallpapers from that folder.
toaster.py can be used to display the label of the picture.
