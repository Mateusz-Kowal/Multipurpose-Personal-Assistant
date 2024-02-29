#from __future__ import unicode_literals
from functions import *

class Song:         # klasa opisująca utwór muzyczny
    # konstruktor; tutaj wczytujemy wszystko co jest w pliku w folderze o ID piosenki, następnie przypisujemy do właściwych wartości
    def __init__(self, id):
        song_file = open(get_song_path(str(id)+"/info.txt"), "r", encoding="utf-8")
        self.link = song_file.readline().split("=", 1)[1].strip("\n")       # zawsze przypisuje wartość po znaku "="; ważne, żeby był argument 1 w splicie, który oznacza, że dzielimy zawsze tylko raz (znak "=" może być jeszcze później w linijce)
        self.ID = int(song_file.readline().split("=", 1)[1].strip("\n"))
        self.artist = song_file.readline().split("=", 1)[1].strip("\n")
        self.title = song_file.readline().split("=", 1)[1].strip("\n")
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.cover_artist = None if val=="None" else val
        self.name = song_file.readline().split("=", 1)[1].strip("\n")
        self.length_sec = int(song_file.readline().split("=", 1)[1].strip("\n"))
        self.length = song_file.readline().split("=", 1)[1].strip("\n")
        self.volume = int(song_file.readline().split("=", 1)[1].strip("\n"))
        self.tempo = song_file.readline().split("=", 1)[1].strip("\n")                  # !!! do ogarniecia, żeby interpretować słownik
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.origin = None if val=="None" else val
        self.genre = song_file.readline().split("=", 1)[1].strip("\n").split(", ")      # dodatkowy split, bo różne gatunki są rozdzielone przecinkiem (i spacją!)
        self.vibe = song_file.readline().split("=", 1)[1].strip("\n").split(", ")
        self.language = song_file.readline().split("=", 1)[1].strip("\n").split(", ")
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_cover = None if val=="None" else True if val=="True" else False     # rakowa linijka, ale nie chcę mi się budować drzewka, a no jednak trzeba to zcastować (boolean(x) testuje a nie castuje)
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_instrumental = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_lyrics = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_lyrics_translated = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_lyrics_romanized = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_lyrics_synchronized = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_lyrics_approved = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_lyrics_translated_approved = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_lyrics_romanized_approved = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_lyrics_synchronized_approved = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_meme = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_from_game = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_from_movie = None if val=="None" else True if val=="True" else False
        val = song_file.readline().split("=", 1)[1].strip("\n")
        self.is_cringe = None if val=="None" else True if val=="True" else False
        self.times_played = song_file.readline().split("=", 1)[1].strip("\n")
        self.times_listened = song_file.readline().split("=", 1)[1].strip("\n")
        self.events = song_file.readline().split("=", 1)[1].strip("\n")                 # !!! również do ogarnięcia, to będzie słownik
        self.dates_listened = song_file.readline().split("=", 1)[1].strip("\n").split(", ")
        song_file.close()
        self.full_name = self.name
        if self.origin is not None:
            self.full_name = self.full_name + " (from " + str(self.origin) + ")"
        if self.is_cover:
            self.full_name = self.full_name + " [cover by " + str(self.cover_artist) + "]"

    def __str__(self):                  # przeładowanie funkcji dla funkcji print() -> jeśli obiekt klasy będzie argumentem funkcji, która potrzebuje stringa, to zostanie przesłane to, co zwraca niniejsza funkcja
        return self.full_name
    
    def update_info(self):
        song_info_file = open(get_song_path(str(self.ID)+"/info.txt"), "w", encoding="utf-8")
        song_info_file.write("URL="+self.link+"\n")                               # link
        song_info_file.write("ID="+str(self.ID)+"\n")                          
        song_info_file.write("artist="+self.artist+"\n")                          # wykonawca 
        song_info_file.write("title="+self.title+"\n")                            # tytuł
        song_info_file.write("cover_artist="+str(self.cover_artist)+"\n")   
        song_info_file.write("name="+self.name+"\n")                          
        song_info_file.write("length_sec="+str(self.length_sec)+"\n")      # długość w sekundach
        song_info_file.write("length="+self.length+"\n")        # długość (string)
        song_info_file.write("volume="+str(self.volume)+"\n")                                 # głośność piosenki, z zakresu 0-200 chyba? 100 jest defaultem, wszystko będzie dobrane do konkretnej piosenki
        song_info_file.write("tempo="+str(self.tempo)+"\n")                                  # tempo piosenki, słownik w stylu {"00:02": 110, "01:45": 130}, oznacza tempo piosenki i moment rozpoczęcia tego tempa/bitu
        song_info_file.write("origin="+str(self.origin)+"\n")                                 # skąd pochodzi dany utwór (np. tytuł film, gra, inne tagi pomagające w znalezieniu piosenki, np. from The Greatest Showman)
        if len(self.genre)==0:                                                          # w ten sposób zapisujemy tablicę w jednej linijce, za pomocą stringa
            song_info_file.write("genre=\n")
        elif len(self.genre)==1:
            song_info_file.write("genre="+self.genre[0]+"\n")
        else:                                                                           # śmieszny sposób na wypisywanie pozycji po przecinku
            genre_string = self.genre[0]
            for i in range(len(self.genre)-1):
                genre_string = genre_string + ", " + self.genre[i+1]
            song_info_file.write("genre="+genre_string+"\n")
        if len(self.vibe)==0:                                                          
            song_info_file.write("vibe=\n")
        elif len(self.vibe)==1:
            song_info_file.write("vibe="+self.vibe[0]+"\n")
        else:
            vibe_string = self.vibe[0]
            for i in range(len(self.vibe)-1):
                vibe_string = vibe_string + ", " + self.vibe[i+1]
            song_info_file.write("vibe="+vibe_string+"\n")
        if len(self.language)==0:                                                          
            song_info_file.write("language=\n")
        elif len(self.language)==1:
            song_info_file.write("language="+self.language[0]+"\n")
        else:
            language_string = self.language[0]
            for i in range(len(self.language)-1):
                language_string = language_string + ", " + self.language[i+1]
            song_info_file.write("language="+language_string+"\n")
        song_info_file.write("is_cover="+str(self.is_cover)+"\n")                               # czy utwór jest coverem
        song_info_file.write("is_instrumental="+str(self.is_instrumental)+"\n")                        # czy utwór jest bez tekstu (w większości, flaga język może być razem z tą)
        song_info_file.write("is_lyrics="+str(self.is_lyrics)+"\n")                              # czy tekst jest pobrany i gotowy do wyświetlania
        song_info_file.write("is_lyrics_translated="+str(self.is_lyrics_translated)+"\n")                              # czy tłumaczenie tekstu (chyba będzie na angielski) jest pobrane
        song_info_file.write("is_lyrics_romanized="+str(self.is_lyrics_romanized)+"\n")                              # czy zromanizowany tekst jest pobrany (dla innych alfabetów)
        song_info_file.write("is_lyrics_synchronized="+str(self.is_lyrics_synchronized)+"\n")                 # czy tekst jest zgrany z rytmem utworu, czy kolejne linijki pokazują się wtedy kiedy trzeba - ustawiane automatycznie, na razie nieużywane, bo i tak synchronizacja następuje ręcznie
        song_info_file.write("is_lyrics_approved=None"+str(self.is_lyrics_approved)+"\n")                     # te same 4 aspekty, ale czy są zatwierdzone przez użytkownika (program w momencie pobierania zmienia poprzednie flagi, te są edytowane w BMP)
        song_info_file.write("is_lyrics_translated_approved="+str(self.is_lyrics_translated_approved)+"\n")                       
        song_info_file.write("is_lyrics_romanized_approved="+str(self.is_lyrics_romanized_approved)+"\n")                             
        song_info_file.write("is_lyrics_synchronized_approved="+str(self.is_lyrics_synchronized_approved)+"\n")                
        song_info_file.write("is_meme="+str(self.is_meme)+"\n")                                # czy utwór jest memem
        song_info_file.write("is_from_game="+str(self.is_from_game)+"\n")                           # czy utwór jest z gry
        song_info_file.write("is_from_movie="+str(self.is_from_movie)+"\n")                          # czy utwór jest z filmu
        song_info_file.write("is_cringe="+str(self.is_cringe)+"\n")                              # czy cringe
        song_info_file.write("times_played="+str(self.times_played)+"\n")                           # ile razy utwór został odtworzony (nawet tylko włączony na chwilę)
        song_info_file.write("times_listened="+str(self.times_listened)+"\n")                         # ile razy utwór został odsłuchany (powyżej pewnego progu)
        song_info_file.write("events="+self.events+"\n")                                    # słownik z eventami piosenki do efektów specjalnych w vizualizerze, np {"00:02": "czarno-białe", "01:45": "ogień", "02:12": "shake"}
        if len(self.dates_listened)==0:                                                          
            song_info_file.write("dates_listened=\n")
        elif len(self.dates_listened)==1:
            song_info_file.write("dates_listened="+self.dates_listened[0]+"\n")
        else:
            dates_listened_string = self.dates_listened[0]
            for i in range(len(self.dates_listened)-1):
                dates_listened_string = dates_listened_string + ", " + self.dates_listened[i+1]
            song_info_file.write("dates_listened="+dates_listened_string+"\n")                         # konkretne daty kiedy utwór został odsłuchany (powyżej pewnego progu) - może być kilka - lista
        song_info_file.close()


    def edit_attribute(self, att, val, add=False):                 # edytuje podaną informację o utworze, opcja czy atrybut nadpisać (np zmienić cover_artist), czy dodać jako nowy (np nowy vibe albo nową datą odsłuchania utworu)
        pass

