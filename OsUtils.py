import os
import glob
import shutil
import subprocess
from shutil import copy
import TelegramInterface
from datetime import datetime

import settings

def logToFile(log_text):
    f = open(settings.LOG_DESTINATION + "\\log.txt", "a")
    f.write(log_text)
    f.close()

# thanks to renanbs on GitHub: https://github.com/renanbs/extractor/blob/master/LICENSE
def multiRarUnzip(torrent_name, torrent_root_path, destination):
    # print(glob.glob(torrent_root_path + "\\**.rar"))
    TelegramInterface.logToTelegram("[multiRarUnzip] - multiRAR detected, unzipping to destination: " + destination + "\n")
    path_list = glob.glob(torrent_root_path + "\\**.rar")
    for path in path_list:
        path_in_str = str(path)
        out = subprocess.run(["unrar", "e", path_in_str, destination], stdout=subprocess.DEVNULL)
        if not out.returncode:
            TelegramInterface.logToTelegram("[multiRarUnzip] - " + torrent_name + " - [ OK ] \n")
        else:
            TelegramInterface.logToTelegram("[multiRarUnzip] - " + torrent_name + " - [ ERROR ]  \n")

def copySomething(root_folder, file_to_copy, path_to_copy_to):
    TelegramInterface.logToTelegram("[copySomething] - copying file: " + file_to_copy + " to destination: " + path_to_copy_to + "\n")
    if not os.path.exists(path_to_copy_to):
        copy(str(root_folder + "\\" + file_to_copy), path_to_copy_to)
        TelegramInterface.logToTelegram("[copySomething] - COPY COMPLETE \n")
    else:
        TelegramInterface.logToTelegram("[copySomething] - FILE ALREADY EXISTS \n")

def moveSomething(root_folder, file_to_copy, path_to_move_to):
    TelegramInterface.logToTelegram("[moveSomething] - moving file: " + file_to_copy + " to destination: " + path_to_move_to + "\n")
    if not os.path.exists(path_to_move_to):
        shutil.move(str(root_folder + "\\" + file_to_copy), path_to_move_to)
        TelegramInterface.logToTelegram("[moveSomething] - MOVE COMPLETE \n")
    else:
        TelegramInterface.logToTelegram("[moveSomething] - FILE ALREADY EXISTS \n")
