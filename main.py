import os
import re
import sys
import shutil
import os.path
from datetime import datetime

import TelegramInterface
import settings
import OsUtils as OSU
import RegexOps as RegOps
import PathGenerator as PathGen
import FileIdentifiers as FileID
import FileTypeChecks as FileCheck

# logging date format for text
# datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def logToFile(log_text):
    f = open(settings.LOG_DESTINATION + "\\log.txt", "a")
    f.write(log_text)
    f.close()

def tvSort(torrent_name, torrent_root_path):
    no_association = True
    for (root, dirs, files) in os.walk(torrent_root_path):
        for file in files:
            # copies all mkv files in torrent folder
            if FileCheck.fileTypeCheck_TV(file):
                OSU.copySomething(root, file, settings.MOVIE_TV_DESTINATION + "\\" + file)
                logToFile(file + "***\n")
                no_association = False

            # rar file discovered, begin unzipping
            elif str(file).__contains__(".rar"):
                OSU.multiRarUnzip(torrent_name, torrent_root_path, settings.MOVIE_TV_DESTINATION)
                no_association = False

    # check to see if the above logic didnt capture a file
    if no_association:
        TelegramInterface.logToTelegram("[tvSort] - NO ASSOCIATIONS FOR -TV- TORRENT - " + torrent_name + " \n")

def movieSort(torrent_name, torrent_root_path):
    no_association = True
    for (root, dirs, files) in os.walk(torrent_root_path):
        for file in files:
            # copies all mkv files in torrent folder except small SAMPLE clips
            generatedMoviePath = PathGen.moviePathGen(file)

            if FileCheck.fileTypeCheck_Movie(file):
                TelegramInterface.logToTelegram("[movieSort] - generated movie path is: " + generatedMoviePath + "\n")
                OSU.copySomething(root, file, generatedMoviePath + "\\" + file)
                no_association = False

            # rar file discovered, begin unzipping
            elif str(file).__contains__(".rar"):
                TelegramInterface.logToTelegram( "[movieSort] - generated movie path is: " + generatedMoviePath + "\n")
                OSU.multiRarUnzip(torrent_name, torrent_root_path, settings.MOVIE_TV_DESTINATION)
                for (rootMOV, dirsMOV, filesMOV) in os.walk(settings.MOVIE_TV_DESTINATION + "\\"):
                    for fileMOV in filesMOV:
                        if FileCheck.fileTypeCheck_Movie(fileMOV):
                            print(settings.MOVIE_TV_DESTINATION + "\\" + fileMOV)
                            OSU.moveSomething(settings.MOVIE_TV_DESTINATION, fileMOV, generatedMoviePath + "\\" + fileMOV)
                no_association = False

    # check to see if the above logic didnt capture a file
    if no_association:
        TelegramInterface.logToTelegram("[movieSort] - NO ASSOCIATIONS FOR -MOVIE- TORRENT - " + torrent_name + " \n")

# music has been verified by this point, just perform the copy
def musicSort(torrent_name, torrent_root_path):
    path_to_copy_to = settings.MUSIC_DESTINATION + "/" + torrent_name
    if not os.path.exists(path_to_copy_to):
        TelegramInterface.logToTelegram("[musicSort] - copying file: " + torrent_name + " to destination: " + settings.MUSIC_DESTINATION + "\n")
        shutil.copytree(torrent_root_path, path_to_copy_to)
        TelegramInterface.logToTelegram("[musicSort] - COPY COMPLETE \n")
    else:
        TelegramInterface.logToTelegram("[musicSort] - FILE ALREADY EXISTS \n")