def create_media_player_window():                       # tworzy layout zakładki monitor
    media_player_background_color = GLOBAL_POPUP_COLOR

    media_player_info_tab_layout = [
        # [sg.Button("PLAY", key="-BUTTONMEDIAPLAYERPLAYSONG-")],
        [sg.Text("Oryginalny wykonawca:", background_color=media_player_background_color), sg.Input("", key="-INPUTMEDIAPLAYERARTIST-", expand_x=True)],
        [sg.Text("Tytuł:", background_color=media_player_background_color), sg.Input("", key="-INPUTMEDIAPLAYERTITLE-", expand_x=True)],
        [sg.Text("Wykonawca coveru:", background_color=media_player_background_color), sg.Input("", key="-INPUTMEDIAPLAYERCOVERARTIST-", expand_x=True)],
        [sg.Text("Pochodzenie utworu:", background_color=media_player_background_color), sg.Input("", key="-INPUTMEDIAPLAYERORIGIN-", expand_x=True)],
        [sg.Text("Głośność domyślna:", background_color=media_player_background_color), sg.Slider(range=(0,200), key="-SLIDERMEDIAPLAYERVOLUME-", expand_x=True, orientation="horizontal", size=(50, 20), tick_interval=25, default_value=100, background_color=media_player_background_color, enable_events=True)],
        [sg.Text("Gatunek:", background_color=media_player_background_color), sg.Input("", key="-INPUTMEDIAPLAYERGENRE-", expand_x=True)],
        [sg.Text("Vibe:", background_color=media_player_background_color), sg.Input("", key="-INPUTMEDIAPLAYERVIBE-", expand_x=True)],
        [sg.Text("Język:", background_color=media_player_background_color), sg.Input("", key="-INPUTMEDIAPLAYERLANGUAGE-", expand_x=True)],
        [sg.Push(background_color=media_player_background_color), sg.Button("Zaktualizuj informacje", key="-BUTTONMEDIAPLAYERUPDATESONGINFO-", size=(11, 2)), sg.Push(background_color=media_player_background_color)],
        [sg.Checkbox("Cover", key="-CHECKBOXMEDIAPLAYERISCOVER-", background_color=media_player_background_color, enable_events=True), sg.Checkbox("Instrumental", key="-CHECKBOXMEDIAPLAYERISINSTRUMENTAL-", background_color=media_player_background_color, enable_events=True), sg.Checkbox("Z filmu", key="-CHECKBOXMEDIAPLAYERISFROMMOVIE-", background_color=media_player_background_color, enable_events=True), sg.Checkbox("Z gry", key="-CHECKBOXMEDIAPLAYERISFROMGAME-", background_color=media_player_background_color, enable_events=True), sg.Checkbox("Z mema", key="-CHECKBOXMEDIAPLAYERISMEME-", background_color=media_player_background_color, enable_events=True), sg.Checkbox("Cringe", key="-CHECKBOXMEDIAPLAYERISCRINGE-", background_color=media_player_background_color, enable_events=True)],
        [sg.Text("Status tekstu: ", background_color=media_player_background_color), sg.Checkbox("Pobrany", key="-CHECKBOXMEDIAPLAYERISLYRICS-", background_color=media_player_background_color, enable_events=True), sg.Checkbox("Tłumaczenie", key="-CHECKBOXMEDIAPLAYERISLYRICSTRANSLATED-", background_color=media_player_background_color, enable_events=True), sg.Checkbox("Romanizacja", key="-CHECKBOXMEDIAPLAYERISLYRICSROMANIZED-", background_color=media_player_background_color, enable_events=True), sg.Checkbox("Zsynchronizowany", key="-CHECKBOXMEDIAPLAYERISLYRICSSYNCHRONIZED-", background_color=media_player_background_color, enable_events=True)],
        [sg.Push(background_color=media_player_background_color), sg.Button("Wczytaj tekst", key="-BUTTONMEDIAPLAYERUPLOADLYRICS-", size=(11, 2), font=GLOBAL_FONT_SMALL), sg.Button("Wczytaj tłumaczenie", key="-BUTTONMEDIAPLAYERUPLOADTRANSLATION-", size=(11, 2), font=GLOBAL_FONT_SMALL), sg.Button("Wczytaj romanizację", key="-BUTTONMEDIAPLAYERUPLOADROMANIZATION-", size=(11, 2), font=GLOBAL_FONT_SMALL), sg.Push(background_color=media_player_background_color)]
    ]

    media_player_filter_tab_layout = [
        [sg.Checkbox("wyjścia", enable_events=True, default=True), sg.Checkbox("zadania", enable_events=True, default=True), sg.Checkbox("pozostałe", enable_events=True, default=True), sg.Push(), sg.Checkbox("coroczne", enable_events=True, default=False)],
        [sg.Checkbox("ważność = 1", enable_events=True, default=True), sg.Checkbox("ważność = 2", enable_events=True, default=True), sg.Checkbox("ważność = 3", enable_events=True, default=True), sg.Checkbox("ważność = 4", enable_events=True, default=True)]
    ]

    media_player_karaoke_tab_layout = [
        [sg.Text("LOL", background_color=media_player_background_color)],
        [sg.Button("Nagraj wydarzenia", size=(11, 2)), sg.Button("Pobierz tekst", size=(11, 2)), sg.Button("Otwórz tekst", size=(11, 2))]
    ]

    media_player_settings_tab_layout = [
        [sg.Button("Zaktualizuj bibliotekę", key="-BUTTONMEDIAPLAYERUPDATELIBRARY-", size=(11, 2))]
    ]

    media_player_layout = [
        [sg.Push(background_color=media_player_background_color), sg.Text("", key="-MEDIAPLAYERTEXTSONGNAME-", background_color=media_player_background_color), sg.Push(background_color=media_player_background_color)],
        [sg.ProgressBar(100, orientation="horizontal", key="-PROGRESSBARSONG-", size_px=(500,10), expand_x=True)],      # początkowa maksymalna wartość paska to 100 (sekund), ale zmienia się to za każdym razem jak wczytujemy piosenkę
        [sg.Push(background_color=media_player_background_color, ), sg.Text("00:00 / 00:00", key='-TEXTSONGTIME-', font=GLOBAL_FONT_NOTIFICATIONS, background_color=media_player_background_color),
            sg.Button(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_STOP, 30, 30), border_width=0, key="-BUTTONMEDIAPLAYERSTOPSONG-", button_color=media_player_background_color, mouseover_colors=media_player_background_color),
            sg.Button(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_PREVIOUS, 50, 50), border_width=0, key="-BUTTONMEDIAPLAYERPREVIOUSSONG-", button_color=media_player_background_color, mouseover_colors=media_player_background_color),
            sg.Button(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_PLAY, 70, 70), border_width=0, key="-BUTTONMEDIAPLAYERPLAYPAUSESONG-", button_color=media_player_background_color, mouseover_colors=media_player_background_color),
            sg.Button(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_NEXT, 50, 50), border_width=0, key="-BUTTONMEDIAPLAYERNEXTSONG-", button_color=media_player_background_color, mouseover_colors=media_player_background_color),
            sg.Button(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_SHUFFLE_PRESSED, 30, 30), border_width=0, key="-BUTTONMEDIAPLAYERSHUFFLE-", button_color=media_player_background_color, mouseover_colors=media_player_background_color),      # domyślnie jest shuffled=True
            sg.Text("      ", font=GLOBAL_FONT_NOTIFICATIONS, background_color=media_player_background_color),          # ten pusty tekst jest po to, żeby przyciski były idealnie na środku - po lewej stronie jest czas, a po drugiej jest przycisk Menu, więc długość tego tekstu jest w przybliżeniu różnicą szerokości tekstu z czasem i przycisku Menu
            sg.Push(background_color=media_player_background_color),
            sg.Button(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_MENU, 50, 50), border_width=0, key="-BUTTONMEDIAPLAYERMENU-", button_color=media_player_background_color, mouseover_colors=media_player_background_color)],
        [sg.Column([             # !!! cała dolna część BMP to kolumna, która się pojawia po naciśnięciu przycisku MENU, w niej są zakładki, pod zakładkami logtext
            [sg.TabGroup([[                                                              
                sg.Tab('Info', media_player_info_tab_layout, key="-MEDIAPLAYERTABINFO-", background_color=media_player_background_color),             
                sg.Tab('Filtry', media_player_filter_tab_layout, key="-MEDIAPLAYERTABFILTER-", background_color=media_player_background_color),            
                sg.Tab('Karaoke', media_player_karaoke_tab_layout, key="-MEDIAPLAYERTABKARAOKE-", background_color=media_player_background_color),
                sg.Tab('Ustawienia', media_player_settings_tab_layout, key="-MEDIAPLAYERTABSETTINGS-", background_color=media_player_background_color)
            ]], background_color=media_player_background_color, tab_background_color=media_player_background_color, selected_title_color=GLOBAL_MEDIA_PLAYER_THEME_ALT_COLOR, selected_background_color=media_player_background_color, key="-MEDIAPLAYERTABGROUP-")],
            [sg.Text("TEST", key='-MEDIAPLAYERLOGTEXT-', expand_x=True, font=GLOBAL_FONT_NOTIFICATIONS, background_color=media_player_background_color)],          # rozmiar podany jako zmienna globalna
            [sg.Push(background_color=media_player_background_color), sg.Text("Created by Mateusz Kowal, "+str(gv.calendar_year), font=GLOBAL_FONT_MINI, text_color='grey', pad=(0,0), border_width=0, background_color=media_player_background_color)]
        ], key="-COLUMNMEDIAPLAYERMENU-", background_color=media_player_background_color)]
    ]

    

    return sg.Window('BATI Media Player', media_player_layout, resizable=False, keep_on_top=False, finalize=True, no_titlebar=False, background_color=media_player_background_color, relative_location=(0,0), icon=get_avatar_path(GLOBAL_AVATAR_MUSIC_PLAYER_ICON))

