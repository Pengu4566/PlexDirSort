import qbittorrentapi
import secrets

WEBSERVER_IP = '108.254.124.93'
WEBSERVER_PORT = '8080'
WEBSERVER_USERNAME = 'Pengu4566'
WEBSERVER_PASSWORD = secrets.WEBSERVER_PASSWORD

# uses QBitTorrent api to control the current torrent tags
def qbitLogin():
    print(1)
    # https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-Documentation#get-torrent-list
    # https://github.com/rmartin16/qbittorrent-api

    qbt_client = qbittorrentapi.Client(host=WEBSERVER_IP + ":" + WEBSERVER_PORT, username='admin', password='adminadmin')

    # TODO
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)