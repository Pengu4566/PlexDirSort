import os
import re
import sys
import glob
import shutil
import os.path
import subprocess
import qbittorrentapi
from shutil import copy
from datetime import datetime

import PathGenerator as PathGen

### SETTINGS ###
PLEX_LIBRARY = "G:\\TV Shows"
GAME_DESTINATION = "Z:\\"
MOVIE_TV_DESTINATION = "Z:\\"
MUSIC_DESTINATION = "C:\\Users\\mihal\\Desktop"
LOG_DESTINATION = "C:\\Users\\mihal\\Desktop"
TORRENT_FOLDER = "H:\\Torrent\\Downloaded Torrents"
MUSIC_CONFIDENCE_REQUIRED_SCORE = 0.65
SEARCH_DEPTH = 2
### SETTINGS ###

# https://github.com/python-telegram-bot/python-telegram-bot
def telegramNotifier():
    print(1)
    #TODO


# uses QBitTorrent api to control the current torrent tags
def qbitLogin():
    print(1)
    # https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-Documentation#get-torrent-list
    # TODO

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

# checks torrent file extension (from path)
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

def fileTypeCheck_Game(torrent_root_path):
    if str(torrent_root_path).__contains__(".iso") | str(torrent_root_path).__contains__(".rar") | str(torrent_root_path).__contains__(".img") | str(torrent_root_path).__contains__("CRACK") | str(torrent_root_path).__contains__("crack"):
        return True

def fileTypeCheck_Game_Zipped(torrent_root_path):
    for (root, dirs, files) in os.walk(PLEX_LIBRARY):
        for file in files:
            if str(file).__contains__(".rar"):
                return True

def musicIdentifier(torrent_root_path):
    confirm_number = 0
    for (root,dirs,files) in os.walk(torrent_root_path):
        for file in files:
            if fileTypeCheck_Music(file):
                confirm_number += 1
                if confirm_number / len(files) > MUSIC_CONFIDENCE_REQUIRED_SCORE:
                    return True

def gameIdentifier(torrent_root_path):
    # confirm_number(0, not a game | 1, game, normal | 2, game, zipped)
    confirm_number = 0
    for (root, dirs, files) in os.walk(torrent_root_path):
        for file in files:
            if fileTypeCheck_Game(file):
                confirm_number = 1
                if fileTypeCheck_Game_Zipped(file):
                    return 2

    return confirm_number

# obtain TV name without ".", all text before SXXEXX identifier
def tvNameSplitter(torrent_name_split):
    tv_name = ''
    for word in torrent_name_split:
        S_E_MATCH = S_E_REGEX(word)

        if S_E_MATCH:
            return tv_name.rstrip()

        tv_name += word + ' '

def tvIdentifier(torrent_name, tv_code):
    torrent_name_split = torrent_name.split(".")
    tv_name = tvNameSplitter(torrent_name_split)
    # print('---' + tv_name + '---')
    # searches plex library for shows matching that name
    for (root, dirs, files) in os.walk(PLEX_LIBRARY):
        if root[len(PLEX_LIBRARY):].count(os.sep) < SEARCH_DEPTH:
            for dir in dirs:
                if dir.__contains__(tv_name) or dir == tv_name:
                    tv_dir = root + '\\' + dir
                    tv_season_num = int(tv_code[1] + tv_code[2])
                    tv_episode_num = int(tv_code[4] + tv_code[5])
                    logToFile(str(datetime.now()) + " [tvIdentifier] TV folder found: " + tv_dir + "\n")
                    # search for correct season
                    for (root, dirs, files) in os.walk(tv_dir):
                        for dir in dirs:
                            if dir.__contains__(str(tv_season_num)):
                                final_folder_path = tv_dir + "\\" + dir + "\\"
                                logToFile(str(datetime.now()) + " [tvIdentifier] season folder found: " + dir + "\n")
                                logToFile(str(datetime.now()) + " [tvIdentifier] final path is: " + final_folder_path + "\n")
                                return final_folder_path

                    # if we get here we have not found the tv show
    logToFile(str(datetime.now()) + " [tvIdentifier] - unable to find PLEX folder for: " + torrent_name + "\n")
    #