def media_player_playbutton_pressed():              # dedykowana funkcja do wykonywania rzeczy po naciśnięciu przycisku play (przy pauzie od razu pauzujemy)
    if mixer.get_busy() == False:                   # jeśli piosenka została zapauzowana, to mixer nadal jest busy, play_song odtwarza od początku, więc dzięki temu wiemy że mamy wznowić odtwarzanie
        play_song(gv.current_song)                             # funkcja, która tylko odtwarza dźwięk, nic więcej
        clock = pygame_time.Clock()
    else:
        mixer.Channel(1).unpause()
    gv.time_paused += pygame_time.get_ticks() - gv.time_since_song_start
    gv.is_music_playing = True

def play_song(song: Song, volume=1.0):                           # odtwarza piosenki za pomocą VLC, używać tylko do BMP
    mixer_song = mixer.Sound(get_song_path(str(song.ID)+"/song.mp3"))
    mixer_song.set_volume(volume)
    mixer.Channel(1).play(mixer_song)

def pause_song():
    mixer.Channel(1).pause()
    gv.is_music_playing = False

def play_next_song():                                   # ustawia indeks playlisty na następny
    mixer.Channel(1).stop()
    gv.time_since_song_start = 0
    gv.time_paused = 0
    if gv.playlist_index+1 < len(gv.playlist):
        gv.playlist_index += 1
    else:
        gv.playlist_index = 0
    gv.current_song = gv.playlist[gv.playlist_index]
    if gv.is_music_playing:
        media_player_playbutton_pressed()

