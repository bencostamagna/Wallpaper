#! /usr/bin/python3

import sys
import urllib.request
import json
from subprocess import call
import os



def usage():
    print("./wallpaper.py storage_folder subreddit")


def getScreenRatio():
    if (os.name == "nt"): # Windows
        import ctypes
        return ctypes.windll.user32.GetSystemMetrics(0)/ctypes.windll.user32.GetSystemMetrics(1)
    else:
        return 1.77 # default to 16/9

def setBackground():
    if (os.name == "nt"): # Windows
        pass
    elif (os.name == "posix"): # Linux
        call(["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", "file:"+image_path])



if len (sys.argv) < 3:
    print (sys.argv)
    usage()
    sys.exit(1)

storage_folder=sys.argv[1]
subreddit=sys.argv[2]

screen_ratio = getScreenRatio()

image_path=storage_folder+"/wallpaper.jpg"
description_path=storage_folder+"/wallpaper.txt"
image_url=""
image_description=""

index_url="http://reddit.com"+subreddit+"/top.json?limit=25"
pagecontent = urllib.request.urlopen(index_url).read().decode('utf-8')
postinfo = json.loads(pagecontent)

# with open('test.json') as json_data:
#     postinfo = json.load(json_data)

for index in range(len(postinfo["data"]["children"])):
    width = int(postinfo["data"]["children"][index]["data"]["preview"]["images"][0]["source"]["width"])
    height = int(postinfo["data"]["children"][index]["data"]["preview"]["images"][0]["source"]["height"])
    ratio = width/height
    # print("image " + str(index) + ": "+str(width)+"x"+str(height)+" ratio="+str(ratio))
    if ratio < screen_ratio*0.8 or ratio > screen_ratio*1.2:
        continue
    # print ("selected")
    image_url = postinfo["data"]["children"][index]["data"]["preview"]["images"][0]["source"]["url"]
    image_description =  postinfo["data"]["children"][index]["data"]["title"]
    break

if (len(image_url) == 0):
    sys.exit(1)

data = urllib.request.urlopen(image_url).read()
if (len(data) <= 0):
    sys.exit(1)

imgfile = open(image_path, 'wb+')
imgfile.write(data)
imgfile.close()

descfile = open(description_path, 'w+')
descfile.write(image_description)
descfile.close()

setBackground()
