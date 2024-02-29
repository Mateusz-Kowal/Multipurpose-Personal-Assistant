# ustawienia, zmienne statyczne itd
# te rzeczy są nieedytowalne !!!                # jeżeli z jakiegoś powodu coś wymaga edycji, to przenieść zmienną do globals.py

# fajne theme'y
# DarkGrey14
# DarkGrey11
# SandyBeach
# Topanga
# DarkBlack

# Fixedsys                  # nie ma polskich znaków :(
# Consolas
# Lucida Console
# Courier
# Fixedsys Excelsior 3.01   <- działa!!!!
# można dodawać czczionki po prostu je instalując na kompie WTF :D

# ogólne, estetyczne
GLOBAL_IS_DEV_VERSION = True        # <-------                              # czy wersja programu jest wersją developerską, to zmieniamy za każdym razem przy tworzeniu nowej wersji

if GLOBAL_IS_DEV_VERSION == False:
    GLOBAL_BATI_VERSION = '1.1.5'                                               # wersja programu, np. "1.2.4"
else:
    GLOBAL_BATI_VERSION = 'DEVELOPMENTAL'

GLOBAL_THEME = 'DarkBlack'                                                      # motyw aplikacji
GLOBAL_THEME_TABS_UNSELECTED_BACKGROUND_COLOR = "Dark Blue 3"                   # tło niezaznaczonej zakładki
GLOBAL_FONT = ("Fixedsys Excelsior 3.01", 16)                                   # dla Calibri 14 (57, 2);        dla Consolas 14;       dla Fixedsys Excelsior 3.01 16;     
GLOBAL_FONT_CALENDAR_BUTTONS = ("Fixedsys Excelsior 3.01", 14)                  # czcionka dla przycisków kalendarza
GLOBAL_FONT_SMALL = ("Fixedsys Excelsior 3.01", 12)
GLOBAL_FONT_NOTIFICATIONS = GLOBAL_FONT_SMALL                                   # czcionka dla powiadomień, na razie ta sama tylko mniejsza, potem może coś się zrobi
GLOBAL_FONT_MINI = ("Fixedsys Excelsior 3.01", 10)                              # bardzo mała czcionka dla specjalnych zastosowań
GLOBAL_FONT_BIG = ("Fixedsys Excelsior 3.01", 20)
GLOBAL_LOG_PANEL_COLOR_DEFAULT = '#ffff99'                                      # jasny żółty
GLOBAL_POPUP_COLOR = '#002b80'                                                  # ciemny niebieski
#GLOBAL_POPUP_THEME = 'SandyBeach'                                              # nieużywane, bo nie działa, bardzo trudno się zmienia theme okna, zwłaszcza pojedynczego
GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS = 62                                        # zależy od global fonta; szerokość elementów, które mają się rozciągać na całą szerokość; również wartość do wrapowania tekstu, zeby wyskakujące okna nie były dłuższe niż główne

# ścieżki
GLOBAL_DEV_FOLDER_PATH = "../../_DEV/scripts/"                                  # ścieżka z miejsca pliku .exe do folderu wersji deweloperskiej _DEV
GLOBAL_IS_BATI_RUNNING_FOLDER_PATH = "text_files/globals/"                      # ścieżka do folderu z plikiem informującym, czy BATI jest już włączony
GLOBAL_AVATARS_FOLDER_PATH = "avatars/"                                         # ścieżka do folderu z avatarami
GLOBAL_CALENDAR_IMAGES_FOLDER_PATH = "images/calendar/"                                           # ścieżka do folderu z plikami graficznymi
GLOBAL_MEDIA_PLAYER_IMAGES_FOLDER_PATH = "images/media_player/"                                           # ścieżka do folderu z plikami graficznymi
GLOBAL_MEDIA_PLAYER_THUMBNAILS_FOLDER_PATH = "images/media_player/thumbnails/"                                           # ścieżka do folderu z plikami graficznymi
GLOBAL_SOUNDS_FOLDER_PATH = "sounds/"                                           # ścieżka do folderu z plikami dźwiękowymi
GLOBAL_SONGS_FOLDER_PATH = "songs/"                                             # ścieżka do folderu z plikami dźwiękowymi piosenek (osobny folder)
GLOBAL_CALENDAR_TEXT_FILES_FOLDER_PATH = "text_files/calendar/"                      # ścieżka do folderu z plikami kalendarza (są tu również month_completion)
GLOBAL_MONITOR_TEXT_FILES_FOLDER_PATH = "text_files/monitor/"                        # ścieżka do folderu z plikami monitora
GLOBAL_CONTROL_TEXT_FILES_FOLDER_PATH = "text_files/control/"                        # ścieżka do folderu z plikami panelu kontrolnego - tutaj trafiają wszystkie pliki ważne dla całego programu
GLOBAL_MEDIA_PLAYER_TEXT_FILES_FOLDER_PATH = "text_files/media_player/"              # ścieżka do folderu z playlistą do pobrania
GLOBAL_PACKAGES_PATH = "packages/"                                              # ścieżka do folderu z paczkami (pliki .dll)

