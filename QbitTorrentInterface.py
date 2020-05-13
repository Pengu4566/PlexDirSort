import qbittorrentapi
import secrets
import TelegramInterface

WEBSERVER_IP = secrets.WEBSERVER_IP
WEBSERVER_PORT = secrets.WEBSERVER_PORT
WEBSERVER_USERNAME = secrets.WEBSERVER_USERNAME
WEBSERVER_PASSWORD = secrets.WEBSERVER_PASSWORD

IPT_TRACKER_ASYNC = secrets.IPT_TRACKER_ASYNC
IPT_TRACKER_STACK = secrets.IPT_TRACKER_STACK
IPT_TRACKER_BGP = secrets.IPT_TRACKER_BGP
IPT_TRACKER_IPT = secrets.IPT_TRACKER_IPT
MYANON_TRACKER = secrets.MYANON_TRACKER
ORPHEUS_TRACKER = secrets.ORPHEUS_TRACKER
REDACTED_TRACKER = secrets.REDACTED_TRACKER
TORRENTECH_TRACKER = secrets.TORRENTECH_TRACKER
THEPOLISH_TRACKER = secrets.THEPOLISH_TRACKER
AWESOME_HD_TRACKER = secrets.AWESOME_HD_TRACKER

# uses QBitTorrent api to control the current torrent tags
def qbitCategorizer(torrent_name, torrent_tracker, torrent_hash):

    # login
    qbt_client = qbittorrentapi.Client(host=WEBSERVER_IP + ":" + WEBSERVER_PORT, username=WEBSERVER_USERNAME, password=WEBSERVER_PASSWORD, VERIFY_WEBUI_CERTIFICATE=False)
    try:
        qbt_client.auth_log_in()
        # TelegramInterface.logToTelegram("[QbitTorrentInterface] - Qbit login SUCCESS \n")
    except qbittorrentapi.LoginFailed as e:
        TelegramInterface.logToTelegram("[QbitTorrentInterface] - Qbit login FAILED \n")
        print(e)

    # get torrent via hash
    torrent_list = qbt_client.torrents_info(hashes=torrent_hash)

    for torrent in torrent_list:
        print(torrent.name)

    torrent = torrent_list[0]

    # enumerate category and set it
    if torrent_tracker.__contains__(IPT_TRACKER_ASYNC) or torrent_tracker.__contains__(IPT_TRACKER_STACK) or torrent_tracker.__contains__(IPT_TRACKER_BGP) or torrent_tracker.__contains__(IPT_TRACKER_IPT):
        torrent.set_category(category='IPTorrents')
        TelegramInterface.logToTelegram("[QbitTorrentInterface] - categorized to: IPTorrents \n")
    elif torrent_tracker.__contains__(MYANON_TRACKER):
        torrent.set_category(category='MyAnonaMouse')
        TelegramInterface.logToTelegram("[QbitTorrentInterface] - categorized to: MyAnonaMouse \n")
    elif torrent_tracker.__contains__(ORPHEUS_TRACKER):
        torrent.set_category(category='Orpheus')
        TelegramInterface.logToTelegram("[QbitTorrentInterface] - categorized to: Orpheus \n")
    elif torrent_tracker.__contains__(REDACTED_TRACKER):
        torrent.set_category(category='REDacted')
        TelegramInterface.logToTelegram("[QbitTorrentInterface] - categorized to: REDacted \n")
    elif torrent_tracker.__contains__(TORRENTECH_TRACKER):
        torrent.set_category(category='TorrenTech')
        TelegramInterface.logToTelegram("[QbitTorrentInterface] - categorized to: TorrenTech \n")
    elif torrent_tracker.__contains__(THEPOLISH_TRACKER):
        torrent.set_category(category='ThePolishTracker')
        TelegramInterface.logToTelegram("[QbitTorrentInterface] - categorized to: ThePolishTracker \n")
    elif torrent_tracker.__contains__(AWESOME_HD_TRACKER):
        torrent.set_category(category='Awesome-HD')
        TelegramInterface.logToTelegram("[QbitTorrentInterface] - categorized to: Awesome-HD \n")
    else:
        TelegramInterface.logToTelegram("[QbitTorrentInterface] - could not determine categry! \n")



