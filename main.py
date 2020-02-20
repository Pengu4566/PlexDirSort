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

import PathGenerator as PathGen

### SETTINGS ###
MOVIE_TV_DESTINATION = "Z:\\"
MUSIC_DESTINATION = "C:\\Users\\mihal\\Desktop"
LOG_DESTINATION = "C:\\Users\\mihal\\Desktop"
TORRENT_FOLDER = "H:\\Torrent\\Downloaded Torrents"
### SETTINGS ###

# uses QBitTorrent api to control the current torrent
def qbitLogin():
    print(1)
    # https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-Documentation#get-torrent-list

def logToFile(log_text):
    f = open(LOG_DESTINATION + "\\log.txt", "a")
    f.write(log_text)
    f.close()

# checks torrent name (from qbittorrent) for attributes
def torrentNameCheck_Movie(torrent_name):
    if torrent_name.__contains__("x264") | torrent_name.__contains__("1080p") | torrent_name.__contains__("720p") | torrent_name.__contains__("XVID"):
        return True
def torrentNameCheck_Music(torrent_name):
    if torrent_name.__contains__("FLAC") | torrent_name.__contains__("320") | torrent_name.__contains__("v0") | torrent_name.__contains__("v2") | torrent_name.__contains__("WAV"):
        return True

#checks torrent file extension (from path)
def fileTypeCheck_Movie(torrent_root_path):
    if str(torrent_root_path).__contains__(".mkv") | str(torrent_root_path).__contains__(".avi") | str(torrent_root_path).__contains__(".mp4") | str(torrent_root_path).__contains__(".wmv") and not str(torrent_root_path).__contains__("sample") | str(torrent_root_path).__contains__("Sample") | str(torrent_root_path).__contains__("SAMPLE"):
        return True
def fileTypeCheck_TV(torrent_root_path):
    if str(torrent_root_path).__contains__(".mkv") | str(torrent_root_path).__contains__(".avi") | str(torrent_root_path).__contains__(".mp4") | str(torrent_root_path).__contains__(".wmv"):
        return True

# checks torrent file extension (from path derived filename)
def fileTypeCheck_Music(torrent_file):
    if str(torrent_file).__contains__(".mp3") | str(torrent_file).__contains__(".flac") | str(torrent_file).__contains__(".FLAC") | str(torrent_file).__contains__(".wav") | str(torrent_file).__contains__(".WAV"):
        return True

# thanks to renanbs on GitHub: https://github.com/renanbs/extractor/blob/master/LICENSE
def multiRarUnzip(torrent_name, torrent_root_path):
    # print(glob.glob(torrent_root_path + "\\**.rar"))
    logToFile(str(datetime.now()) + " [multiRarUnzip] - multiRAR detected, unzipping to destination: " + MOVIE_TV_DESTINATION + "\n")
    path_list = glob.glob(torrent_root_path + "\\**.rar")
    for path in path_list:
        path_in_str = str(path)
        out = subprocess.run(["unrar", "e", path_in_str, MOVIE_TV_DESTINATION], stdout=subprocess.DEVNULL)
        if not out.returncode:
            logToFile(str(datetime.now()) + " " + torrent_name + " - [ OK ] \n")
        else:
            logToFile(str(datetime.now()) + " " + torrent_name + " - [ ERROR ]  \n")

def copySomething(root_folder, file_to_copy, path_to_copy_to):
    logToFile(str(datetime.now()) + " [copySomething] - copying file: " + file_to_copy + " to destination: " + path_to_copy_to + "\n")
    copy(str(root_folder + "\\" + file_to_copy), path_to_copy_to)
    logToFile(str(datetime.now()) + " [copySomething] - COPY COMPLETE \n")

