import traceback
from sys import exit as sys_exit

from Debug import *

# funkcje main'a

def create_main_window(theme):          # tworzy główne okno programu
    sg.theme(theme)                                                 # ustawianie opcji, takich jak theme i czcionkę - możliwe że będzie do zmiany potem w programie
    sg.set_options(font = GLOBAL_FONT)

    # control_tab_layout
    control_tab_layout = create_control_layout(theme)

    # calendar_tab layout
    calendar_tab_layout = create_calendar_layout(theme, button_dates, gv.current_month_word, gv.current_year)
    
    # manager_tab layout
    manager_tab_layout = create_manager_layout(theme)

    # monitor_tab layout
    monitor_tab_layout = create_monitor_layout(theme)

    # log_tab layout
    log_tab_layout = [
        [sg.Text('Historia działania programu', justification='center', expand_x=True)],
        [sg.Multiline('', key='-MULTILINELOG-', expand_x=True, expand_y=True)]
    ]

    # debug_tab layout
    debug_tab_layout = create_debug_layout(theme)

    # tworzenie głównego layoutu
    tab_layout = [
        [sg.TabGroup([[                                                                 # tworzenie TabGroup jest strasznie dziwne, uważać przy edycji bo się można pogubić
            sg.Tab('Control', control_tab_layout, key="-TABCONTROL-"),                  # zakładka kontrolna
            sg.Tab('Calendar', calendar_tab_layout, key="-TABCALENDAR-"),               # zakładka z kalendarzem
            sg.Tab('Manager', manager_tab_layout, key="-TABMANAGER-"),                  # zakładka z menedżerem zadań do zrobienia
            sg.Tab('Monitor', monitor_tab_layout, key="-TABMONITOR-"),                  # zakładka z monitorem komputera
            sg.Tab('Log', log_tab_layout, key="-TABLOG-"),                              # zakładka z pełnym logiem
            sg.Tab('Debug', debug_tab_layout, key="-DEBUGLOG-")                         # zakładka z rzeczami do debugowania/testowania/administrowania
        ]])],
        [sg.Button("", key='-BUTTONLOG-', button_color=GLOBAL_LOG_PANEL_COLOR_DEFAULT, size=(GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS, 2), expand_x=True)],          # rozmiar podany jako zmienna globalna
        [sg.Push(), sg.Text("Created by Mateusz Kowal, "+str(gv.calendar_year), font=GLOBAL_FONT_MINI, text_color='grey', pad=(0,0), border_width=0)]           # stopka na dole okna, parametry są takie a nie inne żeby była jak najcieńsza
    ]

    # tworzenie głównego okna programu
    # z jakiegoś powodu jak się nie da finalize=True, to nie działa timeout w read_all_windows(timeout=1000) w głównej pętli programu
    return sg.Window('BATI v.'+GLOBAL_BATI_VERSION, tab_layout, icon=get_avatar_path(GLOBAL_AVATAR_ICON), resizable=False, enable_close_attempted_event=True, keep_on_top=False, finalize=True)

def update(string):                     # update'uje sekcje programu przekazane w stringu
    if "calendar" in string:
        update_calendar()
    if "manager" in string:
        update_manager()
    if "monitor" in string:
        update_monitor()
    if "control" in string:
        update_control()

def check_for_event(event) -> tuple[sg.Window, str]:          # wykonuje się w każdej iteracji głównej pętli programu, sprawdza, czy następił jakiś event, wykonuje również funkcje dla timeouta; zwraca ewentualne nowoutworzone okno i jego nazwę
    log("Naciśnięto przycisk "+event, 1)
    if event == '-BUTTONCALPREV-':                # naciśnięcie klawisza poprzedniego miesiąca w kalendarzu
        change_month_prev()
        update_calendar()
    elif event == '-BUTTONCALNEXT-':              # naciśnięcie klawisza następnego miesiąca w kalendarzu
        change_month_next()
        update_calendar()
    elif event == '-MONTHTEXT-':                  # naciśnięcie tekstu z nazwą pokazywanego miesiąca powoduje powrót do obecnego miesiąca
        change_month_current()
        update_calendar()
    elif event == '-BUTTONADDCALENDAR-':          # dodanie wydarzenia do kalendarza
        add_to_calendar(values)
    elif event == '-TEXTINPUTDATE-':              # naciśnięcie tekstu "Data:" w kalendarzu powoduje wyczyszczenie się pola z datą (i innych też :P)
        update_calendar_input()
    elif event == '-BUTTONSWITCHBUTTONTEXT-':     # naciśnięcie przycisku zamieniającego tekst przycisków kalendarza z dnia na nazwę wydarzenia i odwrotnie
        calendar_switch_button_text()
    elif event == '-BUTTONCLEARCALENDARINPUT-':   # naciśniecie przycisku "Wyczyść" czyszczącego input kalendarza
        clear_calendar_input()
    elif event == '-BUTTONSWITCHHISTORYLOADING-': # naciśnięcie przycisku "Pokaż/Ukryj historię"
        # if gv.load_calendar_history == False:             # na razie niepotrzebne bo spowolnienie jest mało widoczne, a sam popup jest irytujący
        #     event, v = popup_warning_confirm("Czy na pewno chcesz załadować historię kalendarza?\nSpowolni to mocno działanie programu!")
        #     if event == "-POPUPWARNINGBUTTONNO-":
        #         return
        main_window['-BUTTONSWITCHHISTORYLOADING-'].update("Pokaż historię" if gv.load_calendar_history==True else "Ukryj historię")
        gv.load_calendar_history = not gv.load_calendar_history
        update_calendar()
    elif "CHECKBOXMANAGER" in event:              # naciśnięcie jednego z checkboxów do sortowania menadżera
        check_manager_events()
    elif "RCM" in event:                          # naciśnięcie opcji w Right Click Menu dla jakiegoś wydarzenia, w tej funkcji są dalsze ify, których zadaniem jest określić event
        calendar_right_click_menu_pressed(event)
    elif event == '-BUTTONMONITORUPDATE-':
        update_monitor()
        # save_monitor_records()                    # to jest raczej nie potrzebne, z jednej strony dzięki temu łatwiej "złapać" maksymalną wartość, z drugiej strony przy każdym kliknięciu update odczytujemy wartości z pliku, dodatkowa robota
    elif "DEBUG" in event:
        if event == '-BUTTONDEBUGCHECKPERIODICEVENTS-':
            check_periodic_events()
        elif event == '-BUTTONDEBUGCHECKPERIODICEVENTSINFO-':
            popup_info("Wymusza wykonanie funkcji check_periodic_events(), która uruchamia listę rzadkich funkcji. Domyślnie jest uruchamiana za pomocą biblioteki schedule, co minutę. Użycie tego przycisku pozwala ominąć ten okres.")
        elif event == '-BUTTONDEBUGCOUNTSCRIPTLINES-':
            debug_count_script_lines()
        elif event == '-BUTTONDEBUGCOUNTSCRIPTLINESINFO-':
            popup_info("Liczy linijki we wszystkich plikach .py kodu programu.")
        elif event == '-BUTTONDEBUGPRINTMEMORY-':
            debug_print_memory_usage()
        elif event == '-BUTTONDEBUGPRINTMEMORYINFO-':
            popup_info("Wyświetla informacje o wykorzystanej pamięci RAM programu.")
        elif event == '-BUTTONDEBUGCALCULATECALENDARPOINTS-':
            debug_calculate_calendar_points()
        elif event == '-BUTTONDEBUGCALCULATECALENDARPOINTSINFO-':
            popup_info("Ta funkcja przelicza na nowo punkty dla wszystkich miesięcy w historii kalendarza. Następnie zapisuje je w pliku z punktami. Ponadto na nowo oblicza rekordową wartość.\nUwaga! Funkcja usuwa wszystkie dotychczasowe zapisane punkty!")
    elif event == '-BUTTONMONITORPOPUPTOGGLE-':
        return button_monitor_toggle_pressed()      # wykonujemy funkcję i od razu zwracamy utworzone okno wraz z informacją co to za okno
    elif event == '-BUTTONMEDIAPLAYERWINDOWTOGGLE-':
        return button_media_player_toggle_pressed()
    elif "POPUPMONITORBUTTON" in event:
        move_monitor_popup(event)
    elif "MONITOR" in event:
        check_monitor_events(event)
    elif "MEDIAPLAYER" in event:
        check_media_player_events(event)
    elif "BUTTONCAL" in event:
        for i in range(42):                         # naciśnięcie na jeden z 42 przycisków wchodzących w skład kalendarza
            if event == f"-BUTTONCAL{i+1}-":
                button_cal_pressed(i+1, False)                        

def check_periodic_events():            # sprawdzanie, czy trzeba wykonać jakieś rzadkie funkcje; funkcja ta odpala się automatycznie w głównej pętli programu co minutę dzięki funkcji schedule.run_pending() (uprzednio utworzony schedule w funkcji things_to_do_only_once_after_opening_program())
    log("TIMEOUT")
    check_calendar_events_reminders()   # sprawdzanie, czy trzeba wyświetlić jakieś powiadomienie
    update_monitor()                    # aktualizowanie wykresu monitora o nowe odczyty
    save_monitor_records()              # zapisuje statystyki z monitora do pliku
    update_control()
    check_new_day()                     # sprawdzanie, czy nastąpiła zmiana dnia

def tick_events():             # sprawdzanie eventów co każdy timeout ORAZ co każdy event; jako że tak funkcja będzie wywoływana bardzo często (domyślnie co 100 ms) to tutaj musi być MINIMUM funkcji!
    #print(gv.is_music_playing)
    if gv.is_music_playing:
        media_player_tick_events()

# funkcje panelu kontrolnego