# nazwy plików
GLOBAL_IS_BATI_RUNNING_FILE_NAME = "is_Bati_running.txt"                        # nazwa pliku z informacją, czy program jest włączony czy nie
GLOBAL_CALENDAR_SAVE_FILE_NAME = "calendar_save.txt"                            # nazwa pliku z danymi kalendarza (zapisane wydarzenia)
GLOBAL_CALENDAR_HISTORY_FILE_NAME = "calendar_history.txt"                      # nazwa pliku z danymi kalendarza (historia wydarzeń, nie są one nigdy usuwane);            !!! HISTORY - wszystkie wydarzenia kiedykolwiek dodane
GLOBAL_CALENDAR_MONTH_HISTORY_FILE_NAME = "calendar_month_history.txt"          # nazwa pliku z historią kalendarza z tego miesiąca                                    !!! COMPLETION - wszystkie wydarzenia ukończone
GLOBAL_CALENDAR_MONTH_COMPLETION_FILE_NAME = "calendar_month_completion.txt"    # nazwa pliku z wydarzeniami, które zostały wykonane danego miesiąca (aktualizowane ręcznie)
GLOBAL_CALENDAR_TODAY_FILE_NAME = "calendar_today.txt"                          # nazwa pliku z wydarzeniami do zrobienia dzisiaj
GLOBAL_CALENDAR_NEW_ID_FILE_NAME = "calendar_new_event_id.txt"                  # nazwa pliku z ID następnego wydarzenia dodanego do kalendarza (w calendar_history lub analogicznym pliku ostatnie id powinno być o 1 mniejsze)
GLOBAL_CALENDAR_POINTS_FILE_NAME = "calendar_points.txt"                        # nazwa pliku z miesięcznymi punktami kalendarza rozpisanymi dla każdego miesiąca
GLOBAL_CALENDAR_POINTS_RECORD_FILE_NAME = "calendar_points_record.txt"          # nazwa pliku z miesięcznym rekordem punktów kalendarza
GLOBAL_MONITOR_RECORDS_FILE_NAME = "record_values.txt"                          # nazwa pliku z zapisywanymi rekordami odczytów monitora
GLOBAL_MONITOR_DATA_FILE_NAME = "monitor_data.txt"                              # nazwa pliku z zapisanymi danymi z monitora (cały odczyt z ostatniej godziny)
GLOBAL_MEDIA_PLAYER_PLAYLIST_LINK_FILE_NAME = "UMM_playlist_URL.txt"            # nazwa pliku z linkiem do playlisty do pobrania
GLOBAL_MEDIA_PLAYER_PLAYLIST_DOWNLOADED_LINKS = "downloaded_videos_URLs.txt"    # nazwa pliku z listą linków pobranych utworów
GLOBAL_LOG_FILE_NAME = "log.txt"                                                # nazwa pliku z logami programu
GLOBAL_CRASH_LOG_FILE_NAME = "crash_log.txt"                                    # nazwa pliku, do którego zapisywane są logi na wypadek crasha

# avatary                                                                       # przy używaniu należy dodać ścieżkę!                       
GLOBAL_AVATAR_DEFAULT = "EZY.png"                                               # ikona programu (po lewej stronie paska na górze) (na razie EZY, potem może się coś zmieni)
GLOBAL_AVATAR_ICON = "EZY.ico"
GLOBAL_AVATAR_INFO = "EZY.png"           # DO ZMIANY
GLOBAL_AVATAR_WARNING = "Madge.png"
GLOBAL_AVATAR_WARNING_CONFIRM = "MonkaS.png"
GLOBAL_AVATAR_ERROR = "Dedge.png"
GLOBAL_AVATAR_EDIT = "PepoG.png"
GLOBAL_AVATAR_EDIT_BACKGROUND = "PepoG_background_blue.png"                     # dla zmienionego koloru tła nie będzie działać
GLOBAL_AVATAR_SLEEP = "Bedge.png"
GLOBAL_AVATAR_NOTIFY = "DinkDank.gif"
GLOBAL_AVATAR_MUSIC_PLAYER_ICON = "peepoDJ.ico"  