# thanks to renanbs on GitHub: https://github.com/renanbs/extractor/blob/master/LICENSE
def multiRarUnzip(torrent_name, torrent_root_path, destination):
    # print(glob.glob(torrent_root_path + "\\**.rar"))
    logToFile(str(datetime.now()) + " [multiRarUnzip] - multiRAR detected, unzipping to destination: " + destination + "\n")
    path_list = glob.glob(torrent_root_path + "\\**.rar")
    for path in path_list:
        path_in_str = str(path)
        out = subprocess.run(["unrar", "e", path_in_str, destination], stdout=subprocess.DEVNULL)
        if not out.returncode:
            logToFile(str(datetime.now()) + " [multiRarUnzip] - " + torrent_name + " - [ OK ] \n")
        else:
            logToFile(str(datetime.now()) + " [multiRarUnzip] - " + torrent_name + " - [ ERROR ]  \n")

def copySomething(root_folder, file_to_copy, path_to_copy_to):
    logToFile(str(datetime.now()) + " [copySomething] - copying file: " + file_to_copy + " to destination: " + path_to_copy_to + "\n")
    if not os.path.exists(path_to_copy_to):
        copy(str(root_folder + "\\" + file_to_copy), path_to_copy_to)
        logToFile(str(datetime.now()) + " [copySomething] - COPY COMPLETE \n")
    else:
        logToFile(str(datetime.now()) + " [copySomething] - FILE ALREADY EXISTS \n")

def moveSomething(root_folder, file_to_copy, path_to_move_to):
    logToFile(str(datetime.now()) + " [moveSomething] - moving file: " + file_to_copy + " to destination: " + path_to_move_to + "\n")
    if not os.path.exists(path_to_move_to):
        shutil.move(str(root_folder + "\\" + file_to_copy), path_to_move_to)
        logToFile(str(datetime.now()) + " [moveSomething] - MOVE COMPLETE \n")
    else:
        logToFile(str(datetime.now()) + " [moveSomething] - FILE ALREADY EXISTS \n")

def tvSort(torrent_name, torrent_root_path):
    no_association = True
    for (root, dirs, files) in os.walk(torrent_root_path):
        for file in files:
            # copies all mkv files in torrent folder
            if fileTypeCheck_TV(file):
                copySomething(root, file, MOVIE_TV_DESTINATION + "\\" + file)
                logToFile(file + "***\n")
                no_association = False

            # rar file discovered, begin unzipping
            elif str(file).__contains__(".rar"):
                multiRarUnzip(torrent_name, torrent_root_path, MOVIE_TV_DESTINATION)
                no_association = False

    # check to see if the above logic didnt capture a file
    if no_association:
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
                multiRarUnzip(torrent_name, torrent_root_path, MOVIE_TV_DESTINATION)
                no_association = False

    # check to see if the above logic didnt capture a file
    if no_association == True:
        logToFile("[movieSort] - NO ASSOCIATIONS FOR -MOVIE- TORRENT - " + torrent_name + " \n")

# music has been verified by this point, just perform the copy
def musicSort(torrent_name, torrent_root_path):
    path_to_copy_to = MUSIC_DESTINATION + "/" + torrent_name
    if not os.path.exists(path_to_copy_to):
        logToFile(str(datetime.now()) + " [musicSort] - copying file: " + torrent_name + " to destination: " + MUSIC_DESTINATION + "\n")
        shutil.copytree(torrent_root_path, path_to_copy_to)
        logToFile(str(datetime.now()) + " [musicSort] - COPY COMPLETE \n")
    else:
        logToFile(str(datetime.now()) + " [musicSort] - FILE ALREADY EXISTS \n")

