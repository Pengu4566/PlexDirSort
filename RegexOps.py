import re

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
    return S_match

def E_REGEX(torrent_name):
    # TV show episode
    E_regex = re.compile('E[0-9][0-9]')
    E_match = re.search(E_regex, torrent_name)
    return E_match