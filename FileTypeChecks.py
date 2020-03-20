import os

# checks torrent name (from qbittorrent) for attributes
def torrentNameCheck_Movie(torrent_name):
    if torrent_name.__contains__("x264") | torrent_name.__contains__("1080p") | torrent_name.__contains__("720p") | torrent_name.__contains__("XVID") | torrent_name.__contains__("hevc") | torrent_name.__contains__("HEVC"):
        return True

def torrentNameCheck_Music(torrent_name):
    if torrent_name.__contains__("FLAC") | torrent_name.__contains__("320") | torrent_name.__contains__("v0") | torrent_name.__contains__("v2") | torrent_name.__contains__("WAV") | torrent_name.__contains__("WEB"):
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
    if str(torrent_file).__contains__(".mp3") | str(torrent_file).__contains__(".flac") | str(torrent_file).__contains__(".FLAC") | str(torrent_file).__contains__(".wav") | str(torrent_file).__contains__(".WAV") | str(torrent_file).__contains__(".m4b") | str(torrent_file).__contains__(".log") | str(torrent_file).__contains__(".cue"):
        return True

def fileTypeCheck_Game(torrent_root_path):
    if str(torrent_root_path).__contains__(".iso") | str(torrent_root_path).__contains__(".rar") | str(torrent_root_path).__contains__(".img") | str(torrent_root_path).__contains__("CRACK") | str(torrent_root_path).__contains__("crack"):
        return True

def fileTypeCheck_Game_Zipped(torrent_root_path):
    for (root, dirs, files) in os.walk(torrent_root_path):
        for file in files:
            if str(file).__contains__(".rar"):
                return True