def update_control():                   # wyświetla odpowiednie wydarzenia na panelu kontrolnym
    log("Aktualizowanie panelu kontrolnego")
    # aktualizowanie części monitora
    cpu_load, cpu_temp, gpu_load, gpu_temp, fan_load, ram_usage = get_basic_monitor_values()
    main_window["-CONTROLCPULOAD-"].update("CPU: " + str(round(cpu_load)).rjust(2) + " %")
    main_window["-CONTROLCPUTEMP-"].update("     " + str(round(cpu_temp)).rjust(2) + "\u00B0C")
    main_window["-CONTROLGPULOAD-"].update(" GPU: " + str(round(gpu_load)).rjust(2) + " %")
    main_window["-CONTROLGPUTEMP-"].update("      " + str(round(gpu_temp)).rjust(2) + "\u00B0C")
    main_window["-CONTROLFANLOAD-"].update(" FANS:  " + str(round(fan_load)).rjust(2) + " %")
    main_window["-CONTROLRAMUSAGE-"].update(" RAM: " + str('{0:.1f}'.format(ram_usage)).rjust(4) + " GB")
    
    to_do_today_events, to_do_side_calendar_events, to_do_tomorrow_events = get_to_do_events()
    # wpisywanie wydarzeń do zrobienia dzisiaj
    for i in range(len(to_do_today_events)):
        button_string = to_do_today_events[i].name.center(30)           # poniższe linijki stylizują wyświetlanie na przycisku z dzisiejszym wydarzeniem wg tego czy jest godzina czy nie
        if to_do_today_events[i].hour_start == "":              # nie dodajemy 11 spacji w miejsce godziny, bo lepiej to wygląda jak będzie wycentrowane na środek przycisku
            pass
        elif to_do_today_events[i].hour_start != "" and to_do_today_events[i].hour_end == "":           
            button_string = button_string+"     "+to_do_today_events[i].hour_start+"    "                       # jak wyżej, ale 5 i 4 spacje, żeby było ładnie
        else:
            button_string = button_string+" "+to_do_today_events[i].hour_start+" - "+to_do_today_events[i].hour_end
        main_window[f'-BUTTONTODOEVENT{i+1}-'].update(button_string, button_color = to_do_today_events[i].color)
        main_window[f'-BUTTONTODOEVENT{i+1}-'].set_right_click_menu(create_calendar_right_click_menu([to_do_today_events[i]]))     # przyjmuje jedno-elementowę listę
    # uzupełnianie ewentualnych pustych miejsc          # tutaj kiedyś można np usuwać całe przyciski? ewentualnie wstawić gifa czy coś???
    if len(to_do_today_events) < GLOBAL_CONTROL_TO_DO_BUTTON_NUMBER:
        number_difference = GLOBAL_CONTROL_TO_DO_BUTTON_NUMBER-len(to_do_today_events)
        for i in range(number_difference):      # uzupełniamy od ostatniego przycisku bo tak będzie łatwiej
            main_window[f'-BUTTONTODOEVENT{GLOBAL_CONTROL_TO_DO_BUTTON_NUMBER-i}-'].update("", button_color=GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY1)          # ustawiamy domyślną pustą nazwę, kolor i puste RCM (nie da się chyba usunąć)
            main_window[f'-BUTTONTODOEVENT{GLOBAL_CONTROL_TO_DO_BUTTON_NUMBER-i}-'].set_right_click_menu(["Menu", ["-"]])        # jakimś cudem w kalendarzu da się usunąć całkowicie RCM z przycisku, a tutaj nie, no ale już trudno

    # wpisywanie minionych wydarzeń, co do których trzeba zadecydować co z nimi zrobić
    if len(gv.calendar_decide_events)<=GLOBAL_CONTROL_DECIDE_PAST_BUTTON_NUMBER:      # tutaj robimy to samo co w Control -> get_to_do_events(), ale dla zmiennej gv.calendar_decide_events (może da się to przenieść?)
        gv.calendar_decide_events = gv.calendar_decide_events[:]      
    else:
        gv.calendar_decide_events = gv.calendar_decide_events[0:GLOBAL_CONTROL_DECIDE_PAST_BUTTON_NUMBER]
    for i in range(len(gv.calendar_decide_events)):                 # wartość jest przypisywana w mainie
        button_string = gv.calendar_decide_events[i].name.center(30)    
        if gv.calendar_decide_events[i].hour_start == "":
            pass
        elif gv.calendar_decide_events[i].hour_start != "" and gv.calendar_decide_events[i].hour_end == "":           
            button_string = button_string+"     "+gv.calendar_decide_events[i].hour_start+"    "                       
        else:
            button_string = button_string+" "+gv.calendar_decide_events[i].hour_start+" - "+gv.calendar_decide_events[i].hour_end
        main_window[f'-BUTTONDECIDEEVENT{i+1}-'].update(button_string, button_color = gv.calendar_decide_events[i].color)
        main_window[f'-BUTTONDECIDEEVENT{i+1}-'].set_right_click_menu(create_calendar_right_click_menu([gv.calendar_decide_events[i]]))
    # uzupełnianie ewentualnych pustych miejsc
    if len(gv.calendar_decide_events) < GLOBAL_CONTROL_DECIDE_PAST_BUTTON_NUMBER:
        number_difference = GLOBAL_CONTROL_DECIDE_PAST_BUTTON_NUMBER-len(gv.calendar_decide_events)
        for i in range(number_difference):      # uzupełniamy od ostatniego przycisku bo tak będzie łatwiej
            main_window[f'-BUTTONDECIDEEVENT{GLOBAL_CONTROL_DECIDE_PAST_BUTTON_NUMBER-i}-'].update("", button_color=GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY1)
            main_window[f'-BUTTONDECIDEEVENT{GLOBAL_CONTROL_DECIDE_PAST_BUTTON_NUMBER-i}-'].set_right_click_menu(["Menu", ["-"]])

    # wpisywanie wydarzeń do zrobienia kiedyś
    for i in range(len(to_do_side_calendar_events)):
        button_string = to_do_side_calendar_events[i].name.center(30)           
        # if to_do_side_calendar_events[i].date == "":         # jak nie ma daty
        #     button_string = "          "+button_string
        if to_do_side_calendar_events[i].hour_start == "":
            pass
        elif to_do_side_calendar_events[i].hour_start != "" and to_do_side_calendar_events[i].hour_end == "":           
            button_string = button_string+"     "+to_do_side_calendar_events[i].hour_start+"    "                       
        else:
            button_string = button_string+" "+to_do_side_calendar_events[i].hour_start+" - "+to_do_side_calendar_events[i].hour_end
        main_window[f'-BUTTONTODOSIDEEVENT{i+1}-'].update(button_string, button_color = to_do_side_calendar_events[i].color)
        main_window[f'-BUTTONTODOSIDEEVENT{i+1}-'].set_right_click_menu(create_calendar_right_click_menu([to_do_side_calendar_events[i]]))
    # uzupełnianie ewentualnych pustych miejsc
    if len(to_do_side_calendar_events) < GLOBAL_CONTROL_TO_DO_SIDE_BUTTON_NUMBER:
        number_difference = GLOBAL_CONTROL_TO_DO_SIDE_BUTTON_NUMBER-len(to_do_side_calendar_events)
        for i in range(number_difference):      # uzupełniamy od ostatniego przycisku bo tak będzie łatwiej
            main_window[f'-BUTTONTODOSIDEEVENT{GLOBAL_CONTROL_TO_DO_SIDE_BUTTON_NUMBER-i}-'].update("", button_color=GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY1)
            main_window[f'-BUTTONTODOSIDEEVENT{GLOBAL_CONTROL_TO_DO_SIDE_BUTTON_NUMBER-i}-'].set_right_click_menu(["Menu", ["-"]])

    # wpisywanie wydarzeń do zrobienia jutro
    for i in range(len(to_do_tomorrow_events)):
        button_string = to_do_tomorrow_events[i].name.center(30)    
        if to_do_tomorrow_events[i].hour_start == "":
            pass
        elif to_do_tomorrow_events[i].hour_start != "" and to_do_tomorrow_events[i].hour_end == "":           
            button_string = button_string+"     "+to_do_tomorrow_events[i].hour_start+"    "                       
        else:
            button_string = button_string+" "+to_do_tomorrow_events[i].hour_start+" - "+to_do_tomorrow_events[i].hour_end
        main_window[f'-BUTTONTODOTOMORROWEVENT{i+1}-'].update(button_string, button_color = to_do_tomorrow_events[i].color)
        main_window[f'-BUTTONTODOTOMORROWEVENT{i+1}-'].set_right_click_menu(create_calendar_right_click_menu([to_do_tomorrow_events[i]]))
    # uzupełnianie ewentualnych pustych miejsc
    if len(to_do_tomorrow_events) < GLOBAL_CONTROL_TO_DO_TOMORROW_BUTTON_NUMBER:
        number_difference = GLOBAL_CONTROL_TO_DO_TOMORROW_BUTTON_NUMBER-len(to_do_tomorrow_events)
        for i in range(number_difference):      # uzupełniamy od ostatniego przycisku bo tak będzie łatwiej
            main_window[f'-BUTTONTODOTOMORROWEVENT{GLOBAL_CONTROL_TO_DO_TOMORROW_BUTTON_NUMBER-i}-'].update("", button_color=GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY1)
            main_window[f'-BUTTONTODOTOMORROWEVENT{GLOBAL_CONTROL_TO_DO_TOMORROW_BUTTON_NUMBER-i}-'].set_right_click_menu(["Menu", ["-"]])

# funkcje kalendarza

def button_cal_pressed(number, if_startup = False):         # po kliknięciu przycisku dnia w kalendarzu zmienia się napis na przycisku oraz data wprowadzana jest do inputu żeby ułatwić dodawanie wydarzeń oraz dzień (napis) zamienia się na nazwę wydarzenia
    button_text = str(main_window[f'-BUTTONCAL{number}-'].get_text())                 # opakowujemy w stringa mimo tego, że już powinno zwracać stringa, ale z jakiegoś powodu czasem jest int i się wywala 2 linijki niżej
    calendar_events = load_calendar_events(GLOBAL_CALENDAR_SAVE_FILE_NAME)         # jak jest włączone wczytywanie ukończonych wydarzeń (historii), to wczytujemy z innego pliku (tylko do pokazywania)
    if button_text != "":                       # jeżeli przycisk jest pustym dniem to nic się nie dzieje
        if button_text.isnumeric() == True:         # jeżeli na przycisku wyświetla się numer dnia w danym momencie
            # wprowadzanie daty do inputu
            month = str(month_word_to_number(main_window['-MONTHTEXT-'].get(), True))
            year = main_window['-YEARTEXT-'].get()
            date = day_number_to_string(button_text)+"."+month+"."+year
            main_window['-INPUTDATE-'].update(date)
            calendar_button_datetime_format_date = calendar_event_date_to_datetime_format_date(date)        # szybka konwersja na datetime.date (patrz calendar.py -> assign_button_dates -> sprawdzanie, czy danego dnia jest dane wydarzenie
            # wyświetlanie nazw wydarzeń z danego dnia
            today_event_list = []
            for ev in calendar_events:
                if calendar_button_datetime_format_date in ev.datetime_format_dates_list and ev.show_on_calendar == True:     # jeżeli data podana na przycisku pokrywa się z datą wydarzenia + jeżeli wydarzenie jest pokazywalne w kalendarzu
                    today_event_list.append(ev)
            if today_event_list != []:
                event_names_string = sort_event_names(today_event_list)
                main_window[f'-BUTTONCAL{number}-'].update(event_names_string)
        else:                                       # jak na przycisku wyświetlają się stringi (hehe) to zamień na numer dnia
            button_dates_numbers = assign_calendar_buttons_dates(gv.calendar_year, gv.calendar_month_number)          # obliczamy to jeszcze raz, bo w międzyczasie mogliśmy zmienić miesiące czy coś, na wszelki wypadek
            # znajdywanie indeksów tablicy button_dates dla danej wartości (numeru) dnia
            w = int((number-1)/7)                   # numer tygodnia to całkowita wartość z dzielenia numeru przycisku;     -1 bo przejście numery->indeksy
            d = (number-1)%7                        # numer tygodnia to modulo 
            main_window[f'-BUTTONCAL{number}-'].update(button_dates_numbers[w][d])

