#! /usr/bin/python3

import sys
import urllib.request
import json
from subprocess import call
import os



def usage():
    print("./wallpaper.py storage_folder subreddit")


if len (sys.argv) != 3:
    usage()
    sys.exit(1)

storage_folder=sys.argv[1]
subreddit=sys.argv[2]

image_path=storage_folder+"/wallpaper.jpg"
description_path=storage_folder+"/wallpaper.txt"

index_url="http://reddit.com"+subreddit+"/top.json?limit=1"
pagecontent = urllib.request.urlopen(index_url).read().decode('utf-8')

postinfo = json.loads(pagecontent)
image_url = postinfo["data"]["children"][0]["data"]["preview"]["images"][0]["source"]["url"]
image_description =  postinfo["data"]["children"][0]["data"]["title"]

data = urllib.request.urlopen(image_url).read()
if (len(data) <= 0):
    sys.exit(1)

imgfile = open(image_path, 'wb+')
imgfile.write(data)
imgfile.close()

descfile = open(description_path, 'w+')
descfile.write(image_description)
descfile.close()


# Applying wallpaper changes, depending on the os and desktop manager

if (os.name == "nt"): # Windows
    pass
elif (os.name == "posix"): # Linux
    call(["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", "file:"+image_path])