def play_previous_song():                               # ustawia indeks playlisty na poprzedni
    mixer.Channel(1).stop()
    gv.time_since_song_start = 0
    gv.time_paused = 0
    if gv.playlist_index > 0:
        gv.playlist_index -= 1
    else:
        gv.playlist_index = len(gv.playlist)-1
    gv.current_song = gv.playlist[gv.playlist_index]
    if gv.is_music_playing:
        media_player_playbutton_pressed()

def stop_song():
    mixer.Channel(1).stop()
    gv.time_since_song_start = 0
    gv.time_paused = 0
    gv.is_music_playing = False

def load_music_library():                               # ładuje całą bibliotekę utworów do jednej zmiennej globalnej (okaże się, czy to mądre i czy nie zjem całej pamięci komputera)
    gv.all_songs: list[Song] = []                       # !!! przypisanie typu zmiennej, dzięki temu VSC wie co to jest i podpowiada np pola danej klasy przy pisaniu
    gv.playlist: list[Song] = []
    gv.current_song: Song = None
    song_files = os.listdir(GLOBAL_SONGS_FOLDER_PATH)
    for id in song_files:
        gv.all_songs.append(load_song(id))

def load_song(id) -> Song:
    return Song(id)

# dla danej playlisty patrzy, które piosenki zostały już pobrane i jeśli ich jeszcze nie ma to zwraca je w postaci listy słowników; dodatkowo zwraca jeszcze informacje o samej playliście
def check_playlist_for_downloading(playlist_link_file_name = GLOBAL_MEDIA_PLAYER_PLAYLIST_LINK_FILE_NAME, downloaded_videos_file_name = GLOBAL_MEDIA_PLAYER_PLAYLIST_DOWNLOADED_LINKS) -> tuple[list[dict], str, str, int, int]: 
    playlist_link_file = open(get_media_player_file_path(playlist_link_file_name))
    link = playlist_link_file.readline()
    if link[-1]=="\n":                              # usuwanie ewentualnego znaku końca linii z linku
        link = link.strip("\n")
    playlist_link_file.close()
    playlist_ydl = yt_dlp.YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet':True,})
    with playlist_ydl:
        result = playlist_ydl.extract_info(link, download=False)        # wyciągamy info z linku do playlisty: jej tytuł i oczywiście filmiki z informacjami
        if 'entries' in result:                                         # jeśli są jakiekolwiek filmy (?) (może są jakieś różne rodzaje playlist? idk)
            # Can be a playlist or a list of videos
            playlist_title = result["title"]
            playlist_videos = result['entries']
            new_videos_list_string_names = ""
            new_videos_list_tab = []
            new_counter = 0
            for i, item in enumerate(playlist_videos):                  # iterujemy po każdym filmie na playliście i sprawdzamy, czy nie mamy go już w ściągniętych plikach, jest lista linków w pliku downloaded_videos_URLs.txt
                link = result['entries'][i]['webpage_url']
                with open(get_media_player_file_path(downloaded_videos_file_name)) as f:
                    if link not in f.read():                                            # sprawdzanie, czy link jest w pliku, to może dużo zajmować przy dużych plikach
                        new_videos_list_tab.append(result['entries'][i])                   # dla utworów, których nie ma chcemy zwrócić wszystkie potrzebne dane
                        # for key, value in result['entries'][i].items():
                        #     print(key, value)
                        new_videos_list_string_names += result['entries'][i]["uploader"]+" - "+result['entries'][i]["title"]+"\n"
                        new_counter +=1                                                 # zwracamy jeszcze wykonawcę oraz informacje ile jest nowych utworów do pobrania i w ogóle na playliście
    return new_videos_list_tab, new_videos_list_string_names, playlist_title, i+1, new_counter