# dźwięki                                                                       # przy używaniu należy dodać ścieżkę!
GLOBAL_SOUND_START_UP = "start_up.mp3"                                          # dźwięki puszczane przy otwieraniu programu
GLOBAL_SOUND_START_UP_EARRAPE = "start_up_earrape.mp3"
GLOBAL_SOUND_SHUT_DOWN = "shut_down.mp3"                                        # dźwięk puszczany przy zamykaniu programu
GLOBAL_SOUND_ERROR = "error.mp3"                                                # dźwięk puszczany przy błędzie programu
GLOBAL_SOUND_NOTIFICATION = "notification_bell.mp3"                             # dźwięk powiadomienia wyświetlanego w lewym dolmym rogu ekranu
GLOBAL_SOUND_POINTS_GAIN_SMALL = "points_gain_small.mp3"                        # dźwięki ukończenia wydarzenia i zdobycia punktów
GLOBAL_SOUND_POINTS_GAIN_MEDIUM = "points_gain_medium.mp3"
GLOBAL_SOUND_POINTS_GAIN_BIG = "points_gain_big.mp3"

# panel kontrolny
GLOBAL_CONTROL_TO_DO_BUTTON_NUMBER = 3                                          # liczba rzeczy do zrobienia dzisiaj w panelu to_do w kontrolce
GLOBAL_CONTROL_TO_DO_SIDE_BUTTON_NUMBER = 2                                     # liczba dodatkowych rzeczy do zrobienia dzisiaj w panelu to_do w kontrolce
GLOBAL_CONTROL_TO_DO_TOMORROW_BUTTON_NUMBER = 2                                 # liczba rzeczy do zrobienia jutro w panelu to_do w kontrolce
GLOBAL_CONTROL_DECIDE_PAST_BUTTON_NUMBER = 1                                    # liczba minionych wydarzeń, o których trzeba zadecydować co zrobić (czy uznać jako wykonane, czy usunięte, czy przesunąć)
GLOBAL_CONTROL_APP_BUTTON_ON_COLOR = "green"                                    # kolor przycisku włączania/wyłączania aplikacji, gdy aplikacja jest włączona
GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR = "#ff6969"     # "#ff6969"                     # kolor przycisku włączania/wyłączania aplikacji, gdy aplikacja jest wyłączona

