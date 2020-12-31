import os
import glob
import shutil
import subprocess
from shutil import copy
from shutil import disk_usage
import TelegramInterface
import settings

MAXIMUM_ALLOWED_DISK_USAGE = 0.98

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
    print(path_to_copy_to.split("\\")[0])
    disk_usage = findPercentageDiskUsed(path_to_copy_to.split("\\")[0])

    if disk_usage < MAXIMUM_ALLOWED_DISK_USAGE:
        TelegramInterface.logToTelegram("[copySomething] - copying file: " + file_to_copy + " to destination: " + path_to_copy_to + "\n")
        if not os.path.exists(path_to_copy_to):
            copy(str(root_folder + "\\" + file_to_copy), path_to_copy_to)
            TelegramInterface.logToTelegram("[copySomething] - COPY COMPLETE: \n'" + file_to_copy + "'")
        else:
            TelegramInterface.logToTelegram("[copySomething] - FILE ALREADY EXISTS: \n'" + file_to_copy + "'")
    else:
        TelegramInterface.logToTelegram("[copySomething] - DISK IS FULL - ABORTING: \n'" + path_to_copy_to + "'")

def moveSomething(root_folder, file_to_copy, path_to_move_to):
    print(path_to_move_to.split("\\")[0])
    disk_usage = findPercentageDiskUsed(path_to_move_to.split("\\")[0])

    if disk_usage < 0.98:
        TelegramInterface.logToTelegram("[moveSomething] - moving file: " + file_to_copy + " to destination: " + path_to_move_to + "\n")
        if not os.path.exists(path_to_move_to):
            shutil.move(str(root_folder + "\\" + file_to_copy), path_to_move_to)
            TelegramInterface.logToTelegram("[moveSomething] - MOVE COMPLETE: \n'" + file_to_copy + "'")
        else:
            TelegramInterface.logToTelegram("[moveSomething] - FILE ALREADY EXISTS: \n'" + file_to_copy + "'")
    else:
        TelegramInterface.logToTelegram("[copySomething] - DISK IS FULL - ABORTING: \n'" + path_to_move_to + "'")

#finds the percent usage of a particular disk/directory
def findPercentageDiskUsed(path_to_copy_to):
    disk_usage_tuple = disk_usage(path_to_copy_to)
    usage_percentage = disk_usage_tuple[1] / disk_usage_tuple[0]
    TelegramInterface.logToTelegram("[findPercentageDiskUsed] - drive " + path_to_copy_to + " is " + str(round(usage_percentage,2)*100) + "% full")
    print(str(usage_percentage*100) + "%")
    return usage_percentage