def update_calendar():                  # aktualizuje kalendarz na wybrany miesiąc i rok
    log("Aktualizowanie kalendarza")
    assign_new_calendar_event_id()                                                                              # przypisujemy nowy, wolny numer ID do zmiennej globalnej
    calendar_events = load_calendar_events(GLOBAL_CALENDAR_SAVE_FILE_NAME)                                      # wczytujemy obecne wydarzenia do przetwarzania dalej (lub historię)
    button_dates = assign_calendar_buttons_dates(gv.calendar_year, gv.calendar_month_number)
    button_colors, events_month_array = assign_calendar_buttons_colors(button_dates, calendar_events, gv.calendar_year, gv.calendar_month_number)
    main_window['-MONTHTEXT-'].update(gv.calendar_month_word)
    main_window['-YEARTEXT-'].update(gv.calendar_year)
    for w in range(6):                  # uaktualnia napis oraz kolor na przycisku
        for d in range(7):
            main_window[f'-BUTTONCAL{7*w+d+1}-'].update(text = button_dates[w][d])
            main_window[f'-BUTTONCAL{7*w+d+1}-'].update(image_data = button_colors[w][d])     # button_colors to teraz 2D-lista obrazów(bitów);  image_source nie działa z jakiegoś powodu wtf
                                # ^ pozwala znaleźć numer przycisku za pomocą numeru tygodnia i dnia (o 1 większy niż indeks listy!)
            # if gv.calendar_year == datetime.datetime.now().year and gv.calendar_month_number == datetime.datetime.now().month and button_dates[w][d] == str(datetime.datetime.now().day):        # jak rok, miesiąc i dzień dnia kalendarza się zgadza z dniem dzisiejszym, to robimy obwódkę
            #    main_window[f'-BUTTONCAL{7*w+d+1}-'].update(border_width = 10)
            main_window[f'-BUTTONCAL{7*w+d+1}-'].set_right_click_menu(create_calendar_right_click_menu(events_month_array[w][d]))        # dodanie right_click_menu do każdego z przycisków kalendarza
    
    if gv.calendar_year == gv.current_year and gv.calendar_month_number == gv.current_month_number:
        points = calculate_total_points(read_calendar_events(GLOBAL_CALENDAR_MONTH_COMPLETION_FILE_NAME))           # dla teraźniejszego miesiąca obliczamy punkty na bieżąco
    else:
        points = read_monthly_points()                                                                              # dla któregoś z poprzednich miesięcy odczytujemy punkty z zapisanego pliku za pomocą zmiennych globalnych
    main_window['-MONTHPOINTS-'].update(str(points)+"/"+str(read_record_points())+GLOBAL_CALENDAR_POINTS_SYMBOL)
    calendar_switch_button_text()       # żeby domyślnie były nazwy wydarzeń, a nie numerki dni
    update_calendar_input()             # żeby wyczyścić pole "data"

def update_calendar_input(date=""):             # aktualizuje pola do wpisywania nowego wydarzenia (de facto czyści + opcja automatycznego wpisania daty)
    main_window['-INPUTDATE-'].update(date)

def clear_calendar_input():
    main_window['-INPUTDATE-'].update("")
    main_window['-INPUTDATEEND-'].update("")
    main_window['-INPUTREPEAT-'].update("")
    main_window['-INPUTHOUR1-'].update("")
    main_window['-INPUTHOUR2-'].update("")
    main_window['-INPUTHOUR1-'].update("")
    main_window['-INPUTNAME-'].update("")
    main_window['-INPUTINFO-'].update("")
    main_window['-RADIOIMPORTANCE3-'].update(value=True)
    main_window['-CHECKBOXGOOUT-'].update(value=False)
    main_window['-CHECKBOXDEADLINE-'].update(value=False)
    main_window['-RADIONEUTRAL-'].update(value=True)
    main_window['-CHECKBOXCONSTANT-'].update(value=False)

def add_to_calendar(values):                    # dodaje wydarzenie do kalendarza i automatycznie go aktualizuje
    # ify zabezpieczające przed dodaniem danych, które mogłyby wywołać problemy
    if values['-INPUTNAME-'] == "" or values['-INPUTNAME-'] == " " or values['-INPUTNAME-'] == "\n":
        #sg.popup_notify("Brak nazwy!", fade_in_duration=100, alpha=1, location=(0, 1297))      # dwie super opcje robienia notyfikacji
        #popup_notify("TEST", "TEST")        # tmp
        popup_warning("Brak nazwy wydarzenia!")
        return
    if values['-INPUTDATE-'] == "" and values['-INPUTDATEEND-'] != "":
        popup_warning("Nie można dodać daty zakończenia bez daty rozpoczęcia wydarzenia!\nPodana data zakończenia: "+values['-INPUTDATEEND-'])
        return
    if values['-INPUTHOUR1-'] == "" and values['-INPUTHOUR2-'] != "":
        popup_warning("Nie można dodać godziny zakończenia bez godziny rozpoczęcia wydarzenia!\nPodana godzina zakończenia: "+values['-INPUTHOUR2-'])
        return
    if values['-INPUTDATE-'] != "" and values['-INPUTDATEEND-'] != "" and (calendar_event_date_to_datetime_format_date(values['-INPUTDATE-']) > calendar_event_date_to_datetime_format_date(values['-INPUTDATEEND-'])):
        popup_warning("Data zakończenia wydarzenia jest po dacie rozpoczęcia wydarzenia!\nPodane daty: "+values['-INPUTDATE-']+"   oraz: "+values['-INPUTDATEEND-'])
        return
    if "\n" in values['-INPUTINFO-']:
        popup_warning("W informacji o wydarzeniu nie może być znaków końca linii \"\\n\"!")
        return
    if values['-INPUTDATE-'] == "":
        event, v = popup_warning_confirm("Czy na pewno chcesz dodać wydarzenie bez daty?")
        if event == "-POPUPWARNINGBUTTONNO-":
            return
    if values['-INPUTDATE-'] != "" and (calendar_event_date_to_datetime_format_date(values['-INPUTDATE-']) < datetime.datetime.now().date()):
        event, v = popup_warning_confirm("Czy na pewno chcesz dodać wydarzenie z datą wcześniejszą niż dzisiejsza?\nPodana data: "+values['-INPUTDATE-'])
        if event == "-POPUPWARNINGBUTTONNO-":
            return
    if values['-CHECKBOXCONSTANT-'] == True and values['-INPUTREPEAT-'] != "30" and values['-INPUTREPEAT-'] != "365":           # tutaj muszą być stringi, bo input nie jest jeszcze rzutowany!
        popup_warning("Próbujesz dodać wydarzenie, które jest wydarzeniem stałym = nie jest przekładalne,\nczyli powtarza się co specjalny okres czasu!\nDostępne specjalne wartości powtarzania:\n\u2022 30 - powtarza co miesiąc, wydarzenie będzie zawsze tego samego dnia miesiąca\n\u2022 365 - powtarza co rok, wydarzenie będzie zawsze tego samego dnia i miesiąca w roku\n\nPodany okres powtarzania się: "+values['-INPUTREPEAT-'], auto_close=False)
        return

    # dodawanie do kalendarza
    if values['-RADIOPOSITIVE-'] == True:                           # wartości z radiobuttonów zamieniamy po prostu na inta
        positivity = 1
    elif values['-RADIONEUTRAL-'] == True:
        positivity = 0
    else:
        positivity = -1
    if values['-RADIOIMPORTANCE1-'] == True:
        importance = 1
    elif values['-RADIOIMPORTANCE2-'] == True:
        importance = 2
    elif values['-RADIOIMPORTANCE3-'] == True:
        importance = 3
    else:
        importance = 4
    calendar_event = CalendarEvent(values['-INPUTNAME-'], values['-INPUTDATE-'], values['-INPUTDATEEND-'], values['-INPUTHOUR1-'], values['-INPUTHOUR2-'], values['-INPUTINFO-'], importance, values['-CHECKBOXGOOUT-'], values['-CHECKBOXDEADLINE-'], positivity, values['-INPUTREPEAT-'], values['-CHECKBOXCONSTANT-'], gv.calendar_new_event_id)
    calendar_event.organise_data()      
    calendar_event.write_to_file(GLOBAL_CALENDAR_SAVE_FILE_NAME)                # wpisujemy wydarzenie do pliku z zapisanymi wydarzeniami kalendarza
    calendar_event.write_to_file(GLOBAL_CALENDAR_MONTH_HISTORY_FILE_NAME)             # wpisujemy wydarzenie do pliku z historią kalendarza z tego miesiąca
    id_file = open(get_calendar_file_path(GLOBAL_CALENDAR_NEW_ID_FILE_NAME), "w")                       # zapisujemy id dla następnego wydarzenia
    id_file.write(str(gv.calendar_new_event_id+1))
    id_file.close()
    if calendar_event.datetime_format_date != "" and calendar_event.datetime_format_date == datetime.datetime.now().date():     # dopisanie do pliku z dzisiejszymi wydarzeniami
        calendar_event.write_to_file(GLOBAL_CALENDAR_TODAY_FILE_NAME, append=True, write_if_reminded=True)
    log("Dodano wydarzenie: \""+calendar_event.name+"\" do kalendarza", 2)
    clear_calendar_input()                 # żeby się wyczyściły wszystkie pola do wpisywania wydarzenia
    tmp1, tmp2, gv.calendar_decide_events = manage_past_calendar_events()           # żeby pojawiły się ewentualne minione wydarzenia
    update("calendar manager control")