# kalendarz
GLOBAL_CALENDAR_DAY_BUTTONS_SIZE_CHARACTERS = (9, 3)                            # rozmiar przycisków dni w kalendarzu, może można to zrobić jakoś automatycznie?;   (8, 3) dla czczionki 16;     !!! właściwie to nie ma znaczenia, decyduje i tak poniższa wartość
# GLOBAL_CALENDAR_DAY_BUTTONS_SIZE_PIXELS = (int(12/16*GLOBAL_FONT_CALENDAR_BUTTONS[1]), int(12/16*GLOBAL_FONT_CALENDAR_BUTTONS[1]))      # podobno 16 pixeli to font 12 czczionki
GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS = (85, 70)                        # rozmiar obrazu przycisku dnia w kalendarzu, rozmiar przycisku jest +4/+4m;    !!! decyduje to rozmiarze przycisku kalendarza!
GLOBAL_CALENDAR_DAY_BUTTONS_PAD = 4                                             # odstęp od brzegów przycisku, de facto przerwa między poszczególnymi przyciskami, niewidzialna obramówka;  4
GLOBAL_CALENDAR_DAY_BUTTONS_BORDER = 1                                          # grubość widzialnej obramówki; 1
GLOBAL_CALENDAR_DAY_BUTTON_TODAY_PAD = 0                                        # te same rzeczy, ale dla przycisku oznaczającego dzisiejszy dzień (ma być pogrubiony); 0
GLOBAL_CALENDAR_DAY_BUTTON_TODAY_BORDER = 7                                     #   7
GLOBAL_CALENDAR_DAY_BUTTONS_COLOR_FREE = "green"                                # #008000 kolor przycisków dni kalendarza, gdy dzień jest wolny;        UWAGA - te kolory dni na kalendarzu są rzadko używane, ze względu na przejście na gotowe obrazy
GLOBAL_CALENDAR_DAY_BUTTONS_COLOR_ONE_TASK = "red"                              # kolor przycisków dni kalendarza, gdy dzień ma jedno wydarzenie
GLOBAL_CALENDAR_DAY_BUTTONS_COLOR_IMPORTANT_TASK = "#00ccff"                    # kolor przycisków dni kalendarza, gdy jest tam dokładnie 1 wydarzenie z ważnością = 4
GLOBAL_CALENDAR_DAY_BUTTONS_COLOR_MULTIPLE_TASKS = "#990000"                    # kolor przycisków dni kalendarza, gdy dzień ma wiele wydarzeń
GLOBAL_CALENDAR_DAY_BUTTONS_COLOR_MULTIPLE_IMPORTANT_TASKS = "purple"           # kolor przycisków dni kalendarza, gdy jest co najmniej 1 wydarzenie o ważności 4 oraz co najmniej jedno inne wydarzenie o wazności 4 lub 3
GLOBAL_CALENDAR_DAY_BUTTONS_COLOR_UNAVAILABLE = "gray"                          # kolor przycisków dni kalendarza, gdy dzień nie istnieje XD
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_UNAVAILABLE = "calendar_day_unavailable.png"   # tła dla przycisków dni kalendarza, używane zamiast powyższych
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_FREE = "calendar_day_free.png"                 # #008000
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_FREE_TODAY = "calendar_day_free_today.png"
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3 = "calendar_day_imp3.png"                 # ff0000
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_TODAY = "calendar_day_imp3_today.png"
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_3 = "calendar_day_imp3_3.png"             # #990000
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_3_TODAY = "calendar_day_imp3_3_today.png"             
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_4 = "calendar_day_imp3_4.png"             # #9966ff
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_4_TODAY = "calendar_day_imp3_4.png"       
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP4 = "calendar_day_imp4.png"                 # #00ccff
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP4_TODAY = "calendar_day_imp4_today.png"     
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP4_4 = "calendar_day_imp4_4.png"             # #0000ff
GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP4_4_TODAY = "calendar_day_imp4_4_today.png"             
GLOBAL_CALENDAR_EVENT_NAME_MAX_LENGTH = 29                                      # maksywalna długość nazwy wydarzenia w kalendarzu, na razie 28 bo przy większej chyba tekst się wywala poza przycisk w menedżerze
GLOBAL_CALENDAR_SHOW_REPEAT_THRESHOLD = 30                                      # gdy repeat w wydarzeniu = 30 lub więcej, to wyświetlamy wydarzenie w kalendarzu;  na razie w formie globalnej, potem może zrobić to w interfejsie?
GLOBAL_CALENDAR_NOTIFICATION_TIME = "00:30"                                     # na ile przed wydarzeniem ma być powiadomienie
GLOBAL_CALENDAR_NOTIFICATION_TIME_MINUTES = 30                                  # to samo, potrzebna wartość liczbowa
GLOBAL_CALENDAR_NOTIFICATION_TIME_GOOUT = "02:00"                               # na ile przed wydarzeniem ma być powiadomienie, w przypadku wyjścia
GLOBAL_CALENDAR_NOTIFICATION_TIME_GOOUT_HOURS = 2                               # również potrzebna wartość liczbowa
GLOBAL_CALENDAR_POINTS_MEDIUM_RANGE_LIMIT = 500                                 # próg od kiedy są wartości punktowe ze "średniego zakresu" (odtwarzany jest osobny dźwięk)
GLOBAL_CALENDAR_POINTS_BIG_RANGE_LIMIT = 1000                                   # próg od kiedy są wartości punktowe z "wysokiego zakresu" (odtwarzany jest osobny dźwięk)
GLOBAL_CALENDAR_BEGINNING_DATE = "01.08.2022"                                   # początek istnienia BATIego, przedtem nie ma żadnych wydarzeń, wszystkie analizy i zliczenia są liczone maksymalnie od tej daty, nie wcześniej

