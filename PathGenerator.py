
### PATHS AND PATTERNS ###
MOVIE_PATH_A_F = "G:\\Movies\\a-f"
MOVIE_PATH_G_L = "G:\\Movies\\g-l"
MOVIE_PATH_M_R = "G:\\Movies\\m-r"
MOVIE_PATH_S_X = "G:\\Movies\\s-x"
MOVIE_PATH_Y_Z = "G:\\Movies\\y-z"

LETTERS_A_F = ["a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
LETTERS_G_L = ["g", "h", "i", "j", "k", "l", "G", "H", "I", "J", "K", "L"]
LETTERS_M_R = ["m", "n", "o", "p", "q", "r", "M", "N", "O", "P", "Q", "R"]
LETTERS_S_X = ["s", "t", "u", "v", "w", "x", "S", "T", "U", "V", "W", "X"]
LETTERS_Y_Z = ["y", "z", "Y", "Z"]
### PATHS AND PATTERNS ###

def moviePathGen(torrent_name):
    torrent_first_letter = str(torrent_name[0])

    for letter in LETTERS_A_F:
        if str(torrent_first_letter) == letter:
            return MOVIE_PATH_A_F

    for letter in LETTERS_G_L:
        if str(torrent_first_letter) == letter:
            return MOVIE_PATH_G_L

    for letter in LETTERS_M_R:
        if str(torrent_first_letter) == letter:
            return MOVIE_PATH_M_R

    for letter in LETTERS_S_X:
        if str(torrent_first_letter) == letter:
            return MOVIE_PATH_S_X

    for letter in LETTERS_Y_Z:
        if str(torrent_first_letter) == letter:
            return MOVIE_PATH_Y_Z

    return MOVIE_PATH_A_F + "\\"
