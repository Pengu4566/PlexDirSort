#first commit, nothing here!

import os
import re
import sys
import glob
import shutil
import subprocess
import qbittorrentapi
from shutil import copy
from datetime import datetime

### SETTINGS ###
copy_destination = "Z:/"
music_destination = "C:/Users/mihal/Desktop"
log_destination = "C:/Users/mihal/Desktop"
### SETTINGS ###

# uses QBitTorrent api to control the current torrent
def qbitLogin():
    print(1)
    # https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-Documentation#get-torrent-list

def logToFile(log_text):
    f = open(log_destination + "/log.txt", "a")
    f.write(log_text)
    f.close()

# thanks to renanbs on GitHub: https://github.com/renanbs/extractor/blob/master/LICENSE
def multiRarUnzip(torrent_name, torrent_root_path):

    # print(glob.glob(torrent_root_path + "\\**.rar"))
    logToFile(str(datetime.now()) + " [tvSort] - multiRAR detected, unzipping to destination: " + copy_destination + "\n")
    path_list = glob.glob(torrent_root_path + "\\**.rar")
    for path in path_list:
        path_in_str = str(path)
        out = subprocess.run(["unrar", "e", path_in_str, copy_destination], stdout=subprocess.DEVNULL)
        if not out.returncode:
            logToFile(str(datetime.now()) + " " + torrent_name + " - [ OK ] \n")
        else:
            logToFile(str(datetime.now()) + " " + torrent_name + " - [ ERROR ]  \n")

def copySomething(root_folder, file_to_copy):
    logToFile(str(datetime.now()) + " [copySomething] - copying file: " + file_to_copy + " to destination: " + copy_destination + "\n")
    copy(str(root_folder + "/" + file_to_copy), copy_destination)
    logToFile(str(datetime.now()) + " [copySomething] - COPY COMPLETE \n")

def musicSort(torrent_name, torrent_root_path):

    confirm_number = 0
    confirmation = False

    for (root,dirs,files) in os.walk(torrent_root_path):
        for file in files:
            # copies all mkv files in torrent folder
            if str(file).__contains__(".mp3") | str(file).__contains__(".flac") | str(file).__contains__(".FLAC") | str(file).__contains__(".wav") | str(file).__contains__(".WAV"):
                # copy the whole folder, not just individual files in folder
                print(file)
                confirm_number += 1
                no_association = False

                # if more than 65% of files in folder are music, this is most likely an album
                if confirm_number / len(files) > 0.65:
                    confirmation = True

    # files inside torrent are verified to be music files
    if confirmation == True:
        shutil.copytree(torrent_root_path, music_destination + "/" + torrent_name)

# TODO handle torrents that just leave a file in the downloads folder

    # check to see if the above logic didnt capture a file
    if no_association == True:
        logToFile("[musicSort] - NO ASSOCIATIONS FOR -MUSIC- TORRENT - " + torrent_name + " \n")

def tvSort(torrent_name, torrent_root_path):

    for (root,dirs,files) in os.walk(torrent_root_path):
        for file in files:
            # copies all mkv files in torrent folder
            if str(file).__contains__(".mkv") | str(file).__contains__(".avi") | str(file).__contains__(".mp4") | str(file).__contains__(".wmv"):
                copySomething(root, file)
                logToFile(file + "***\n")

                no_association = False

            # rar file discovered, begin unzipping
            elif str(file).__contains__(".rar"):
                multiRarUnzip(torrent_name, torrent_root_path)
                no_association = False

    # check to see if the above logic didnt capture a file
    if no_association == True:
        logToFile("[tvSort] - NO ASSOCIATIONS FOR -TV- TORRENT - " + torrent_name + " \n")

def movieSort(torrent_name, torrent_root_path):
    #print(torrent_root_path)
    #os.mkdir(str(torrent_root_path + "/hacked bitchhh"))
    no_association = True

    for (root,dirs,files) in os.walk(torrent_root_path):
        for file in files:
            # copies all mkv files in torrent folder except small SAMPLE clips
            if str(file).__contains__(".mkv") | str(file).__contains__(".avi") | str(file).__contains__(".mp4") | str(file).__contains__(".wmv") and not str(file).__contains__("sample"):
                copySomething(root, file)
                no_association = False

            # rar file discovered, begin unzipping
            elif str(file).__contains__(".rar"):
                multiRarUnzip(torrent_name, torrent_root_path)
                no_association = False

    # check to see if the above logic didnt capture a file
    if no_association == True:
        logToFile("[movieSort] - NO ASSOCIATIONS FOR -MOVIE- TORRENT - " + torrent_name + " \n")

def ebookSort(torrent_name, torrent_root_path):
    for (root,dirs,files) in os.walk(torrent_root_path):
        for file in files:
            copy(str(root + "/" + file), copy_destination)
            logToFile(str(datetime.now()) + " [ebookSort] - copying file: " + file + " to destination: " + copy_destination + "\n")

def main():
    print(str(sys.argv))
    torrent_name = sys.argv[1]
    torrent_root_path = sys.argv[2]
    # .replace("\\", "/")
    # os.mkdir(str("C:/Users/mihal/Desktop/" + sys.argv[1]))
    logToFile(str(datetime.now()) + "---------------------------------------------------------------\n")
    logToFile(str(datetime.now()) + " [main] - NEW TORRENT: " + torrent_name + "\n")

    # check if TV show single
    S_E_regex = re.compile('S[0-9][0-9]E[0-9][0-9]')
    S_E_match = re.search(S_E_regex, torrent_name)
    #logToFile(str(datetime.now()) + " [main] - REGEX MATCH" + str(S_E_match) + "\n")

    # TV show entire season/show
    S_regex = re.compile('S[0-9][0-9]')
    S_match =re.search(S_regex, torrent_name)
    #logToFile(str(datetime.now()) + " [main] - REGEX MATCH" + str(S_match) + "\n")

    # if tv show do stuff
    if S_E_match:
        # single file detected, simply copy it to destination
        #TODO handle single file without folder
        #if(torrent_root_path.__contains__(".mkv") | torrent_root_path.__contains__(".avi") | torrent_root_path.__contains__(".mp4") | torrent_root_path.__contains__(".wmv") and not torrent_root_path.__contains__("sample")):
            #copySomething(torrent_root_path, file)
        #else:
        logToFile(str(datetime.now()) + " [main] - TV detected \n")
        tvSort(torrent_name, torrent_root_path)

    # not tv show, must be movie
    elif torrent_name.__contains__("x264") | torrent_name.__contains__("1080p") | torrent_name.__contains__("720p"):
        logToFile(str(datetime.now()) + " [main] - MOVIE detected \n")
        movieSort(torrent_name, torrent_root_path)

    # might be music too
    elif torrent_name.__contains__("FLAC") | torrent_name.__contains__("320") | torrent_name.__contains__("v0") | torrent_name.__contains__("v2") | torrent_name.__contains__("WAV"):
        logToFile(str(datetime.now()) + " [main] - MUSIC detected \n")
        musicSort(torrent_name, torrent_root_path)

    # oh yeah ebooks sometimes get copied
    elif torrent_root_path.__contains__(".pdf") | torrent_root_path.__contains__(".mobi"):
        ebookSort(torrent_name, torrent_root_path)

    else:
        logToFile("***NO ASSOCIATIONS FOR TORRENT - " + torrent_name + "***\n")

main()