# menedżer
GLOBAL_MANAGER_NUMER_OF_EVENT_BUTTONS = 100                              # liczba przycisków/pozycji wydarzeń w menedżerze, od tego zależy skalowanie scrollbara, ale każda wartość powinna być bezpieczna :)
GLOBAL_MANAGER_EVENT_BUTTONS_SIZE = (GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS-4, 1)                  # rozmiar przycisków/pozycji wydarzeń w menedżerze, expand_x nie działa, więc trzeba w sen sposób;  -4 bo scrollbar tyle zajmuje
GLOBAL_MANAGER_EVENT_IMPORTANCE_WEIGHT = 1                              # waga ważności do "optymalnego sortowania" - kluczowa składowa
GLOBAL_MANAGER_EVENT_DATE_DIFFERENCE_WEIGHT = 1                         # jeszcze *(-ln(x+1) + 2); waga tego, za ile dni będzie wydarzenie - im bliżej, tym wyżej będzie wydarzenie; poniżej 7 dni dodaje, powyżej odejmuje
GLOBAL_MANAGER_EVENT_POSITIVITY_WEIGHT = 0.01                           # waga pozytywności - pozytywne rzeczy będą ciut wyżej
GLOBAL_MANAGER_EVENT_REPEAT_WEIGTH = 0.01                               # jeszcze razy 1 / x+1; jeżeli zadanie się powtarza rzadko, to znaczy że jest chyba trochę bardziej specjalne, więc będzie troszke wyżej
GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY1 = "white"                        # biały
GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY2 = GLOBAL_LOG_PANEL_COLOR_DEFAULT # jasny żółty
GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY3 = "#FFD700"                      # złoty
GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY4 = GLOBAL_CALENDAR_DAY_BUTTONS_COLOR_IMPORTANT_TASK       # błękitny

# monitor
GLOBAL_FAN2_MAX_SPEED_THEORETICAL = 1700                                # CPU, Noctua NH-U12S redux - max 1700 RPM, w praktyce też max 1700 RPM; CPU FAN1
GLOBAL_FAN2_MAX_SPEED_MEASURED = 1700       # 1475, ale nie chcę zmieniać
GLOBAL_FAN3_MAX_SPEED_THEORETICAL = 1000                                # wentylator domyślny, raczej tył, nie wiadomo - max 1000 RPM, w praktyce max 940 RPM; SYS FAN1
GLOBAL_FAN3_MAX_SPEED_MEASURED = 973
GLOBAL_FAN5_MAX_SPEED_THEORETICAL = 1500                                # przód kolorowy, boost, Noctua NF-A14 - max 1500 RPM, w praktyce max 1400 RPM;  SYS FAN3
GLOBAL_FAN5_MAX_SPEED_MEASURED = 1424
GLOBAL_FAN6_MAX_SPEED_THEORETICAL = 1000                                # wentylator domyślny, raczej przód, nie wiadomo - max 1000 RPM, w praktyce max 850 RPM; SYS FAN4
GLOBAL_FAN6_MAX_SPEED_MEASURED = 862
GLOBAL_MONITOR_MAX_PLOT_LENGTH = 60                                     # maksymalna długość wykresu monitora - ile maksymalnie minut do tyłu może sięgać wykres
GLOBAL_CPU_USAGE_COLOR = "red"                                          # kolory przypisane do poszczególnych sensorów / komponentów komputera
GLOBAL_CPU_TEMP_COLOR = "red"
GLOBAL_GPU_USAGE_COLOR = "orange"
GLOBAL_GPU_TEMP_COLOR = "orange"
GLOBAL_FAN_USAGE_COLOR = "blue"
GLOBAL_FAN2_USAGE_COLOR = "#0055ff"
GLOBAL_FAN3_USAGE_COLOR = "#00ffff"
GLOBAL_FAN5_USAGE_COLOR = "#0099ff"
GLOBAL_FAN6_USAGE_COLOR = "#00ccff"
GLOBAL_FAN2_SPEED_COLOR = "#0055ff"
GLOBAL_FAN3_SPEED_COLOR = "#00ffff"
GLOBAL_FAN5_SPEED_COLOR = "#0099ff"
GLOBAL_FAN6_SPEED_COLOR = "#00ccff"
GLOBAL_RAM_USAGE_COLOR = "green"
GLOBAL_RAM_LOAD_COLOR = "green"

