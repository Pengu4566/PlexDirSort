#first commit, nothing here!

import sys
import os
import qbittorrentapi
from shutil import copy

#uses QBitTorrent api to control the current torrent
def qbitLogin():
    print(1)
    #https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-Documentation#get-torrent-list





def movieUnzip():
    print(1)

def movieSort(torrent_name, torrent_root_path, copy_destination):
    print(torrent_root_path)
    #os.mkdir(str(torrent_root_path + "/hacked bitchhh"))
    no_association = True

    for (root,dirs,files) in os.walk(torrent_root_path):
        for file in files:
            #copies all mkv files in torrent folder except small SAMPLE clips
            if str(file).__contains__(".mkv") and not str(file).__contains__("sample"):
                copy(str(root + "/" + file), copy_destination)
                print("[movieSort - copying file: " + file + " to destination " + copy_destination)
                no_association = False

    #check to see if the above logic didnt capture a file
    if no_association == True:
        print("***NO ASSOCIATIONS FOR TORRENT - " + torrent_name + "***")

    #print(files)
    #print(dirs)


def main():

    #SETTINGS
    copy_destination = "C:/Users/mihal/Desktop"

    print(str(sys.argv))

    #TODO make log file that lives in dropbox or something
    #TODO differentiate between torrents that download into folders and ones that just leave a file in the donwloads folder


    torrent_name = sys.argv[1]
    torrent_root_path = sys.argv[2]\
        #.replace("\\", "/")
    #os.mkdir(str("C:/Users/mihal/Desktop/" + sys.argv[1]))

    movieSort(torrent_name, torrent_root_path, copy_destination)


main()