def calendar_right_click_menu_pressed(event):            # obsługa wybrania którejś pozycji z RCM od kalendarza
    log("Naciśnięto przycisk RCM: "+event)
    # poniższe 3 linijki wyszukują wydarzenie po ID przesłane przez RCM; domyślnie szuka w save_file.txt, ale jeśli nie znajdzie (==None), to przeszukuje jeszcze w pliku historii (bo może być włączony jest tryb przeglądania historii)
    calendar_event = get_calendar_event_by_id(event.split('_')[1], GLOBAL_CALENDAR_SAVE_FILE_NAME)
    if calendar_event == None:      # gdy wydarzenia nie ma w zapisywanych wydarzeniach kalendarza
        calendar_event = get_calendar_event_by_id(event.split('_')[1], get_month_calendar_file_name(gv.calendar_month_number, gv.calendar_year))
    if "RCMDELETE" in event:
        deleted_event_name = delete_calendar_event(event.split('_')[1])      # przekazuje ID wydarzenia wydzielone z klucza do usunięcia
        if calendar_event.date != "" and calendar_event.datetime_format_date == datetime.datetime.now().date():         # usuwanie z dzisiejszych wydarzeń jeżeli data się pokrywa z dzisiejszą
            delete_calendar_event(event.split('_')[1], GLOBAL_CALENDAR_TODAY_FILE_NAME)
        log("Usunięto wydarzenie: \""+deleted_event_name+"\"", 2)
    elif "RCMEDIT" in event:
        popup_event, popup_values = popup_edit_calendar_event(calendar_event)                 # tworzy okno z edycją wydarzenia i zwraca wszystkie wartości
        if popup_event == '-POPUPEDITBUTTONCANCELCALENDAR-':             # jeśli kliknęliśmy anulowanie edycji wydarzenia, to nic nie robimy, wracamy
            log("Anulowano edycję wydarzenia: \""+calendar_event.name+"\"", 2)
            return

        # ify zabezpieczające przed dodaniem danych, które mogłyby wywołać problemy; to samo co 
        if popup_values['-POPUPEDITINPUTNAME-'] == "" or popup_values['-POPUPEDITINPUTNAME-'] == " " or popup_values['-POPUPEDITINPUTNAME-'] == "\n":
            #sg.popup_notify("Brak nazwy!", fade_in_duration=100, alpha=1, location=(0, 1297))      # dwie super opcje robienia notyfikacji
            #popup_notify("TEST", "TEST")        # tmp
            popup_warning("Brak nazwy wydarzenia!")
            return
        if popup_values['-POPUPEDITINPUTDATE-'] == "" and popup_values['-POPUPEDITINPUTDATEEND-'] != "":
            popup_warning("Nie można dodać daty zakończenia bez daty rozpoczęcia wydarzenia!\nPodana data zakończenia: "+popup_values['-POPUPEDITINPUTDATEEND-'])
            return
        if popup_values['-POPUPEDITINPUTHOUR1-'] == "" and popup_values['-POPUPEDITINPUTHOUR2-'] != "":
            popup_warning("Nie można dodać godziny zakończenia bez godziny rozpoczęcia wydarzenia!\nPodana godzina zakończenia: "+popup_values['-POPUPEDITINPUTHOUR2-'])
            return
        if popup_values['-POPUPEDITINPUTDATE-'] != "" and popup_values['-POPUPEDITINPUTDATEEND-'] != "" and (calendar_event_date_to_datetime_format_date(popup_values['-POPUPEDITINPUTDATE-']) > calendar_event_date_to_datetime_format_date(popup_values['-POPUPEDITINPUTDATEEND-'])):
            popup_warning("Data zakończenia wydarzenia jest po dacie rozpoczęcia wydarzenia!\nPodane daty: "+popup_values['-POPUPEDITINPUTDATE-']+"   oraz: "+popup_values['-POPUPEDITINPUTDATEEND-'])
            return
        if "\n" in popup_values['-POPUPEDITINPUTINFO-']:
            popup_warning("W informacji o wydarzeniu nie może być znaków końca linii \"\\n\"!")
            return

        if popup_values['-POPUPEDITINPUTDATE-'] == "":
            event, v = popup_warning_confirm("Czy na pewno chcesz dodać wydarzenie bez daty?")
            if event == "-POPUPWARNINGBUTTONNO-":
                return
        if popup_values['-POPUPEDITINPUTDATE-'] != "" and (calendar_event_date_to_datetime_format_date(popup_values['-POPUPEDITINPUTDATE-']) < datetime.datetime.now().date()):
            event, v = popup_warning_confirm("Czy na pewno chcesz dodać wydarzenie z datą wcześniejszą niż dzisiejsza?\nPodana data: "+popup_values['-POPUPEDITINPUTDATE-'])
            if event == "-POPUPWARNINGBUTTONNO-":
                return
        
        # te same rzeczy co w add_to_calendar, musimy je szybko przerobić, zanim przekażemy do edita
        if popup_values['-POPUPEDITRADIOPOSITIVE-'] == True:                           
            positivity = 1
        if popup_values['-POPUPEDITRADIONEUTRAL-'] == True:
            positivity = 0
        if popup_values['-POPUPEDITRADIONEGATIVE-'] == True:
            positivity = -1
        if popup_values['-POPUPEDITRADIOIMPORTANCE1-'] == True:
            importance = 1
        elif popup_values['-POPUPEDITRADIOIMPORTANCE2-'] == True:
            importance = 2
        elif popup_values['-POPUPEDITRADIOIMPORTANCE3-'] == True:
            importance = 3
        else:
            importance = 4
        if popup_event == "-POPUPEDITBUTTONEDITCALENDAR-":                  # jeżeli zatwierdzono wprowadzenie zmian to edytujemy
            edit_calendar_event(calendar_event, popup_values['-POPUPEDITINPUTNAME-'], popup_values['-POPUPEDITINPUTDATE-'], popup_values['-POPUPEDITINPUTDATEEND-'], popup_values['-POPUPEDITINPUTHOUR1-'], popup_values['-POPUPEDITINPUTHOUR2-'], popup_values['-POPUPEDITINPUTINFO-'], importance, popup_values['-POPUPEDITCHECKBOXGOOUT-'], popup_values['-POPUPEDITCHECKBOXDEADLINE-'], positivity, popup_values['-POPUPEDITINPUTREPEAT-'], popup_values['-POPUPEDITCONSTANT-'])
            log("Zedytowano wydarzenie: \""+calendar_event.name+"\"", 1)                 # ^ używając wartości zwróconych przez popup, edytujemy wydarzenie
            if calendar_event.date != "" and calendar_event.datetime_format_date == datetime.datetime.now().date():         # usuwanie z dzisiejszych wydarzeń starej wersji wydarzenia
                delete_calendar_event(event.split('_')[1], GLOBAL_CALENDAR_TODAY_FILE_NAME)
    elif "RCMINFO" in event:
        tmp = popup_calendar_event_info(calendar_event)
    elif "RCMDONE" in event:
        calendar_event_name = complete_calendar_event(event.split('_')[1])
        if calendar_event.date != "" and calendar_event.datetime_format_date == datetime.datetime.now().date():         # usuwanie z dzisiejszych wydarzeń, z tego pliku zawsze tylko usuwamy, wykonywanie jest robione oprócz tego już linijke wcześniej
            delete_calendar_event(event.split('_')[1], GLOBAL_CALENDAR_TODAY_FILE_NAME)
        log("\u2611 Ukończono wydarzenie: \""+calendar_event_name+"\"!\t+"+str(calendar_event.points)+"\u227C\u2119\u227D", 2)
        if calendar_event.points > GLOBAL_CALENDAR_POINTS_BIG_RANGE_LIMIT:          # odtwarza odpowiedni dźwięk ukończenia wydarzenia i zdobycia punktów
            play_sound(GLOBAL_SOUND_POINTS_GAIN_BIG, 0.15)
        elif calendar_event.points > GLOBAL_CALENDAR_POINTS_MEDIUM_RANGE_LIMIT:
            play_sound(GLOBAL_SOUND_POINTS_GAIN_MEDIUM, 0.15)
        else:
            play_sound(GLOBAL_SOUND_POINTS_GAIN_SMALL, 0.2)
    elif "RCMPRINT" in event:
        tmp = popup_print_calendar_event(calendar_event)
    # czemu to jest tutaj? idealnie to to powinno się wykonywać tylko jak jest edit, delete albo done...
    
    for i in range(len(gv.calendar_decide_events)):                     # jeżeli któreś wydarzenie było minionym wydarzeniem to usuwa je z tej globalnej listy, ech, tragiczny sposób
        if calendar_event.id == gv.calendar_decide_events[i].id:
            del(gv.calendar_decide_events[i])               # podobno działa
            log("Zadecydowano o minionym wydarzeniu: \""+calendar_event.name+"\"")
            tmp1, tmp2, gv.calendar_decide_events = manage_past_calendar_events()          # ponownie rozpatrujemy przeszłe wydarzenia, dzięki temu w panelu kontrolnym może znowu coś się pojawić w minionych wydarzeniach
    update("calendar manager control")

def calendar_switch_button_text():                      # naciska wszystkie guziki w kalendarzu, ale nie printuje tego do loga (no słaba opcja ale nie chce mi się przerabiać reszty)
    #log("Naciśnięto przycisk zamiany tekstu w kalendarzu")         # wywalone na razie, bo to funkcja jest wywoływana przy każdym updacie kalendarza, robi się spam w logach
    for i in range(42):                                 # wymuszamy "kliknięcie" na każdy z przycisków kalendarza, żeby zamienić wszystkie numery dni na nazwy -> funkcja osobna?
        button_cal_pressed(i+1, True)
    update_calendar_input()

# funkcje menedżera

def check_manager_events():                                    # po naciśnięciu czegokolwiek właściwie to chcemy od razu wczystko posortować i wczytać na nowo, czy coś tu jeszcze będzie?
    update_manager()

def update_manager():                                                  # aktualizuje zakładkę z menedżerem
    log("Aktualizowanie menadżera")
    calendar_events = read_calendar_events(GLOBAL_CALENDAR_SAVE_FILE_NAME)
    sort_by = ""
    if values['-CHECKBOXMANAGERSORTID-'] == True:                           # wartości z radiobuttonów zamieniamy po prostu na inta
        sort_by = 1                                             # 1 - wg ID
    if values['-CHECKBOXMANAGERSORTDATE-'] == True:
        sort_by = 2                                             # 2 - wg daty
    if values['-CHECKBOXMANAGERSORTIMPORTANCE-'] == True:
        sort_by = 3                                             # 3 - wg ważności
    if values['-CHECKBOXMANAGERSORTOPTIMALSCORE-'] == True:
        sort_by = 4                                             # 4 - wg algorytmu optymalizacyjnego (to co w control panel)
    sorted_calendar_events = sort_calendar_events(calendar_events, sort_by, values['-CHECKBOXMANAGERGOOUT-'], values['-CHECKBOXMANAGERDEADLINE-'], values['-CHECKBOXMANAGEROTHER-'], values['-CHECKBOXMANAGERANNUAL-'], values['-CHECKBOXMANAGERIMPORTANCY1-'], values['-CHECKBOXMANAGERIMPORTANCY2-'], values['-CHECKBOXMANAGERIMPORTANCY3-'], values['-CHECKBOXMANAGERIMPORTANCY4-'])
    #log(f"Posortowano wydarzenia: -CHECKBOXMANAGER{button_number}-")
    for i in range(GLOBAL_MANAGER_NUMER_OF_EVENT_BUTTONS):                     # rozszerza przyciski na całą szerokość okna, bo przy tworzeniu layoutu to nie chce działać
        main_window[f'-BUTTONMANAGEREVENT{i+1}-'].expand(expand_x = True, expand_row = True)         # I TAK NIE DZIAŁA, CZEMUUUUUU :(
        main_window[f'-BUTTONMANAGEREVENT{i+1}-'].update("")
    main_window.refresh()

    for i in range(len(sorted_calendar_events)):                        # wpisuje wydarzenia do poszczególnych przycisków, data + nazwa + godzina
        #button_string = sorted_calendar_events[i].name+"\n"+sorted_calendar_events[i].date+"\t\t"+sorted_calendar_events[i].hour_start+" - "+sorted_calendar_events[i].hour_end        # opcja dla dwóch rzędów, może się kiedyś przyda
        button_string = ""
        if sorted_calendar_events[i].date == "":
            button_string = "          "            # 10 spacji, miejsce na datę
        button_string = button_string+sorted_calendar_events[i].date+sorted_calendar_events[i].name.center(30)           # centruje nazwę wydarzenia na środku na polu danej liczby spacji
        if sorted_calendar_events[i].hour_start == "":                                                          # formatuje godzinę w zależności od tego czy jest (XD)
            button_string = button_string+"              "      # 14 spacji, miejsce na godziny
        elif sorted_calendar_events[i].hour_start != "" and sorted_calendar_events[i].hour_end == "":           
            button_string = button_string+"     "+sorted_calendar_events[i].hour_start+"    "                       # jak wyżej, ale 5 i 4 spacje, żeby było ładnie
        else:
            button_string = button_string+" "+sorted_calendar_events[i].hour_start+" - "+sorted_calendar_events[i].hour_end
        if i<GLOBAL_MANAGER_NUMER_OF_EVENT_BUTTONS:                                     # wpisuje tylko, jeżeli nie zapełniliśmy już wszystkich pozycji w menedżerze
            main_window[f'-BUTTONMANAGEREVENT{i+1}-'].update(button_string)
            main_window[f'-BUTTONMANAGEREVENT{i+1}-'].update(button_color = sorted_calendar_events[i].color)
            main_window[f'-BUTTONMANAGEREVENT{i+1}-'].set_right_click_menu(create_calendar_right_click_menu([sorted_calendar_events[i]]))        # tworzy RCM
    for i in range(GLOBAL_MANAGER_NUMER_OF_EVENT_BUTTONS):          # "resetowanie" pozostałych pozycji/przycisków, żeby nie miały koloru i RCM
        if i+len(sorted_calendar_events)<GLOBAL_MANAGER_NUMER_OF_EVENT_BUTTONS:
            main_window[f'-BUTTONMANAGEREVENT{i+1+len(sorted_calendar_events)}-'].update("", button_color = GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY1)
            main_window[f'-BUTTONMANAGEREVENT{i+1+len(sorted_calendar_events)}-'].set_right_click_menu(["Menu", ["-"]])