# media player
GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_PREVIOUS = "media_player_previous_button.png"                  # tło przycisku odtwarzania poprzedniej piosenki
GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_NEXT = "media_player_next_button.png"                          # tło przycisku odtwarzania następnej piosenki
GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_PLAY = "media_player_play_button.png"                          # tło przycisku włączenia odtwarzania
GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_PAUSE = "media_player_pause_button.png"                        # tło przycisku zapauzowania odtwarzania
GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_STOP = "media_player_stop_button.png"                          # tło przycisku zastopowania odtwarzania (powrót na początek piosenki)
GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_MENU = "media_player_menu_button.png"                          # przycisk menu
GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_MENU_PRESSED = "media_player_menu_button_pressed.png"          # przycisk menu
GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_SHUFFLE = "media_player_shuffle_button.png"                    # tło przycisku losowego wyboru piosenek
GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_SHUFFLE_PRESSED = "media_player_shuffle_button_pressed.png"    # tło przycisku losowego wyboru piosenek
GLOBAL_MEDIA_PLAYER_NEW_ID_FILE_NAME = "media_player_new_song_id.txt"                           # plik z id nowo dodanej piosenki
GLOBAL_MEDIA_PLAYER_GENIUS_API_KEY = "RiupKu3XuyJlPoOUqEnZ4j4_xOVljniTgh6oc1QKY_JN-bonO4XgwdNw221M189K"     # CLIENT ACCESS TOKEN ze strony https://genius.com/api-clients (trzeba było założyć konto: login: maties hasło: moje defaultowe bez liter)
GLOBAL_MEDIA_PLAYER_THEME_ALT_COLOR = "#E6B616"                                                       # kolor dopełniający w BMP
GLOBAL_MEDIA_PLAYER_UNASSIGNED_ATTRIBUTE_COLOR = GLOBAL_MEDIA_PLAYER_THEME_ALT_COLOR                  # kolor tekstu atrybutu, który nie został jeszcze przypisany przez użytkownika (np nie została podana informacja czy utwór jest coverem)
GLOBAL_MEDIA_PLAYER_ASSIGNED_ATTRIBUTE_COLOR = "white"

# symbole
GLOBAL_FAN_SYMBOL = "\u2707"                                            # symbol wentylatora
GLOBAL_CALENDAR_POINTS_SYMBOL = "\u227C\u2119\u227D"                    # symbol punktów kalendarza, na razie tragiczne, do zmiany