def download_song(video: dict):             # pobiera utwór z internetu za pośrednictwem linku, tworzy pomocnicze pliki
    # !!!!!
    # (ℹ️) See help(yt_dlp.YoutubeDL) for a list of available options and public functions (wpisać w cmd python i potem help(yt_dlp.YoutubeDL) )
    # !!!!!

    # przygotowywanie zmiennych
    title = video["title"]
    if "creator" in video.keys():           # sprawdza, czy jest klucz "creator" w słowniku przypisanym do danego video; tylko dla utworów muzycznych będzie creator, dla filmików trzeba użyć uploader
        author = video["creator"]
    else:
        uploader = video["uploader"]
        e, values = popup_double_enter(question = "Utwór "+title+" z kanału "+uploader+" nie ma przypisanego twórcy. Jaką zapisaną nazwę ma mieć utwór i twórca?", title="BATI Media Player", textbox_text1=uploader, textbox_text2=title)
        author = values['-POPUPENTERTEXT1-']
        title = values['-POPUPENTERTEXT2-']
    if "Topic" in author:                   # jeśli jest Topic na końcu, to usuwamy
        author = author.strip("- Topic")
    song_name = author+" - "+title          # !!! nieużywane, zamiast tego jest używane ID !!!     # optymistycznie zakładam, że nie ma opcji, żeby były dwa utwory o takiej samej nazwie od tego samego twórcy
    link = video["webpage_url"]
    assign_new_song_id()                    # przypisuje ID nowej piosence - ID będzie użyte do wyszukiwania piosenek
    song_folder_path = get_song_path(str(gv.new_song_id))
    if not os.path.exists(song_folder_path):           # tworzenie folderu dla nowego utworu
        os.makedirs(song_folder_path)
    
    # opcje pobierania
    ydl_options = {
        'format': 'mp3/bestaudio/best',
        'outtmpl': song_folder_path+"/song",
        'verbose': False,
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
    #       'preferredquality': '192',          # można by się tym pobawić, żeby zmniejszyć rozmiar, ale wtedy jakość spada
        }]
    }
    
    # pobieranie utworu
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        error_code = ydl.download(link)
    if error_code:
        print("Wystąpił błąd podczas pobierania "+song_name)

    # pobieranie miniaturki
    urllib.request.urlretrieve(video["thumbnail"], song_folder_path+"/thumbnail.jpg")           # pobieranie miniaturki filmu

    # pobieranie tekstu, czyszczenie + próba pobrania tłumaczenia na angielski i wersji romanizowanej
    genius = lg.Genius(GLOBAL_MEDIA_PLAYER_GENIUS_API_KEY, timeout=15, retries=3)
    genius.verbose = False
    genius.remove_section_headers = True
    genius_song = genius.search_song(title, author, get_full_info=False)
    is_lyrics = False
    is_lyrics_translated = False
    is_lyrics_romanized = False
    if genius_song is not None:
        lyrics_file = open(song_folder_path+"/lyrics.txt", "w", encoding='utf-8')               # zapisywanie tekstu piosenki
        for line in list(map(clean_line, genius_song.lyrics.split("\n"))):                      # czyści tekst piosenki za pomocą mapowania funkcji do poszczególnych stringów (linijek) tekstu
            lyrics_file.write(line+"\n")                            
        lyrics_file.close()
        is_lyrics = True
    genius_song = genius.search_song(title+" translation", author, get_full_info=False)
    if genius_song is not None:
        lyrics_file = open(song_folder_path+"/lyrics_translation.txt", "w", encoding='utf-8')       # zapisywanie tłumaczenia na angielski (o ile istnieje)
        for line in list(map(clean_line, genius_song.lyrics.split("\n"))):
            lyrics_file.write(line+"\n")
        lyrics_file.close()
        is_lyrics_translated = True
    genius_song = genius.search_song(title+" romanized", author, get_full_info=False)               # zapisywanie zromanizowanej wersji tekstu (o ile istnieje)
    if genius_song is not None:
        lyrics_file = open(song_folder_path+"/lyrics_romanization.txt", "w", encoding='utf-8')
        for line in list(map(clean_line, genius_song.lyrics.split("\n"))):
            lyrics_file.write(line+"\n")
        lyrics_file.close()
        is_lyrics_romanized = True

    # tworzenie pliku z informacjami o utworze; wszystko co jest tutaj jest przypisywane w konstruktorze podczas tworzenia obiektu klasy Song
    # przy każdej zmiennej ma być wartość lub None, chyba że zmienna to tablica, wtedy może być puste miejsce (bez None'a)
    song_info_file = open(song_folder_path+"/info.txt", "w", encoding='utf-8')
    song_info_file.write("URL="+link+"\n")                               # link
    song_info_file.write("ID="+str(gv.new_song_id)+"\n")                               # ID utworu
    song_info_file.write("artist="+author+"\n")                          # wykonawca (oryginalny)
    song_info_file.write("title="+title+"\n")                            # tytuł
    song_info_file.write("cover_artist=None"+"\n")                            # nazwa artysty, który wykonał cover
    song_info_file.write("name="+song_name+"\n")                          # tytuł
    song_info_file.write("length_sec="+str(video["duration"])+"\n")      # długość w sekundach
    song_info_file.write("length="+video["duration_string"]+"\n")        # długość (string)
    song_info_file.write("volume=100"+"\n")                                 # głośność piosenki, z zakresu 0-200 chyba? 100 jest defaultem, wszystko będzie dobrane do konkretnej piosenki
    song_info_file.write("tempo="+"\n")                                  # tempo piosenki, słownik w stylu {"00:02": 110, "01:45": 130}, oznacza tempo piosenki i moment rozpoczęcia tego tempa/bitu
    song_info_file.write("origin=None"+"\n")                                 # skąd pochodzi dany utwór (np. tytuł film, gra, inne tagi pomagające w znalezieniu piosenki, np. from The Greatest Showman)
    song_info_file.write("genre="+"\n")                                  # gatunek - może być kilka: [metal, rock, pop, electronic, classic]
    song_info_file.write("vibe="+"\n")                                   # klimat danej piosenki - może być kilka: [power, chill, sad, happy, disco]
    song_info_file.write("language="+"\n")                               # język - może być kilka
    song_info_file.write("is_cover=None"+"\n")                               # czy utwór jest coverem
    song_info_file.write("is_instrumental=None"+"\n")                        # czy utwór jest bez tekstu (w większości, flaga język może być razem z tą)
    song_info_file.write("is_lyrics="+str(is_lyrics)+"\n")                              # czy tekst jest pobrany i gotowy do wyświetlania
    song_info_file.write("is_lyrics_translated="+str(is_lyrics_translated)+"\n")                              # czy tłumaczenie tekstu (chyba będzie na angielski) jest pobrane
    song_info_file.write("is_lyrics_romanized="+str(is_lyrics_romanized)+"\n")                              # czy zromanizowany tekst jest pobrany (dla innych alfabetów)
    song_info_file.write("is_lyrics_synchronized=None"+"\n")                 # czy tekst jest zgrany z rytmem utworu, czy kolejne linijki pokazują się wtedy kiedy trzeba - ustawiane automatycznie, na razie nieużywane, bo i tak synchronizacja następuje ręcznie
    song_info_file.write("is_lyrics_approved=False"+"\n")                     # te same 4 aspekty, ale czy są zatwierdzone przez użytkownika (program w momencie pobierania zmienia poprzednie flagi, te są edytowane w BMP)
    song_info_file.write("is_lyrics_translated_approved=False"+"\n")                       
    song_info_file.write("is_lyrics_romanized_approved=False"+"\n")                             
    song_info_file.write("is_lyrics_synchronized_approved=False"+"\n")                
    song_info_file.write("is_meme=None"+"\n")                                # czy utwór jest memem
    song_info_file.write("is_from_game=None"+"\n")                           # czy utwór jest z gry
    song_info_file.write("is_from_movie=None"+"\n")                          # czy utwór jest z filmu
    song_info_file.write("is_cringe=None"+"\n")                              # czy cringe
    song_info_file.write("times_played=0"+"\n")                           # ile razy utwór został odtworzony (nawet tylko włączony na chwilę)
    song_info_file.write("times_listened=0"+"\n")                         # ile razy utwór został odsłuchany (powyżej pewnego progu)
    song_info_file.write("events="+"\n")                                    # słownik z eventami piosenki do efektów specjalnych w vizualizerze, np {"00:02": "czarno-białe", "01:45": "ogień", "02:12": "shake"}
    song_info_file.write("dates_listened="+"\n")                         # konkretne daty kiedy utwór został odsłuchany (powyżej pewnego progu) - może być kilka - lista
    song_info_file.close()
    # przypilnować, żeby do rozdzielania stringa używać PIERWSZEGO znaku "=" (w linku jeszcze mogą być, może czasem w innych miejscach)

    # dodawanie linku do pliku z listą pobranych piosenek (na końcu, jako potwierdzenie że wszystko było ok)
    song_list_file = open(get_media_player_file_path(GLOBAL_MEDIA_PLAYER_PLAYLIST_DOWNLOADED_LINKS), "a", encoding='utf-8')
    song_list_file.write(link+"\n")
    song_list_file.close()

def assign_new_song_id(read_file = GLOBAL_MEDIA_PLAYER_NEW_ID_FILE_NAME):        # przypisuje nowy numer ID piosence
    id_file = open(get_media_player_file_path(read_file), "r")                                          # wczytujemy plik z nowym ID dla wydarzenia
    gv.new_song_id = int(id_file.readline().strip("\n"))                 
    id_file.close()
    id_file = open(get_media_player_file_path(GLOBAL_MEDIA_PLAYER_NEW_ID_FILE_NAME), "w")
    id_file.write(str(gv.new_song_id+1))
    id_file.close()