# funkcje monitora

def initialize_monitor_plot():                                      # inicjalizuje zmienne globalne związane z wykresem monitora - przypisuje figure i jakiś dziwny canvasowy obiekt
    gv.monitor_plot_figure = plt.figure(figsize=(6.75, 4))               # używanie tych zmiennych globalnych to jest tragiczny sposób, ale naprawdę nie wiem jak przekazać monitor_figure i figure_canvas_agg do funkcji update_monitor -> rozwiązać to kiedyś !!!!!
    gv.monitor_plot_figure.add_subplot(111)
    #axes = gv.monitor_plot_figure.axes
    #axes[0].plot(gv.monitor_data[1][1])
    gv.figure_canvas_agg = FigureCanvasTkAgg(gv.monitor_plot_figure, main_window['-MONITORCANVAS-'].TKCanvas)
    gv.figure_canvas_agg.draw()
    gv.figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

def update_monitor(add_new_data=True):                                   # aktualizuje pola tekstowe z wartościami odczytanymi z czujników komputera oraz aktualizuje wykres
    log("Aktualizowanie monitora")
    if add_new_data:                                                     # zczytuje nowe informacje z sensorów tylko, gdy add_new_data = True, nie chcemy tego zrobić dla zmiany typu wykresu czy włączania/wyłączania poszczególnych serii danych na wykresie
        cpu_load_total, cpu_temp1, cpu_temp2, gpu_load, gpu_temp1, gpu_temp2, fan_percentage_avg, fan2_percentage, fan3_percentage, fan5_percentage, fan6_percentage, fan2, fan3, fan5, fan6, ram_load, ram_usage = get_advanced_monitor_values()
        # aktualizowanie pól tekstowych z informacjami o temperaturach itd
        main_window["-CHECKBOXMONITORSHOWCPUUSAGE-"].update(text=str('{0:.1f}'.format(cpu_load_total)).rjust(5) + " %")
        main_window["-CHECKBOXMONITORSHOWCPUTEMP-"].update(text=str('{0:.1f}'.format(cpu_temp1)).rjust(5) + "\u00B0C  " + str('{0:.1f}'.format(cpu_temp2)).rjust(5) + "\u00B0C")
        main_window["-CHECKBOXMONITORSHOWGPUUSAGE-"].update(text=str('{0:.1f}'.format(gpu_load)).rjust(5) + " %")
        main_window["-CHECKBOXMONITORSHOWGPUTEMP-"].update(text=str('{0:.1f}'.format(gpu_temp1)).rjust(5) + "\u00B0C  " + str('{0:.1f}'.format(gpu_temp2)).rjust(5) + "\u00B0C")
        main_window["-CHECKBOXMONITORSHOWFANUSAGE-"].update(text=str('{0:.1f}'.format(fan_percentage_avg)).rjust(5) + " %")
        main_window["-CHECKBOXMONITORSHOWFAN2USAGE-"].update(text=str('{0:.1f}'.format(fan2_percentage)).rjust(5) + " %")
        main_window["-CHECKBOXMONITORSHOWFAN2SPEED-"].update(text=str(round(fan2)).rjust(4) + " RPM")
        main_window["-CHECKBOXMONITORSHOWFAN3USAGE-"].update(text=str('{0:.1f}'.format(fan3_percentage)).rjust(5) + " %")
        main_window["-CHECKBOXMONITORSHOWFAN3SPEED-"].update(text=str(round(fan3)).rjust(4) + " RPM")
        main_window["-CHECKBOXMONITORSHOWFAN5USAGE-"].update(text=str('{0:.1f}'.format(fan5_percentage)).rjust(5) + " %")
        main_window["-CHECKBOXMONITORSHOWFAN5SPEED-"].update(text=str(round(fan5)).rjust(4) + " RPM")
        main_window["-CHECKBOXMONITORSHOWFAN6USAGE-"].update(text=str('{0:.1f}'.format(fan6_percentage)).rjust(5) + " %")
        main_window["-CHECKBOXMONITORSHOWFAN6SPEED-"].update(text=str(round(fan6)).rjust(4) + " RPM")
        main_window["-CHECKBOXMONITORSHOWRAMUSAGE-"].update(text=str('{0:.2f}'.format(ram_usage)).rjust(5) + "  /  32 GB  " + str('{0:.1f}'.format(ram_load)).rjust(5)+ " %")
    create_monitor_plot()
    #draw_plot_on_canvas(figure=plt.gcf(), canvas=main_window['-MONITORCANVAS-'].TKCanvas)

def check_monitor_events(event):
    if event == '-RADIOMONITORPLOTTEMPERATURE-':
        gv.monitor_view_mode = "temp"
    elif event == '-RADIOMONITORPLOTUSAGE-':
        gv.monitor_view_mode = "usage"
    elif event == '-RADIOMONITORPLOTFANSPEED-':
        gv.monitor_view_mode = "fan"
    elif event == '-CHECKBOXMONITORSHOWCPUUSAGE-':
        gv.monitor_dict["CPU_usage"] = values['-CHECKBOXMONITORSHOWCPUUSAGE-']
    elif event == '-CHECKBOXMONITORSHOWCPUTEMP-':
        gv.monitor_dict["CPU_temp"] = values['-CHECKBOXMONITORSHOWCPUTEMP-']
    elif event == '-CHECKBOXMONITORSHOWGPUUSAGE-':
        gv.monitor_dict["GPU_usage"] = values['-CHECKBOXMONITORSHOWGPUUSAGE-']
    elif event == '-CHECKBOXMONITORSHOWGPUTEMP-':
        gv.monitor_dict["GPU_temp"] = values['-CHECKBOXMONITORSHOWGPUTEMP-']
    elif event == '-CHECKBOXMONITORSHOWFANUSAGE-':
        gv.monitor_dict["FAN_usage"] = values['-CHECKBOXMONITORSHOWFANUSAGE-']
    elif event == '-CHECKBOXMONITORSHOWFAN2USAGE-':
        gv.monitor_dict["FAN2_usage"] = values['-CHECKBOXMONITORSHOWFAN2USAGE-']
    elif event == '-CHECKBOXMONITORSHOWFAN3USAGE-':
        gv.monitor_dict["FAN3_usage"] = values['-CHECKBOXMONITORSHOWFAN3USAGE-']
    elif event == '-CHECKBOXMONITORSHOWFAN5USAGE-':
        gv.monitor_dict["FAN5_usage"] = values['-CHECKBOXMONITORSHOWFAN5USAGE-']
    elif event == '-CHECKBOXMONITORSHOWFAN6USAGE-':
        gv.monitor_dict["FAN6_usage"] = values['-CHECKBOXMONITORSHOWFAN6USAGE-']
    elif event == '-CHECKBOXMONITORSHOWFAN2SPEED-':
        gv.monitor_dict["FAN2_speed"] = values['-CHECKBOXMONITORSHOWFAN2SPEED-']
    elif event == '-CHECKBOXMONITORSHOWFAN3SPEED-':
        gv.monitor_dict["FAN3_speed"] = values['-CHECKBOXMONITORSHOWFAN3SPEED-']
    elif event == '-CHECKBOXMONITORSHOWFAN5SPEED-':
        gv.monitor_dict["FAN5_speed"] = values['-CHECKBOXMONITORSHOWFAN5SPEED-']
    elif event == '-CHECKBOXMONITORSHOWFAN6SPEED-':
        gv.monitor_dict["FAN6_speed"] = values['-CHECKBOXMONITORSHOWFAN6SPEED-']
    elif event == '-CHECKBOXMONITORSHOWRAMUSAGE-':
        gv.monitor_dict["RAM_usage"] = values['-CHECKBOXMONITORSHOWRAMUSAGE-']
    elif event == '-BUTTONMONITORPRINTSENSORS-':
        popup_print_computer_sensors()
    elif event == '-BUTTONMONITORSAVEDATATOFILE-':
        save_monitor_data()
    update_monitor(add_new_data=False)

def button_monitor_toggle_pressed():                                # tworzy lub usuwa monitor_popup i zwraca go wraz z informacją co to za okno
    if gv.is_monitor_window == False:     # jeśli w nazwie przycisku było "Włącz", znaczy, że popup jest wyłączony i go uruchamiamy
        log("Uruchamianie Monitor Popup", 1)
        main_window['-BUTTONMONITORPOPUPTOGGLE-'].update(button_color=GLOBAL_CONTROL_APP_BUTTON_ON_COLOR)
        new_monitor_window = create_popup_monitor_window()
        w1, h1 = location = sg.Window.get_screen_size()
        w2, h2 = new_monitor_window.current_size_accurate()
        new_monitor_window.move(w1-w2, 0)                           # przesuwa popup w pracy górny róg
        gv.is_monitor_window = True
        schedule.every(1).seconds.do(update_monitor_popup).tag("monitor_popup")     # tworzy joba, który co sekundę będzie aktualizował monitor_popup
        return new_monitor_window, "monitor_popup"                  # zwraca tuple'a
    else:
        log("Zamykanie Monitor Popup", 1)
        main_window['-BUTTONMONITORPOPUPTOGGLE-'].update(button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR)
        schedule.clear("monitor_popup")
        monitor_window.close()
        gv.is_monitor_window = False

def move_monitor_popup(event):                                      # przesuwa okno monitor popupa o 10 pikseli we wskazaną stronę
    w, h = monitor_window.current_location()
    if "LEFT" in event:
        monitor_window.move(w-10, h)
    elif "RIGHT" in event:
        monitor_window.move(w+10, h)
    elif "DOWN" in event:
        monitor_window.move(w, h+10)
    elif "UP" in event:                 # !!! łapie też 'UP' z 'POPUP' XDDDDDDDDD
        monitor_window.move(w, h-10)

def update_monitor_popup():                                         # aktualizuje monitor popup o najnowsze dane z sensorów
    cpu_load, cpu_temp, gpu_load, gpu_temp, fan_load, ram_usage = get_basic_monitor_values()
    monitor_window["-MONITORPOPUPCPULOAD-"].update("CPU: " + str(round(cpu_load)).rjust(2) + " %")
    monitor_window["-MONITORPOPUPCPUTEMP-"].update("     " + str(round(cpu_temp)).rjust(2) + "\u00B0C")
    monitor_window["-MONITORPOPUPGPULOAD-"].update(" GPU: " + str(round(gpu_load)).rjust(2) + " %")
    monitor_window["-MONITORPOPUPGPUTEMP-"].update("      " + str(round(gpu_temp)).rjust(2) + "\u00B0C")
    monitor_window["-MONITORPOPUPFANLOAD-"].update(" FANS:  " + str(round(fan_load)).rjust(2) + " %")
    monitor_window["-MONITORPOPUPRAMUSAGE-"].update(" RAM: " + str('{0:.1f}'.format(ram_usage)).rjust(4) + " GB")

# funkcje media playera

