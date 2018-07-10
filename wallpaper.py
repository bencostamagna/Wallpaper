#! /usr/bin/python3

import sys
import urllib.request
import json
import configparser, logging
from subprocess import call
import os
import re
if (os.name == "nt"): # Windows
    import ctypes



def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def getScreenRatio():
    if (os.name == "nt"): # Windows
        return ctypes.windll.user32.GetSystemMetrics(0)/ctypes.windll.user32.GetSystemMetrics(1)
    else:
        return 1.77 # default to 16/9

def setBackground():
    if (os.name == "nt"): # Windows
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path , 3)
    elif (os.name == "posix"): # Linux
        call(["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", "file:"+image_path])


config = configparser.ConfigParser()
config.read(os.path.join(getScriptPath(), 'wallpaper.ini'))

subreddit=config['Source']['subreddit']
image_path=config['Files']['image_path']
description_path=config['Files']['description_path']
log_path=config['Files']['log_path']

user_agent="WallpaperFetcher"


if (len(log_path) > 0):
    try:
        os.remove(log_path)
    except OSError:
        pass
    logging.basicConfig(level=logging.DEBUG, filename=log_path, format='[%(asctime)s]: %(levelname)s:  %(message)s')

try:
    screen_ratio = getScreenRatio()
    logging.info("Screen ratio is "+ str(screen_ratio))

    image_url=""
    image_description=""

    index_url="http://reddit.com/r/"+subreddit+"/top.json?limit=25"
    logging.info("Fetching reddit data from "+ index_url + "...")

    pagecontent = urllib.request.urlopen(urllib.request.Request(index_url, None, {'User-Agent': user_agent})).read().decode('utf-8')
    postinfo = json.loads(pagecontent)

    # with open('test.json') as json_data:
    #     postinfo = json.load(json_data)

    for index in range(len(postinfo["data"]["children"])):
        width = int(postinfo["data"]["children"][index]["data"]["preview"]["images"][0]["source"]["width"])
        height = int(postinfo["data"]["children"][index]["data"]["preview"]["images"][0]["source"]["height"])
        ratio = width/height
        if ratio < screen_ratio*0.8 or ratio > screen_ratio*1.2:
            logging.info("Image "+ str(index) + " rejected with ratio of " + str(ratio))
            continue

        logging.info("Image "+ str(index) + " SELECTED with ratio of " + str(ratio))

        image_url = postinfo["data"]["children"][index]["data"]["preview"]["images"][0]["source"]["url"]
        image_description =  postinfo["data"]["children"][index]["data"]["title"]
        break

    if (len(image_url) == 0):
        sys.exit(1)

    logging.info("Fetching data from "+ image_url)
    data = urllib.request.urlopen(urllib.request.Request(image_url, None, {'User-Agent': user_agent})).read()
    if (len(data) <= 0):
        sys.exit(1)

    logging.info("Saving to file...")
    imgfile = open(image_path, 'wb+')
    imgfile.write(data)
    imgfile.close()

    descfile = open(description_path, 'w+')
    descfile.write(re.sub(r'\[[^)]*\]', '', image_description))
    descfile.close()

    logging.info("Setting downloaded image as background...")
    setBackground()

except:
    logging.exception("Exception raised: ")