# game has been verified by this point
def gameSort(torrent_name, torrent_root_path):
    path_to_copy_to = GAME_DESTINATION + torrent_name
    if not os.path.exists(path_to_copy_to):
        logToFile(str(datetime.now()) + " [gameSort] - copying file: " + torrent_name + " to destination: " + path_to_copy_to + "\n")
        shutil.copytree(torrent_root_path, path_to_copy_to)
        logToFile(str(datetime.now()) + " [gameSort] - COPY COMPLETE \n")
    else:
        logToFile(str(datetime.now()) + " [gameSort] - FILE ALREADY EXISTS \n")

    if fileTypeCheck_Game_Zipped(path_to_copy_to + "\\"):
        logToFile(str(datetime.now()) + " [gameSort] - unzipping from " + path_to_copy_to + " to " + path_to_copy_to + " - unzipped\n")
        multiRarUnzip(torrent_name, path_to_copy_to, path_to_copy_to + " - unzipped\\")

        for (root, dirs, files) in os.walk(path_to_copy_to + "\\"):
            for file in files:
                if str(file).__contains__(".nfo"):
                    copySomething(root, file, path_to_copy_to + " - unzipped\\" + file)

def S_E_REGEX_NAME(torrent_name):
    S_E_regex = re.compile('S[0-9][0-9]E[0-9][0-9]')
    S_E_match_name = re.findall(S_E_regex, torrent_name)
    return S_E_match_name

def S_E_REGEX(torrent_name):
    # check if TV show single
    S_E_regex = re.compile('S[0-9][0-9]E[0-9][0-9]')
    S_E_match = re.search(S_E_regex, torrent_name)
    return S_E_match

def S_REGEX(torrent_name):
    # TV show entire season/show
    S_regex = re.compile('S[0-9][0-9]')
    S_match = re.search(S_regex, torrent_name)

def main():
    print(str(sys.argv))
    torrent_name = sys.argv[1]
    torrent_root_path = sys.argv[2]
    logToFile(str(datetime.now()) + "---------------------------------------------------------------\n")
    logToFile(str(datetime.now()) + " [main] - NEW TORRENT: " + torrent_name + "\n")

    S_E_match = S_E_REGEX(torrent_name)
    S_E_name = S_E_REGEX_NAME(torrent_name)
    S_match = S_REGEX(torrent_name)

    # if tv show do stuff
    if S_E_match:
        tv_code = str(S_E_name[0])
        logToFile(str(datetime.now()) + " [main] - TV detected \n")
        if fileTypeCheck_TV(torrent_root_path):
            logToFile(str(datetime.now()) + " [main] - single file detected...copying to drive: " + MOVIE_TV_DESTINATION + "\n")
            # extract torrent name + file extension from full path
            fileName = str(torrent_root_path.rsplit("\\", 1)[1])
            # we know the file isn't in a folder and resides in the main torrent directory, use global
            copySomething(TORRENT_FOLDER, fileName, MOVIE_TV_DESTINATION)
        else:
            tvSort(torrent_name, torrent_root_path)

        # looks through MOVIE_TV_DESTINATION for the file and copies it to the correct folder in plex library
        PLEX_DESTINATION = tvIdentifier(torrent_name, tv_code)
        fileName = str(torrent_root_path.rsplit("\\", 1)[1])

        for (root, dirs, files) in os.walk(MOVIE_TV_DESTINATION):
            for file in files:
                if re.search(fileName, file, re.IGNORECASE):
                    moveSomething(MOVIE_TV_DESTINATION, file, PLEX_DESTINATION + "\\" + file)

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

    # might be music too, must check torrent name and have more than 65% music files inside
    elif torrentNameCheck_Music(torrent_name) or musicIdentifier(torrent_root_path):
        logToFile(str(datetime.now()) + " [main] - MUSIC detected \n")
        musicSort(torrent_name, torrent_root_path)

    elif gameIdentifier(torrent_root_path):
        gameSort(torrent_name, torrent_root_path)

    else:
        logToFile("[main] - ***NO ASSOCIATIONS FOR TORRENT - " + torrent_name + "***\n")

main()