def button_media_player_toggle_pressed():                           # tworzy lub usuwa media_player_window i zwraca go wraz z informacją co to za okno
    if gv.is_media_player_window == False:     # jeśli w nazwie przycisku było "Włącz", znaczy, że popup jest wyłączony i go uruchamiamy
        log("Uruchamianie Media Player Window", 1)
        main_window['-BUTTONMEDIAPLAYERWINDOWTOGGLE-'].update(button_color=GLOBAL_CONTROL_APP_BUTTON_ON_COLOR)
        new_media_player_window = create_media_player_window()
        # w1, h1 = location = sg.Window.get_screen_size()
        # w2, h2 = new_monitor_window.current_size_accurate()
        # new_monitor_window.move(w1-w2, 0)                           # przesuwa popup w pracy górny róg
        gv.is_media_player_window = True
        new_media_player_window['-COLUMNMEDIAPLAYERMENU-'].hide_row()
        new_media_player_window['-BUTTONMEDIAPLAYERMENU-'].update(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_MENU, 50, 50))
        gv.all_songs: list[Song] = []                       # !!! przypisanie typu zmiennej, dzięki temu VSC wie co to jest i podpowiada np pola danej klasy przy pisaniu
        gv.playlist: list[Song] = []
        load_music_library()
        create_playlist()
        return new_media_player_window, "media_player_window"                  # zwraca tuple'a
    else:
        log("Zamykanie Media Player Window", 1)
        main_window['-BUTTONMEDIAPLAYERWINDOWTOGGLE-'].update(button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR)
        # schedule.clear("media_player_window")
        media_player_window.close()
        gv.is_media_player_window = False

def check_media_player_events(event):                             # sprawdzanie dodatkowych eventów media playera
    if event == '-BUTTONMEDIAPLAYERPLAYPAUSESONG-':               # naciśnięty przycisk play/pause
        if gv.is_music_playing:                                     # jeśli muzyka gra, to znaczy, że trzeba ją zapauzować i odwrotnie - wykonywanie odpowiednich funkcji
            pause_song()
            media_player_window['-BUTTONMEDIAPLAYERPLAYPAUSESONG-'].update(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_PLAY, 70, 70))
        else:
            if len(gv.playlist) == 0:
                #media_player_log("W playliście nie ma żadnych utworów!")
                return
            media_player_playbutton_pressed()
            media_player_window["-MEDIAPLAYERTEXTSONGNAME-"].update(gv.playlist[gv.playlist_index].name)
            media_player_window['-BUTTONMEDIAPLAYERPLAYPAUSESONG-'].update(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_PAUSE, 70, 70))
            load_song_info()
    elif event == '-BUTTONMEDIAPLAYERPREVIOUSSONG-':
        play_previous_song()
        reset_media_player()
        load_song_info()
    elif event == '-BUTTONMEDIAPLAYERNEXTSONG-':
        play_next_song()
        reset_media_player()
        load_song_info()
    elif event == '-BUTTONMEDIAPLAYERSTOPSONG-':
        stop_song()
        reset_media_player()
        media_player_window['-BUTTONMEDIAPLAYERPLAYPAUSESONG-'].update(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_PLAY, 70, 70))
    elif event == "-BUTTONMEDIAPLAYERMENU-":
        # print(media_player_window['-MEDIAPLAYERTABGROUP-'].visible)        # czemu własność .visible się nie zmienia gdy ukrywamy rząd? -> zamiast tego używamy zmiennej is_media_player_menu_open
        if gv.is_media_player_menu_open:
            media_player_window['-COLUMNMEDIAPLAYERMENU-'].hide_row()
            media_player_window['-BUTTONMEDIAPLAYERMENU-'].update(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_MENU, 50, 50))
            gv.is_media_player_menu_open = False
        else:
            media_player_window['-COLUMNMEDIAPLAYERMENU-'].unhide_row()
            media_player_window['-BUTTONMEDIAPLAYERMENU-'].update(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_MENU_PRESSED, 50, 50))
            gv.is_media_player_menu_open = True
    elif event == "-BUTTONMEDIAPLAYERSHUFFLE-":
        if gv.is_media_player_shuffle:
            media_player_window['-BUTTONMEDIAPLAYERSHUFFLE-'].update(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_SHUFFLE, 30, 30))
            gv.is_media_player_shuffle = False
        else:
            media_player_window['-BUTTONMEDIAPLAYERSHUFFLE-'].update(image_data=get_media_player_image_byte_value(GLOBAL_MEDIA_PLAYER_BUTTON_IMAGE_SHUFFLE_PRESSED, 30, 30))
            gv.is_media_player_shuffle = True
    elif event == '-BUTTONMEDIAPLAYERUPDATELIBRARY-':                  # kliknięcie przycisku "Zaktualizuj bibliotekę", wykonuje zadania w wątkach
        media_player_log("Sprawdzanie playlisty...")
        media_player_window.perform_long_operation(check_playlist_for_downloading, "-THREADEDMEDIAPLAYERCHECKPLAYLIST-")         # tworzy osobny wątek, w którym wykonuje funkcję, wykonanie funkcji jest reprezentowane przez zwrot eventu o podanej nazwie
    elif event == '-BUTTONMEDIAPLAYERUPDATESONGINFO-':
        update_song_info_button_pressed(values)
    elif "CHECKBOXMEDIAPLAYER" in event:
        if gv.current_song is None:
            popup_info("Brak wczytanej piosenki!", auto_close=True)
            return
        if event == "-CHECKBOXMEDIAPLAYERISCOVER-":
            gv.current_song.is_cover = values["-CHECKBOXMEDIAPLAYERISCOVER-"]
        elif event == "-CHECKBOXMEDIAPLAYERISINSTRUMENTAL-":
            gv.current_song.is_instrumental = values["-CHECKBOXMEDIAPLAYERISINSTRUMENTAL-"]
        elif event == "-CHECKBOXMEDIAPLAYERISFROMMOVIE-":
            gv.current_song.is_from_movie = values["-CHECKBOXMEDIAPLAYERISFROMMOVIE-"]
        elif event == "-CHECKBOXMEDIAPLAYERISFROMGAME-":
            gv.current_song.is_from_game = values["-CHECKBOXMEDIAPLAYERISFROMGAME-"]
        elif event == "-CHECKBOXMEDIAPLAYERISMEME-":
            gv.current_song.is_meme = values["-CHECKBOXMEDIAPLAYERISMEME-"]
        elif event == "-CHECKBOXMEDIAPLAYERISCRINGE-":
            gv.current_song.is_cringe = values["-CHECKBOXMEDIAPLAYERISCRINGE-"]
        elif event == "-CHECKBOXMEDIAPLAYERISLYRICS-":
            gv.current_song.is_lyrics_approved = values["-CHECKBOXMEDIAPLAYERISLYRICS-"]
        elif event == "-CHECKBOXMEDIAPLAYERISLYRICSSYNCHRONIZED-":
            gv.current_song.is_lyrics_synchronized = values["-CHECKBOXMEDIAPLAYERISLYRICSSYNCHRONIZED-"]
        elif event == "-CHECKBOXMEDIAPLAYERISLYRICSTRANSLATED-":
            gv.current_song.is_lyrics_translated_approved = values["-CHECKBOXMEDIAPLAYERISLYRICSTRANSLATED-"]
        elif event == "-CHECKBOXMEDIAPLAYERISLYRICSROMANIZED-":
            gv.current_song.is_lyrics_romanized_approved = values["-CHECKBOXMEDIAPLAYERISLYRICSROMANIZED-"]
        gv.current_song.update_info()
        load_song_info()
    elif event == "-BUTTONMEDIAPLAYERUPLOADLYRICS-":
        popup_upload_lyrics(lyrics_version="lyrics", background_color=GLOBAL_POPUP_COLOR)
    elif event == "-THREADEDMEDIAPLAYERCHECKPLAYLIST-":
        new_videos_list, new_videos_string_names, playlist_title, playlist_length, new_videos_number = values[event]    # dla eventu zakończenia wątku rozpatrywana jest ta część, wartości zwrócone przez funkcję odbieramy za pomocą values[event]
        media_player_log("Sprawdzono playlistę")
        event, v = popup_confirm(message1="Przeszukano playlistę "+playlist_title+" ("+str(playlist_length)+" utworów)\nZnaleziono "+str(new_videos_number)+" nowych utworów. Czy chcesz je pobrać?\nPoniżej lista nowych utworów:\n", message2=new_videos_string_names, title="BATI Media Player")
        if event == "-POPUPWARNINGBUTTONNO-":
            return
        download_playlist(new_videos_list)
        create_playlist()

def media_player_tick_events():                                     # funkcje, które są wykonywane co każdy tick programu (o ile funkcja ta zostanie włączona)
    update_media_player_window()

