import os
from datetime import datetime

import settings
import TelegramInterface
import RegexOps as RegOps
import FileTypeChecks as FileCheck

def logToFile(log_text):
    f = open(settings.LOG_DESTINATION + "\\log.txt", "a")
    f.write(log_text)
    f.close()

def musicIdentifier(torrent_root_path):
    confirm_number = 0
    for (root, dirs, files) in os.walk(torrent_root_path):
        for file in files:
            if FileCheck.fileTypeCheck_Music(file):
                confirm_number += 1
                if confirm_number / len(files) > settings.MUSIC_CONFIDENCE_REQUIRED_SCORE:
                    return True

def gameIdentifier(torrent_root_path):
    # confirm_number(0, not a game | 1, game, normal | 2, game, zipped)
    confirm_number = 0
    for (root, dirs, files) in os.walk(torrent_root_path):
        for file in files:
            if FileCheck.fileTypeCheck_Game(file):
                confirm_number = 1
                if FileCheck.fileTypeCheck_Game_Zipped(file):
                    return 2
    return confirm_number

def tvSeasonIdentifier(torrent_root_path):
    confirm_number = 0
    for (root, dirs, files) in os.walk(torrent_root_path):
        for file in files:
            if FileCheck.fileTypeCheck_Movie(file):
                confirm_number += 1
                print(confirm_number)
                if confirm_number > settings.TV_SEASON_NUM_FILES_REQUIRED:
                    return True

# obtain TV name without ".", all text before SXXEXX identifier
def tvNameSplitter(torrent_name_split):
    tv_name = ''
    for word in torrent_name_split:
        S_E_MATCH = RegOps.S_E_REGEX(word)

        if S_E_MATCH:
            return tv_name.rstrip()

        tv_name += word + ' '

def tvIdentifier(torrent_name, tv_code):
    torrent_name_split = torrent_name.split(".")
    tv_name = tvNameSplitter(torrent_name_split)
    # print('---' + tv_name + '---')
    # searches plex library for shows matching that name
    for (root, dirs, files) in os.walk(settings.PLEX_LIBRARY):
        if root[len(settings.PLEX_LIBRARY):].count(os.sep) < settings.SEARCH_DEPTH:
            for dir in dirs:
                if dir.__contains__(tv_name) or dir == tv_name:
                    tv_dir = root + '\\' + dir + "\\"
                    tv_season_num = int(tv_code[1] + tv_code[2])
                    # tv_episode_num = int(tv_code[4] + tv_code[5])
                    # TelegramInterface.logToTelegram("[tvIdentifier] TV folder found: " + tv_dir + "\n")
                    # search for correct season
                    print(tv_dir)
                    for (root2, dirs2, files2) in os.walk(tv_dir):
                        for dir2 in dirs2:
                            if dir2.__contains__(str(tv_season_num)):
                                final_folder_path = tv_dir + "\\" + dir2 + "\\"
                                # TelegramInterface.logToTelegram("[tvIdentifier] season folder found: " + dir2 + "\n")
                                TelegramInterface.logToTelegram("[tvIdentifier] final path is: " + final_folder_path + "\n")
                                return final_folder_path

                    # if we get here we have not found the tv show
    TelegramInterface.logToTelegram("[tvIdentifier] - unable to find PLEX folder for: " + torrent_name + "\n")
