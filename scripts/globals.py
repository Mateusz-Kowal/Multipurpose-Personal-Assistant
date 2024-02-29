import datetime

def initialize():
    global there_are_things_to_do
    there_are_things_to_do = True
    global current_month_word
    current_month_word = datetime.datetime.now().strftime("%B")                                     # !!! przypisanie obecnego czasu przy odpaleniu programu, mają nie być zmieniane, chyba że przez ponowne wczytanie systemowej daty
    global current_month_number
    current_month_number = int(datetime.datetime.now().strftime("%m"))
    global current_year
    current_year = int(datetime.datetime.now().strftime("%Y"))
    global current_day
    current_day = int(datetime.datetime.now().strftime("%d"))
    global calendar_month_word
    calendar_month_word = current_month_word                                                        # zmienne określające to co jest wyświetlane na kalendarzu, początkowo obecny czas, zmienia się wraz ze zmianą miesięcy w kalendarzu
    global calendar_month_number
    calendar_month_number = current_month_number
    global calendar_year
    calendar_year = current_year
    global calendar_new_event_id
    calendar_new_event_id = ""
    global log_string                                                                               # zmienna z logami zapasowa na wypadek crasha
    log_string = ""
    global calendar_decide_events                                                                   # tablica z minionymi wydarzeniami, o których trzeba zadecydować
    calendar_decide_events = []                                                                     # !!! to nie jest chyba dobry pomysł, żeby to robić w taki sposób, ale nie wiem jak to inaczej przekazywać
    global load_calendar_history
    load_calendar_history = False
    global run_as_administrator                                                                     # informuje, czy program został odpalony w trybie administatora - określa to za pomocą tego, czy 
    run_as_administrator = False
    global computer_data                                                                            # zmienna przechowjąca odczyty z podzespołów komputera
    computer_data = None
    global monitor_data                                                                             # zmienna przechowująca wartości do wyświetlania na wykresie w monitorze
    monitor_data = {"Time" : [], "CPU_temp" : [], "GPU_temp" : [], "CPU_usage" : [], "GPU_usage" : [], "RAM_usage" : [], "RAM_value" : [], "FAN_usage" : [], "FAN2_usage" : [], "FAN3_usage" : [], "FAN5_usage" : [], "FAN6_usage" : [], "FAN2_speed" : [], "FAN3_speed" : [], "FAN5_speed" : [], "FAN6_speed" : []}
    global monitor_timestamps                                                                       # czasy do wyświetlania na osi X na wykresie monitora
    monitor_timestamps = []
    global monitor_plot_figure                                                                      # plot z matplotliba, który jest używany do wyświetlania danych w monitorze
    monitor_plot_figure = None
    global figure_canvas_agg                                                                        # dziwny obiekt canvasowy, za pomocą którego można umieścić wykres matplotliba w okienku PySimpleGUI
    figure_canvas_agg = None
    global monitor_dict                                                                             # słownik z informacją, które wykresy mają być pokazywane w monitorze
    monitor_dict = {"CPU_temp" : True, "GPU_temp" : True, "CPU_usage" : True, "GPU_usage" : True, "RAM_usage" : False, "FAN_usage" : True, "FAN2_usage" : False, "FAN3_usage" : False, "FAN5_usage" : False, "FAN6_usage" : False, "FAN2_speed" : True, "FAN3_speed" : True, "FAN5_speed" : True, "FAN6_speed" : True}
    global monitor_view_mode                                                                        # tryb wykresu monitora: temp, usage lub fan
    monitor_view_mode = "temp"
    global is_monitor_window                                                                        # czy popup monitora jest uruchomiony
    is_monitor_window = False
    global is_media_player_window                                                                   # czy okno media playera jest uruchomione
    is_media_player_window = False                                                              
    global is_music_playing                                                                         # czy w danym momencie gra muzyka
    is_music_playing = False
    global time_since_song_start                                                                    # czas, jaki upłynął od włączenia piosenki (wliczając ewentualnie pauzy)
    time_since_song_start = 0
    global time_paused                                                                              # czas, przez który piosenka była zapauzowana (odejmuje się potem to od time_since_song_start)
    time_paused = 0
    global is_media_player_tab_group_visible                                                        # zmienna informująca o tym, czy TabGroup w BMP jest widoczny (wewnętrza zmienna .visible nie chce się zmieniać)
    is_media_player_tab_group_visible = True
    global is_media_player_menu_open                                                                # czy menu w BMP jest otwarte
    is_media_player_menu_open = False
    global is_media_player_shuffle                                                                  # czy włączone jest losowe odtwarzanie piosenek
    is_media_player_shuffle = True 
    global new_song_id                                                                              # id dla nowo pobieranej piosenki, przechowywane w dedykowanym pliku
    new_song_id = ""
    global all_songs                                                                                # lista ze wszystkimi piosenkami które są na dysku
    #all_songs: list[Song] = []                             # ciekawostka: nie można przypisać typu zmiennej globalnej w ten sposób -> podobno trzeba to zrobić w zewnętrzej funkcji, gdzie już używamy tej zmiennej
    all_songs = []
    global playlist                                                                                 # playlista piosenek
    playlist = []
    global playlist_index                                                                           # indeks, która piosenka z playlisty jest teraz odtwarzana (może być ujemny)
    playlist_index = 0
    global current_song                                                                             # piosenka, która obecnie jest grana/ustawiona w BMP
    current_song = None