# dostępne czcionki bez instalowania
# ['@MS Gothic', '@MS PGothic', '@MS UI Gothic', '@Malgun Gothic', '@Malgun Gothic Semilight', '@Microsoft JhengHei', '@Microsoft JhengHei Light', '@Microsoft JhengHei UI', '@Microsoft JhengHei UI Light', '@Microsoft YaHei', '@Microsoft YaHei Light', '@Microsoft YaHei UI', '@Microsoft YaHei UI Light', '@MingLiU-ExtB', '@MingLiU_HKSCS-ExtB', '@NSimSun', '@PMingLiU-ExtB', '@SimSun', '@SimSun-ExtB', '@Yu Gothic', '@Yu Gothic Light', '@Yu Gothic Medium', '@Yu Gothic UI', '@Yu Gothic UI Light', '@Yu Gothic UI Semibold', '@Yu Gothic UI Semilight', 'Agency FB', 'Algerian', 'Arabic Transparent', 'Arial', 'Arial Baltic', 'Arial Black', 'Arial CE', 'Arial CE', 'Arial CYR', 'Arial Greek', 'Arial Narrow', 'Arial Rounded MT Bold', 'Arial TUR', 'Bahnschrift', 'Bahnschrift Condensed', 'Bahnschrift Light', 'Bahnschrift Light Condensed', 'Bahnschrift Light SemiCondensed', 'Bahnschrift SemiBold', 'Bahnschrift SemiBold Condensed', 'Bahnschrift SemiBold SemiConden', 'Bahnschrift SemiCondensed', 'Bahnschrift SemiLight', 'Bahnschrift SemiLight Condensed', 'Bahnschrift SemiLight SemiConde', 'Baskerville Old Face', 'Bauhaus 93', 'Bell MT', 'Berlin Sans FB', 'Berlin Sans FB Demi', 'Bernard MT Condensed', 'Blackadder ITC', 'Bodoni MT', 'Bodoni MT Black', 'Bodoni MT Condensed', 'Bodoni MT Poster Compressed', 'Book Antiqua', 'Bookman Old Style', 'Bookshelf Symbol 7', 'Bradley Hand ITC', 'Britannic Bold', 'Broadway', 'Brush Script MT', 'Calibri', 'Calibri Light', 'Californian FB', 'Calisto MT', 'Cambria', 'Cambria Math', 'Candara', 'Candara Light', 'Cascadia Code', 'Cascadia Code ExtraLight', 'Cascadia Code Light', 'Cascadia Code SemiBold', 'Cascadia Code SemiLight', 'Cascadia Mono', 'Cascadia Mono ExtraLight', 'Cascadia Mono Light', 'Cascadia Mono SemiBold', 'Cascadia Mono SemiLight', 'Castellar', 'Centaur', 'Century', 'Century Gothic', 'Century Schoolbook', 'Chiller', 'Colonna MT', 'Comic Sans MS', 'Consolas', 'Constantia', 'Cooper Black', 'Copperplate Gothic Bold', 'Copperplate Gothic Light', 'Corbel', 'Corbel Light', 'Courier', 'Courier', 'Courier New', 'Courier New Baltic', 'Courier New CE', 'Courier New CE', 'Courier New CYR', 'Courier New Greek', 'Courier New TUR', 'Curlz MT', 'Dubai', 'Dubai Light', 'Dubai Medium', 'Ebrima', 'Edwardian Script ITC', 'Elephant', 'Engravers MT', 'Eras Bold ITC', 'Eras Demi ITC', 'Eras Light ITC', 'Eras Medium ITC', 'Felix Titling', 'Fixedsys', 'Footlight MT Light', 'Forte', 'Franklin Gothic Book', 'Franklin Gothic Demi', 'Franklin Gothic Demi Cond', 'Franklin Gothic Heavy', 'Franklin Gothic Medium', 'Franklin Gothic Medium Cond', 'Freestyle Script', 'French Script MT', 'Gabriola', 'Gadugi', 'Garamond', 'Georgia', 'Gigi', 'Gill Sans MT', 'Gill Sans MT Condensed', 'Gill Sans MT Ext Condensed Bold', 'Gill Sans Ultra Bold', 'Gill Sans Ultra Bold Condensed', 'Gloucester MT Extra Condensed', 'Goudy Old Style', 'Goudy Stout', 'Haettenschweiler', 'Harlow Solid Italic', 'Harrington', 'High Tower Text', 'HoloLens MDL2 Assets', 'Impact', 'Imprint MT Shadow', 'Informal Roman', 'Ink Free', 'Javanese Text', 'Jokerman', 'Juice ITC', 'Kristen ITC', 'Kunstler Script', 'Leelawadee', 'Leelawadee UI', 'Leelawadee UI Semilight', 'Lucida Bright', 'Lucida Calligraphy', 'Lucida Console', 'Lucida Fax', 'Lucida Handwriting', 'Lucida Sans', 'Lucida Sans Typewriter', 'Lucida Sans Unicode', 'MS Gothic', 'MS Outlook', 'MS PGothic', 'MS Reference Sans Serif', 'MS Reference Specialty', 'MS Sans Serif', 'MS Serif', 'MS UI Gothic', 'MT Extra', 'MV Boli', 'Magneto', 'Maiandra GD', 'Malgun Gothic', 'Malgubold', 'Segoe UI Variable Text Semiligh', 'Showcard Gothic', 'SimSun', 'SimSun-ExtB', 'Sitka Banner', 'Sitka Banner Semibold', 'Sitka Display', 'Sitka Display Semibold', 'Sitka Heading', 'Sitka Heading Semibold', 'Sitka Small', 'Sitka Small Semibold', 'Sitka Subheading', 'Sitka Subheading Semibold', 'Sitka Text', 'Sitka Text Semibold', 'Small Fonts', 'Snap ITC', 'Stencil', 'Sylfaen', 'Symbol', 'System', 'Tahoma', 'Tempus Sans ITC', 'Terminal', 'Times New Roman', 'Times New Roman Baltic', 'Times New Roman CE', 'Times New Roman CE', 'Times New Roman CYR', 'Times New Roman Greek', 'Times New Roman TUR', 'Trebuchet MS', 'Tw Cen MT', 'Tw Cen MT Condensed', 'Tw Cen MT Condensed Extra Bold', 'Unispace', 'Verdana', 'Viner Hand ITC', 'Vivaldi', 'Vladimir Script', 'Webdings', 'Wide Latin', 'Wingdings', 'Wingdings 2', 'Wingdings 3', 'Yu Gothic', 'Yu Gothic Light', 'Yu Gothic Medium', 'Yu Gothic UI', 'Yu Gothic UI Light', 'Yu Gothic UI Semibold', 'Yu Gothic UI Semilight']