def update_media_player_window():                                   # wykonywana przy każdym ticku programu, uaktualnia pasek i czas piosenki, w przyszłości będzie też odpowiadała za animacje podczas odtwarzania
    gv.time_since_song_start = pygame_time.get_ticks()
    media_player_window["-PROGRESSBARSONG-"].update(current_count = (gv.time_since_song_start - gv.time_paused)/1000, max=gv.current_song.length_sec)
    time = divmod((gv.time_since_song_start - gv.time_paused)//1000, 60)                    # nieużywane, bo bierzemy zmienną bezpośrednio z klasy;        # jako że czas liczymy w sekundach, to musimy to przekonwertować na minuty i sekundy
    media_player_window["-TEXTSONGTIME-"].update('{:02d}:{:02d} / {:0>5}'.format(*time, gv.current_song.length))      # formatujemy wyświetlanie w taki sposób, żeby były 2 miejsca na minuty i 2 na sekundy dla czasu trwania piosenki; czas całkowity jest już z góry narzucony

def load_song_info():                                               # wczytuje atrybuty utworu do zakładki Info w BMP, można je tam zmienić
    media_player_window["-INPUTMEDIAPLAYERARTIST-"].update(gv.current_song.artist)
    media_player_window["-INPUTMEDIAPLAYERTITLE-"].update(gv.current_song.title)
    media_player_window["-INPUTMEDIAPLAYERCOVERARTIST-"].update(gv.current_song.cover_artist)
    media_player_window["-INPUTMEDIAPLAYERORIGIN-"].update(gv.current_song.origin)
    media_player_window["-SLIDERMEDIAPLAYERVOLUME-"].update(gv.current_song.volume)
    if len(gv.current_song.genre)==0:                                       # łączenie wszystkich pozycji z listy i wypisywanie gatunków po przecinku
        media_player_window["-INPUTMEDIAPLAYERGENRE-"].update("")
    elif len(gv.current_song.genre)==1:
        media_player_window["-INPUTMEDIAPLAYERGENRE-"].update(gv.current_song.genre[0])
    else:
        genre_string = gv.current_song.genre[0]
        for i in range(len(gv.current_song.genre)-1):
            genre_string = genre_string + ", " + gv.current_song.genre[i+1]
        media_player_window["-INPUTMEDIAPLAYERGENRE-"].update(genre_string)
    if len(gv.current_song.vibe)==0:
        media_player_window["-INPUTMEDIAPLAYERVIBE-"].update("")
    elif len(gv.current_song.vibe)==1:
        media_player_window["-INPUTMEDIAPLAYERVIBE-"].update(gv.current_song.vibe[0])
    else:
        vibe_string = gv.current_song.vibe[0]
        for i in range(len(gv.current_song.vibe)-1):
            vibe_string = vibe_string + ", " + gv.current_song.vibe[i+1]
        media_player_window["-INPUTMEDIAPLAYERVIBE-"].update(vibe_string)
    if len(gv.current_song.language)==0:
        media_player_window["-INPUTMEDIAPLAYERLANGUAGE-"].update("")
    elif len(gv.current_song.language)==1:
        media_player_window["-INPUTMEDIAPLAYERLANGUAGE-"].update(gv.current_song.language[0])
    else:
        language_string = gv.current_song.language[0]
        for i in range(len(gv.current_song.language)-1):
            language_string = language_string + ", " + gv.current_song.language[i+1]
        media_player_window["-INPUTMEDIAPLAYERLANGUAGE-"].update(language_string)
    if gv.current_song.is_cover is None:        # jeśli wartość nie jest jeszcze przypisana (nowa piosenka), napis będzie czerwony - dopiero kliknięcie checkboxa przynajmniej raz nadpisze wartość i zlikwiduje czerwony kolor
        media_player_window["-CHECKBOXMEDIAPLAYERISCOVER-"].update(False, text_color=GLOBAL_MEDIA_PLAYER_UNASSIGNED_ATTRIBUTE_COLOR)
    else:
        media_player_window["-CHECKBOXMEDIAPLAYERISCOVER-"].update(gv.current_song.is_cover, text_color=GLOBAL_MEDIA_PLAYER_ASSIGNED_ATTRIBUTE_COLOR)
    if gv.current_song.is_instrumental is None:
        media_player_window["-CHECKBOXMEDIAPLAYERISINSTRUMENTAL-"].update(False, text_color=GLOBAL_MEDIA_PLAYER_UNASSIGNED_ATTRIBUTE_COLOR)
    else:
        media_player_window["-CHECKBOXMEDIAPLAYERISINSTRUMENTAL-"].update(gv.current_song.is_instrumental, text_color=GLOBAL_MEDIA_PLAYER_ASSIGNED_ATTRIBUTE_COLOR)
    if gv.current_song.is_meme is None:
        media_player_window["-CHECKBOXMEDIAPLAYERISMEME-"].update(False, text_color=GLOBAL_MEDIA_PLAYER_UNASSIGNED_ATTRIBUTE_COLOR)
    else:
        media_player_window["-CHECKBOXMEDIAPLAYERISMEME-"].update(gv.current_song.is_meme, text_color=GLOBAL_MEDIA_PLAYER_ASSIGNED_ATTRIBUTE_COLOR)
    if gv.current_song.is_from_movie is None:
        media_player_window["-CHECKBOXMEDIAPLAYERISFROMMOVIE-"].update(False, text_color=GLOBAL_MEDIA_PLAYER_UNASSIGNED_ATTRIBUTE_COLOR)
    else:
        media_player_window["-CHECKBOXMEDIAPLAYERISFROMMOVIE-"].update(gv.current_song.is_from_movie, text_color=GLOBAL_MEDIA_PLAYER_ASSIGNED_ATTRIBUTE_COLOR)
    if gv.current_song.is_from_game is None:
        media_player_window["-CHECKBOXMEDIAPLAYERISFROMGAME-"].update(False, text_color=GLOBAL_MEDIA_PLAYER_UNASSIGNED_ATTRIBUTE_COLOR)
    else:
        media_player_window["-CHECKBOXMEDIAPLAYERISFROMGAME-"].update(gv.current_song.is_from_game, text_color=GLOBAL_MEDIA_PLAYER_ASSIGNED_ATTRIBUTE_COLOR)
    if gv.current_song.is_cringe is None:
        media_player_window["-CHECKBOXMEDIAPLAYERISCRINGE-"].update(False, text_color=GLOBAL_MEDIA_PLAYER_UNASSIGNED_ATTRIBUTE_COLOR)
    else:
        media_player_window["-CHECKBOXMEDIAPLAYERISCRINGE-"].update(gv.current_song.is_cringe, text_color=GLOBAL_MEDIA_PLAYER_ASSIGNED_ATTRIBUTE_COLOR)
    media_player_window["-CHECKBOXMEDIAPLAYERISLYRICS-"].update(gv.current_song.is_lyrics_approved)
    media_player_window["-CHECKBOXMEDIAPLAYERISLYRICSTRANSLATED-"].update(gv.current_song.is_lyrics_translated_approved)
    media_player_window["-CHECKBOXMEDIAPLAYERISLYRICSROMANIZED-"].update(gv.current_song.is_lyrics_romanized_approved)
    media_player_window["-CHECKBOXMEDIAPLAYERISLYRICSSYNCHRONIZED-"].update(gv.current_song.is_lyrics_synchronized_approved)

def update_song_info_button_pressed(values):                        # aktualizowanie atrybutów utworu, wszytkich na raz o wartości wpisane w odpowiednich polach
    if gv.current_song is None:
        popup_info("Brak załadowanej piosenki!")
        return
    event, v = popup_confirm("Czy na pewno chcesz nadpisać wszystkie atrybuty piosenki:\n"+str(gv.current_song)+" ?", "Przypisane zostaną tylko atrybuty, które nie są zmiennymi logicznymi. Zmienne logiczne aktualizują się automatycznie po kliknęciu.", "Bati Media Player")
    if event == "-POPUPWARNINGBUTTONNO-":
        return
    # booleany są przypisywane w odpowiednich listenerach, żeby nie przypisywać niechcący wartości, która powinna być None (bo jest jeszcze nie potwierdzona), tutaj są wszystkie pozostałe
    gv.current_song.artist = values["-INPUTMEDIAPLAYERARTIST-"]
    gv.current_song.title = values["-INPUTMEDIAPLAYERTITLE-"]
    gv.current_song.cover_artist = values["-INPUTMEDIAPLAYERCOVERARTIST-"]
    gv.current_song.origin = values["-INPUTMEDIAPLAYERORIGIN-"]
    gv.current_song.volume = int(values["-SLIDERMEDIAPLAYERVOLUME-"])
    gv.current_song.genre = values["-INPUTMEDIAPLAYERGENRE-"].split(", ")
    gv.current_song.vibe = values["-INPUTMEDIAPLAYERVIBE-"].split(", ")
    gv.current_song.language = values["-INPUTMEDIAPLAYERLANGUAGE-"].split(", ")
    gv.current_song.name = gv.current_song.artist+" - "+gv.current_song.title
    gv.current_song.full_name = gv.current_song.name
    if gv.current_song.origin is not None:
        gv.current_song.full_name = gv.current_song.full_name + " (from " + str(gv.current_song.origin) + ")"
    if gv.current_song.is_cover:
        gv.current_song.full_name = gv.current_song.full_name + " [cover by " + str(gv.current_song.cover_artist) + "]"
    gv.current_song.update_info()
    media_player_log("Zaktualizowano informacje o utworze "+gv.current_song.name)

def reset_media_player():
    media_player_window["-MEDIAPLAYERTEXTSONGNAME-"].update(gv.current_song.name)
    media_player_window["-PROGRESSBARSONG-"].update(current_count = 0, max=gv.current_song.length_sec)
    media_player_window["-TEXTSONGTIME-"].update('00:00 / {:0>5}'.format(gv.current_song.length))

def create_playlist():                          # ???
    gv.playlist = gv.all_songs
    # shuffling, filtering...
    gv.playlist_index = 0
    if len(gv.playlist) == 0:
        #media_player_log("W playliście nie ma żadnych utworów!")
        return
    gv.current_song = gv.playlist[0]

def download_playlist(new_videos_list: list[dict]):                            # aktualizuje bibliotekę pobranych utworów - w podanym argumencie przekazywana jest lista nowych utworów, które nie są pobrane (tzn. ich linków nie ma w pliku downloaded_videos_URLs.txt)
    length = len(new_videos_list)
    for i, video in enumerate(new_videos_list):                    
        # for key in video.keys():
        #     print(key, video[key])
        media_player_log("Pobieranie utworu " +str(i+1)+" / "+str(length)+": "+video["uploader"]+ " - " + video["title"])
        media_player_window.refresh()
        download_song(video)
    media_player_log("Wczytywanie nowej biblioteki...")
    load_music_library()
    media_player_log("Ukończono pobieranie utworów!")

def popup_upload_lyrics(lyrics_version, background_color):
    scrollbar_layout = [
        [sg.Multiline('', key='-MEDIAPLAYERMULTILINELYRICS-', expand_x=True, expand_y=True)]
    ]
    file_dialog_layout = [
        #[sg.Column(scrollbar_layout, scrollable=True, vertical_scroll_only=True, size=(500, 700), size_subsample_height = 10, expand_x=True)],
        [sg.Multiline('', key='-MEDIAPLAYERMULTILINELYRICS-', size=(50, 50), expand_x=True, expand_y=True)],
        [sg.Push(background_color=background_color), sg.FileBrowse('Wczytaj z pliku', key="-WCZYTAJPYTANIE-", size=(10, 2), file_types=(("Text Files", "*.txt"), ("All Files", "*.*"))), sg.Button('Pobierz z genius.com', bind_return_key=True, size=(10, 2)), sg.Push(background_color=background_color)],
        [sg.Push(background_color=background_color), sg.Button('Ok', bind_return_key=True, size=(3, 1)), sg.Button('Cancel', size=(6, 1)), sg.Push(background_color=background_color)]
    ]
    return sg.Window('Filename Chooser With History', file_dialog_layout, finalize=True, background_color=background_color).read(close=True)

def media_player_log(text):
    media_player_window["-MEDIAPLAYERLOGTEXT-"].update(text)

# funkcje log'a

# type=0 -> informacja do loga o poszczególnych procesach programu, nieistotna dla użytkownika
# type=1 -> informacja o akcji użytkownika, również zapisywana a logach, nieistotna dla użytkownika
# type=2 -> zwykła wiadomość potwierdzająca zrobienie czegoś lub informująca o czymś, wyświetlana na log_buttonie
# type=3 -> info o błędzie;             dodać warninga?

def log(text, type=0):                      # zajmuje się zarządzaniem logami
    if type>=3:
        gv.log_string = gv.log_string+text+"\n"
    if type>=2:                             
        main_window['-BUTTONLOG-'].update(text)             # printuje komunikaty istotne dla użytkownika na log buttonie - dolnym pasku
        main_window['-MULTILINELOG-'].update(wrap_log_panel(text), append = True)        # dodawanie linijki do loga - panelu
    if type>=0:
        file = open(get_log_file_path(GLOBAL_LOG_FILE_NAME), "a", encoding='utf-8')        # zapisywanie linijki do pliku z logami
        file.write(wrap_log_file(text, type))
        file.close()

def wrap_log_file(text, type):                       # przygotowuje loga do bycia wyświetlonym w log_panelu (w programie, w zakładce log)
    if type==0:                                 # dopisywanie prefixów odróżniających konkretne typy wiadomości i dodawanie końca linii
        text = str(datetime.datetime.now().strftime("%H:%M:%S"))+"\t"+"Log:\t\t\t\t"+text+"\n"
    elif type==1:
        text = str(datetime.datetime.now().strftime("%H:%M:%S"))+"\t"+"Action:\t\t"+text+"\n"
    elif type==2:
        text = str(datetime.datetime.now().strftime("%H:%M:%S"))+"\t"+"Info:\t"+text+"\n"
    elif type==3:
        text = text+"\n"
    return text

def wrap_log_panel(text):
    return str(datetime.datetime.now().strftime("%H:%M:%S"))+"\t"+text+"\n"

# funkcje dodatkowe

def things_to_do_only_once_after_opening_program():     # specjalna funkcja (oby tylko tymczasowa), której zadaniem jest zrobienie pewnych rzeczy od razu po utworzeniu okna, które nie mogły być zrobione wcześniej, a które nie wymagają żadnego eventu
    log_file = open(get_log_file_path(GLOBAL_LOG_FILE_NAME), "w", encoding='utf-8')     # szybkie czyszczenie pliku z logami
    log_file.close()
    log("BATI v. "+GLOBAL_BATI_VERSION+"   "+str(datetime.datetime.now()), 3)      # PRZED TYM NIE MOŻNA ROBIĆ NIC Z OKNEM!!!
    mixer.init()
    if GLOBAL_IS_DEV_VERSION == False:
        if random() < 0.99:
            play_sound(GLOBAL_SOUND_START_UP, 0.25)
        else:
            play_sound(GLOBAL_SOUND_START_UP_EARRAPE, 0.03)
    log("Uruchamienie BATIego...", 2)
    log("Uruchamianie kalendarza")
    update_calendar()
    log("Uruchomianie menedżera")
    update_manager()                   
    #update_control()                   # nie może tutaj tego być, bo hardware monitor nie jest jeszcze zainicjowany
    #log("Uruchomiono panel kontrolny")
    log("Uporządkowywanie przedawnionych wydarzeń w kalendarzu")
    postponed_events, deleted_events, decide_events = manage_past_calendar_events()             # z tej części większość kodu można przenieść do manage_past_calendar_events i żeby zwracało stringa do loga od razu
    if postponed_events != []:
        string = ""
        for event in postponed_events:
            string = string+" "+event.name+" "+str(event.id)+","
        log("Przesunięto następujące wydarzenia:"+string)
    if deleted_events != []:
        string = ""
        for event in deleted_events:
            string = string+" "+event.name+" "+str(event.id)+","
        log("Usunięto następujące wydarzenia:"+string)
    gv.calendar_decide_events = decide_events                                       # przypisujemy minione wydarzenia do zadecydowania do zmiennej globalnej
    log("Wczytywanie dzisiejszych wydarzeń")
    todays_events = get_todays_events(GLOBAL_CALENDAR_SAVE_FILE_NAME)                             # wczytywanie dzisiejszych wydarzeń z pliku i zapisywanie ich do pliku z dzisiejszymi wydarzeniami
    today_file = open(get_calendar_file_path(GLOBAL_CALENDAR_TODAY_FILE_NAME), "w", encoding='utf-8')       # UWAGA!!! szybkie wyczyszczenie pliku z dzisiejszymi wydarzeniami; powinno być OK nawet jak program został zamknięty w ciągu dnia, bo linijka wyżej i tak przeszukuje cały plik calendar_save.txt
    today_file.close()
    for event in todays_events:
        event.write_to_file(GLOBAL_CALENDAR_TODAY_FILE_NAME, append=True, write_if_reminded=True)       # nadpisuje wydarzenia z poprzedniego dnia !!!; w pozostałych użyciach tej funkcji zawsze append=True
    previous_month_file_name = get_month_calendar_file_name(*get_previous_month(gv.current_month_number, gv.current_year), is_completion=True)         
    if os.path.exists(GLOBAL_CALENDAR_TEXT_FILES_FOLDER_PATH+previous_month_file_name) == False:                     # sprawdza, czy jest nowy miesiąc i czy trzeba przenieść ukończone wydarzenia do osobnego pliku; jeśli nie ma pliku z poprzednim miesiącem, to znaczy że jest nowy miesiąc
        log("Wykryto nowy miesiąc! Tworzenie plików z wydarzeniami dla poprzedniego miesiąca")
        calendar_events = read_calendar_events(GLOBAL_CALENDAR_MONTH_COMPLETION_FILE_NAME)
        points = calculate_total_points(calendar_events)
        write_monthly_points_to_file(calendar_events, points)                                           # przed przenoszeniem wydarzeń podlicza punkty i dopisuje je do pliku z comiesięcznymi punktami
        if (points > read_record_points()):                                                             # jak jest pobity rekord punktów to zapisuje je w pliku z rekordem
            write_points_record_to_file(points, *get_previous_month(gv.current_month_number, gv.current_year))
        move_month_events(GLOBAL_CALENDAR_MONTH_COMPLETION_FILE_NAME, previous_month_file_name)         # dodawanie wykonanych wydarzeń;
        move_month_events(GLOBAL_CALENDAR_MONTH_HISTORY_FILE_NAME, GLOBAL_CALENDAR_HISTORY_FILE_NAME)         # dodawanie wydarzeń z historii do wspólnego pliku, dzielenie na miesiące nie ma sensu
        log("Utworzono pliki z wydarzeniami dla poprzedniego miesiąca")
    log("Inicjalizowanie połączenia z podzespołami komputera")
    initialize_computer_sensors()                                                                       # inicjalizowanie zmiennej globalnej z odczytami z podzespołów komputera
    initialize_monitor_plot()
    log("Ustawianie schedulerów")
    schedule.every(1).minutes.do(check_periodic_events).tag("periodic_events")                          # ustala cominutowe wydarzenie - sprawdzanie szeregu różnych rzeczy
    log("Uruchamianie panelu kontrolnego")
    update("calendar manager monitor control")
    log("BATI v."+GLOBAL_BATI_VERSION+" jest gotowy :)", 2)


### MAIN CODE ###

if __name__ == "__main__":
    gv.initialize()                     # inicjalizuje zmienne globalne
    if GLOBAL_IS_DEV_VERSION == False and is_bati_running() == True:            # jeśli wersja nie jest wersją developerską i jeśli BATI jest już włączony to wyświetlamy komunikat i w przypadku decyzji użytkownika zamykamy instancję
        gv.log_string = gv.log_string+"SYSTEM: BATI v."+GLOBAL_BATI_VERSION+" jest już otwarty. Anulowanie włączania programu.\n"
        gv.log_string = gv.log_string+'SYSTEM: Jeśli jesteś pewny, że program jest wyłączony, sprawdź plik "is_Bati_running.txt" w plikach obecnej wersji -> powinna być wartość "no".\n'
        event_if_continue, v = popup_warning_confirm('Według plików programu BATI jest już włączony.\n Czy kontynuować włączanie mimo to?')
        if event_if_continue ==  "-POPUPWARNINGBUTTONNO-":                              # jeśli wykryto wartość "yes" zmiennej is_Bati_running, zadajemy pytanie, czy na pewno chcemy otworzyć program; jeśli nie, to automatycznie skrypt się zatrzyma
            sys_exit(0)
    # sg.main()                          # otwiera panel PySimpleGUI, odkomentować dla sprawdzenia różnych ciekawych rozwiązań
    try:
        update_is_bati_running("yes")                                                       # blok poleceń do wykonania na początku programu - no fajnie fajnie, ale czemu to jest tutaj, a nie w funkcji things_to_do_only_once_after_opening_program() ???
        calendar_events = read_calendar_events(GLOBAL_CALENDAR_SAVE_FILE_NAME)
        button_dates = assign_calendar_buttons_dates()
        button_colors = assign_calendar_buttons_colors(button_dates, calendar_events)
        main_window = create_main_window(GLOBAL_THEME)
        event, values = main_window.read(1)                     # do testowania można tutaj wstawić np 2000, żeby zdążyć zobaczyć co się dzieje przed ewentualnym errorem
        things_to_do_only_once_after_opening_program()          # PRZED TYM NIE MOŻNA ROBIĆ NIC Z OKNEM, NP. PRINTOWAĆ LOGÓW
        #print(main_window.current_size_accurate())
        while True:                                     # głowna pętla funkcjonowania okna z eventami
            activated_window, event, values = sg.read_all_windows(timeout=100)              # automatycznie odświeża pętlę co sekundę i zczytuje wszystkie okna
            # if event != "__TIMEOUT__":                        # timeout teraz w ogóle nie funkcjonuje
            #     check_timeout_events()
            if event == None:                                   # !!!!!!!!!!! USUNĄĆ TEGO IFA JAK WYJDZIE PySimpleGUI 5 (Typek pisał że się tym zajmie PO tym jak wyjdzie nowa wersja)
                log("Zamykanie BATIego...", 2)
                break
            if event != "__TIMEOUT__" and event != None and event != '-WINDOW CLOSE ATTEMPTED-':        # jeśli event nie jest timeoutem i jeśli nie jest None'm to znaczy że coś kliknęliśmy i sprawdzamy co to było
                returned_value = check_for_event(event)         # sprawdza co to za input i wykonuje odpowiednią zagnieżdżoną funkcję; może też zwracać nowo utworzone okno
                if returned_value != None:                      # jeśli ta wartość nie jest None'm, to znaczy, że zwrócono nowoutworzone okno
                    new_window, which_window = returned_value   # returned_value to tuple, więc go odpakowujemy
                    if which_window == "monitor_popup":         # sprawdza, jakie okno zostało teraz utworzone i przypisuje nowe okno do odpowiedniej zmiennej, ta zmienna będzie teraz używana jako referencja do tego okna w całym tym pliku
                        monitor_window = new_window
                    elif which_window == "media_player_window":
                        media_player_window = new_window
            elif event == '-WINDOW CLOSE ATTEMPTED-':           # !!!!!!!! UWAGA! NA RAZIE DZIAŁA TYLKO NONE, TO DRUGIE NIE JEST JESZCZE ZAIMPLEMENTOWANE -> SPRAWDZAĆ NA GITHUBIE KIEDY WYJDZIE PYSIMPLEGUI 5.0!!!!  naciśnięcie przycisku zamykania okna (event jest dla kontroli, by nie przerwała się żadna ważna operacja)
                log("Zamykanie BATIego...", 2)
                break
            tick_events()                                       # rzeczy wykonywana ZAWSZE przy KAŻDYM TICKU lub evencie
            schedule.run_pending()                              # w tym momencie sprawdza, czy nie nadszedł czas, żeby odpalić check_for_perdiodic_events()
        if GLOBAL_IS_DEV_VERSION == False:
            play_sound(GLOBAL_SOUND_SHUT_DOWN, 0.25)
    except Exception as e:
        try:
            play_sound(GLOBAL_SOUND_ERROR, 0.2)                 # w tej sekcji infomacje o błędzie próbujemy wyświetlać zarówno w log_buttonie, jak i zapisać do log_stringa i potem do pliku; oraz jeszcze print w konsoli, jeśli to wersja DEV
            log("ERROR!", 3)
            log("Coś się zepsuło...", 3)
            # gv.log_string = gv.log_string+"BATI wziął umarł. Oto informacje, które mogą być przydatne:\n\n"
            log("Poniżej coś, co może się przydać:", 3)
            error = str(e)              # z jakiegoś powodu, jeśli się nie zrzutuje tego na stringa to poniższa linijka się wywala
            log(error, 3)
            log("TRACEBACK:", 3)
            tb = traceback.format_exc()
            log(str(tb), 3)
            print("ERROR:", error)
            print(tb)
            popup_error(error)
        except Exception as e1:
            print(str(e1))
            gv.log_string = gv.log_string+"SYSTEM: Nie udało się wykonać czynności awaryjnych. Program abort...\n"
        crash_log_file = open(GLOBAL_CRASH_LOG_FILE_NAME, "w", encoding='utf-8')
        crash_log_file.write(gv.log_string)     # zapisuje wszystkie logi do pliku crash_log.txt
        crash_log_file.close()
    update_is_bati_running("no")            # zmienia zmienną określającą, czy Bati jest uruchomiony
    if gv.is_monitor_window:                # zamyka monitor_popup, jeśli jest nadal włączony
        print("Zamykam monitora")
        monitor_window.close()
    main_window.close()                     # zamyka główne okno i kończy cały program