def musicSort(torrent_name, torrent_root_path):
    confirm_number = 0
    confirmation = False

    for (root,dirs,files) in os.walk(torrent_root_path):
        for file in files:
            # copies all mkv files in torrent folder
            if fileTypeCheck_Music(file):
                # copy the whole folder, not just individual files in folder
                print(file)
                confirm_number += 1
                no_association = False

                # if more than 65% of files in folder are music, this is most likely an album
                if confirm_number / len(files) > 0.65:
                    confirmation = True

    # files inside torrent are verified to be music files
    if confirmation == True:
        shutil.copytree(torrent_root_path, MUSIC_DESTINATION + "/" + torrent_name)

# TODO handle torrents that just leave a file in the downloads folder

    # check to see if the above logic didnt capture a file
    if no_association == True:
        logToFile("[musicSort] - NO ASSOCIATIONS FOR -MUSIC- TORRENT - " + torrent_name + " \n")

def tvSort(torrent_name, torrent_root_path):
    for (root,dirs,files) in os.walk(torrent_root_path):
        for file in files:
            # copies all mkv files in torrent folder
            if fileTypeCheck_TV(file):
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
    no_association = True

    for (root,dirs,files) in os.walk(torrent_root_path):
        for file in files:
            # copies all mkv files in torrent folder except small SAMPLE clips
            if fileTypeCheck_Movie(file):
                generatedMoviePath = PathGen.moviePathGen(file)
                copySomething(root, file, generatedMoviePath)
                no_association = False

            # rar file discovered, begin unzipping
            elif str(file).__contains__(".rar"):
                multiRarUnzip(torrent_name, torrent_root_path)
                no_association = False

    # check to see if the above logic didnt capture a file
    if no_association == True:
        logToFile("[movieSort] - NO ASSOCIATIONS FOR -MOVIE- TORRENT - " + torrent_name + " \n")

def main():

    # TODO make games copy/unzip to z drive
    # TODO check for existing files during copy
    # TODO put mp3 check before torrent name check for music only
    # TODO upgrade music percentage checker to drill recursively through folders

    print(str(sys.argv))
    torrent_name = sys.argv[1]
    torrent_root_path = sys.argv[2]
    logToFile(str(datetime.now()) + "---------------------------------------------------------------\n")
    logToFile(str(datetime.now()) + " [main] - NEW TORRENT: " + torrent_name + "\n")

    # check if TV show single
    S_E_regex = re.compile('S[0-9][0-9]E[0-9][0-9]')
    S_E_match = re.search(S_E_regex, torrent_name)

    # TV show entire season/show
    S_regex = re.compile('S[0-9][0-9]')
    S_match =re.search(S_regex, torrent_name)

    # if tv show do stuff
    if S_E_match:
        logToFile(str(datetime.now()) + " [main] - TV detected \n")
        if fileTypeCheck_TV(torrent_root_path):
            logToFile(str(datetime.now()) + " [main] - single file detected...copying to drive: " + MOVIE_TV_DESTINATION + "\n")
            # extract torrent name + file extension from full path
            fileName = str(torrent_root_path.rsplit("\\", 1)[1])
            # we know the file isn't in a folder and resides in the main torrent directory, use global
            copySomething(TORRENT_FOLDER, fileName, MOVIE_TV_DESTINATION)
        else:
            tvSort(torrent_name, torrent_root_path)

    # not tv show, must be movie
    elif torrentNameCheck_Movie(torrent_name):
        logToFile(str(datetime.now()) + " [main] - MOVIE detected \n")
        if fileTypeCheck_Movie(torrent_root_path):
            fileName = str(torrent_root_path.rsplit("\\", 1)[1])
            generatedMoviePath = PathGen.moviePathGen(fileName)
            logToFile(str(datetime.now()) + " [main] - single file detected... copying to path: " + generatedMoviePath + "\n")
            copySomething(TORRENT_FOLDER, fileName, generatedMoviePath)
        else:
            movieSort(torrent_name, torrent_root_path)

    # might be music too
    elif torrentNameCheck_Music(torrent_name):
        logToFile(str(datetime.now()) + " [main] - MUSIC detected \n")
        musicSort(torrent_name, torrent_root_path)

    else:
        logToFile("***NO ASSOCIATIONS FOR TORRENT - " + torrent_name + "***\n")

main()