# game has been verified by this point
def gameSort(torrent_name, torrent_root_path):
    path_to_copy_to = settings.GAME_DESTINATION + torrent_name
    if not os.path.exists(path_to_copy_to):
        TelegramInterface.logToTelegram("[gameSort] - copying file: " + torrent_name + " to destination: " + path_to_copy_to + "\n")
        shutil.copytree(torrent_root_path, path_to_copy_to)
        TelegramInterface.logToTelegram("[gameSort] - COPY COMPLETE \n")
    else:
        TelegramInterface.logToTelegram("[gameSort] - FILE ALREADY EXISTS \n")

    if FileCheck.fileTypeCheck_Game_Zipped(path_to_copy_to + "\\"):
        TelegramInterface.logToTelegram("[gameSort] - unzipping from " + path_to_copy_to + " to " + path_to_copy_to + " - unzipped\n")
        OSU.multiRarUnzip(torrent_name, path_to_copy_to, path_to_copy_to + " - unzipped\\")

        for (root, dirs, files) in os.walk(path_to_copy_to + "\\"):
            for file in files:
                if str(file).__contains__(".nfo"):
                    OSU.copySomething(root, file, path_to_copy_to + " - unzipped\\" + file)

def main():
    print(str(sys.argv))
    torrent_name = sys.argv[1]
    torrent_root_path = sys.argv[2]
    TelegramInterface.logToTelegram("-------------------------------------------------------------------------------\n")
    TelegramInterface.logToTelegram("[main] - NEW TORRENT: " + torrent_name + "\n")

    S_E_match = RegOps.S_E_REGEX(torrent_name)
    S_E_name = RegOps.S_E_REGEX_NAME(torrent_name)
    # S_match = S_REGEX(torrent_name)

    # if tv show do stuff
    if S_E_match:
        tv_code = str(S_E_name[0])
        TelegramInterface.logToTelegram("[main] - TV detected \n")
        if FileCheck.fileTypeCheck_TV(torrent_root_path):
            TelegramInterface.logToTelegram("[main] - single file detected...copying to drive: " + settings.MOVIE_TV_DESTINATION + "\n")
            # extract torrent name + file extension from full path
            fileName = str(torrent_root_path.rsplit("\\", 1)[1])
            # we know the file isn't in a folder and resides in the main torrent directory, use global
            OSU.copySomething(settings.TORRENT_FOLDER, fileName, settings.MOVIE_TV_DESTINATION)
        else:
            tvSort(torrent_name, torrent_root_path)

        # looks through MOVIE_TV_DESTINATION for the file and copies it to the correct folder in plex library
        PLEX_DESTINATION = FileID.tvIdentifier(torrent_name, tv_code)
        fileName = str(torrent_root_path.rsplit("\\", 1)[1])

        for (root, dirs, files) in os.walk(settings.MOVIE_TV_DESTINATION):
            for file in files:
                if re.search(fileName, file, re.IGNORECASE):
                    OSU.moveSomething(settings.MOVIE_TV_DESTINATION, file, PLEX_DESTINATION + "\\" + file)

        TelegramInterface.notifyPlexUsers(torrent_name, "tv show")

    # not tv show, must be movie
    elif FileCheck.torrentNameCheck_Movie(torrent_name):
        TelegramInterface.logToTelegram("[main] - MOVIE detected \n")
        if FileCheck.fileTypeCheck_Movie(torrent_root_path):
            fileName = str(torrent_root_path.rsplit("\\", 1)[1])
            generatedMoviePath = PathGen.moviePathGen(fileName)
            TelegramInterface.logToTelegram("[main] - single file detected... copying to path: " + generatedMoviePath + "\n")
            OSU.copySomething(settings.TORRENT_FOLDER, fileName, generatedMoviePath + "\\" + fileName)
        else:
            movieSort(torrent_name, torrent_root_path)

        TelegramInterface.notifyPlexUsers(torrent_name, "movie")

    # might be music too, must check torrent name and have more than 65% music files inside
    elif FileID.musicIdentifier(torrent_root_path) or FileCheck.torrentNameCheck_Music(torrent_name):
        TelegramInterface.logToTelegram("[main] - MUSIC detected \n")
        musicSort(torrent_name, torrent_root_path)


    elif FileID.gameIdentifier(torrent_root_path):
        gameSort(torrent_name, torrent_root_path)


    else:
        TelegramInterface.logToTelegram("[main] - ***NO ASSOCIATIONS FOR TORRENT - " + torrent_name + "***\n")


main()
