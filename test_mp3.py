import mp3

SAMPLE_FOLDER = '/Users/zaydrianprice/desktop/sample-mp3s/'
FILE_PATH_1 = SAMPLE_FOLDER + '01 Fergalicious (Feat. Will.I.Am).mp3'
FILE_PATH_2 = SAMPLE_FOLDER + '01 Forever (Main Version) 1.mp3'

music = []
music.append(mp3.Mp3(FILE_PATH_1))
music.append(mp3.Mp3(FILE_PATH_2))

print(music[0].title)
print(music[1].title)

music[0].set_genre('')
print(music[0].genre)


