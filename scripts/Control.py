from Manager import *
from Monitor import *
from Media_Player import *


def create_control_layout(theme):                                       # tworzy layout panelu kontrolnego
    # control_tab layout, czyli zakładka kontrolna (pierwsza)
    avatar_col = sg.Column([[sg.Image(get_avatar_byte_value(GLOBAL_AVATAR_DEFAULT, 200, 200))]])
    # avatar_col = sg.Column([[sg.Image('avatars/EZY.png', size=(100, 100))]])                  # opcja alternatywna bez pięciu linijek powyżej, zachować aż do zrobienia funkcjonalnego awatara, na wszelki wypadek

    # potem sie może przyda

    sys_monitor_col = sg.Column([
        [sg.Text("CPU: XX %", key="-CONTROLCPULOAD-"), sg.Text(" GPU: XX %", key="-CONTROLGPULOAD-"), sg.Text(" FANS:  XX %", key="-CONTROLFANLOAD-")],
        [sg.Text("     XX\u00B0C", key="-CONTROLCPUTEMP-"), sg.Text("      XX\u00B0C", key="-CONTROLGPUTEMP-"), sg.Text(" RAM: XXXX GB", key="-CONTROLRAMUSAGE-")],
    ], expand_x=True)

    control_todo_buttons_layout = []
    for i in range(GLOBAL_CONTROL_TO_DO_BUTTON_NUMBER):
        row = []
        row.append(sg.Button("", key=f'-BUTTONTODOEVENT{i+1}-', expand_x=True))
        control_todo_buttons_layout.append(row)

    control_decide_past_buttons_layout = []
    for i in range(GLOBAL_CONTROL_DECIDE_PAST_BUTTON_NUMBER):
        row = []
        row.append(sg.Button("", key=f'-BUTTONDECIDEEVENT{i+1}-', expand_x=True))
        control_decide_past_buttons_layout.append(row)
    
    control_todo_side_buttons_layout = []
    for i in range(GLOBAL_CONTROL_TO_DO_SIDE_BUTTON_NUMBER):
        row = []
        row.append(sg.Button("", key=f'-BUTTONTODOSIDEEVENT{i+1}-', expand_x=True))
        control_todo_side_buttons_layout.append(row)
    
    control_todo_tomorrow_buttons_layout = []
    for i in range(GLOBAL_CONTROL_TO_DO_TOMORROW_BUTTON_NUMBER):
        row = []
        row.append(sg.Button("", key=f'-BUTTONTODOTOMORROWEVENT{i+1}-', expand_x=True))
        control_todo_tomorrow_buttons_layout.append(row)

    to_do_col = sg.Column([
        [sg.Text("Do zrobienia dzisiaj:", key='-TEXTTODOTODAY-', justification='center', expand_x=True)],
        [sg.Column(control_todo_buttons_layout, expand_x=True)],
        [sg.Text("Minione wydarzenia:", key='-TEXTDECIDEEVENT-', justification='center', expand_x=True)],
        [sg.Column(control_decide_past_buttons_layout, expand_x=True)],
        [sg.Text("Side quests:", key='-TEXTTODOSIDE-', justification='center', expand_x=True)],
        [sg.Column(control_todo_side_buttons_layout, expand_x=True)],
        [sg.Text("Jutro:", key='-TEXTTODOTOMORROW-', justification='center', expand_x=True)],
        [sg.Column(control_todo_tomorrow_buttons_layout, expand_x=True)]
        #[sg.Button("Button test", expand_x=True)]
    ], expand_x=True)

    apps_col = sg.Column([                                                                   # tworzenie panelu kontrolnego, tymczasowe
        [sg.Text('Lista aplikacji:', justification='left', expand_x=True)],
        [sg.Push(), sg.Button("Hardware monitor", key="-BUTTONMONITORPOPUPTOGGLE-", size=(13, 2), button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR), sg.Push(), sg.Button("Media player", key="-BUTTONMEDIAPLAYERWINDOWTOGGLE-", size=(13, 2), button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR), sg.Push(), sg.Button("", key='-PROGRAM3-', size=(13, 2), button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR), sg.Push(), sg.Button("", key='-PROGRAM7-', size=(13, 2), button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR)],
        [sg.Push(), sg.Button("", key='-PROGRAM4-', size=(13, 2), button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR), sg.Push(), sg.Button("", key='-PROGRAM5-', size=(13, 2), button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR), sg.Push(), sg.Button("", key='-PROGRAM6-', size=(13, 2), button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR), sg.Push(), sg.Button("", key='-PROGRAM8-', size=(13, 2), button_color=GLOBAL_CONTROL_APP_BUTTON_OFF_COLOR)]
    ])

    control_tab_layout = [
        [avatar_col, sys_monitor_col],
        [to_do_col],
        [apps_col]
    ]
    return control_tab_layout

def get_to_do_events() -> tuple[list[CalendarEvent], list[CalendarEvent], list[CalendarEvent]]:                     # ustala które wydarzenia wyświetlić na panelu kontrolnym wczytując je bezpośrednio z pliku kalendarza i odpowiednio filtrując
    calendar_events = read_calendar_events(GLOBAL_CALENDAR_SAVE_FILE_NAME)      # wczytujemy wydarzenia
    calendar_events = sort_calendar_events(calendar_events, sort_type=2)        # sortujemy je wg daty
    today_calendar_events = []
    side_calendar_events = []
    tomorrow_calendar_events = []
    # wybieranie wydarzeń pasujących do daty
    for i in range(len(calendar_events)):
        if calendar_events[i].datetime_format_date == datetime.datetime.now().date():     # tylko gdy dzień wydarzenia się pokrywa z dniem dzisiejszym
            today_calendar_events.append(calendar_events[i])
        elif calendar_events[i].datetime_format_date == datetime.datetime.now().date() + datetime.timedelta(days=1):        # wybieramy wydarzenia jutrzejsze dla innej listy
            tomorrow_calendar_events.append(calendar_events[i])
        elif calendar_events[i].date == "" or calendar_events[i].importance == 1:         # gdy daty w ogóle nie ma lub gdy ważność == 1 (ten warunek na pewno będzie do zmiany, razem z pierwszym w tym forze, zależy co gdzie będzie)
            side_calendar_events.append(calendar_events[i])
    # sortowanie wydarzeń wg ważności (dla opcjonalnych zadań wg optymalności - eksperymentalnie)
    today_calendar_events = sort_calendar_events(today_calendar_events, sort_type=3)
    side_calendar_events = sort_calendar_events(side_calendar_events, sort_type=4)          # tutaj sortujemy eksperymentalnie wg optymalności, zobaczymy jak to wyjdzie
    tomorrow_calendar_events = sort_calendar_events(tomorrow_calendar_events, sort_type=3)
    # obcinanie list z wydarzeniami do limitu narzuconego przez liczbę pozycji w panelu kontrolnym, zawsze brane jest pierwsze x wydarzeń
    if len(today_calendar_events)<=GLOBAL_CONTROL_TO_DO_BUTTON_NUMBER:
        today_calendar_events = today_calendar_events[:]        # jeżeli wydarzeń jest mniej niż tyle, ile miejsca jest w control panelu to przekazujemy całą tablicę
    else:
        today_calendar_events = today_calendar_events[0:GLOBAL_CONTROL_TO_DO_BUTTON_NUMBER]       # jak jest więcej, to przekazujemy tylko pierwsze x wydarzeń / przycinamy listę z wydarzeniami do liczby dostępnych przycisków
    if len(side_calendar_events)<=GLOBAL_CONTROL_TO_DO_SIDE_BUTTON_NUMBER:
        side_calendar_events = side_calendar_events[:]      
    else:
        side_calendar_events = side_calendar_events[0:GLOBAL_CONTROL_TO_DO_SIDE_BUTTON_NUMBER]
    if len(tomorrow_calendar_events)<=GLOBAL_CONTROL_TO_DO_TOMORROW_BUTTON_NUMBER:
        tomorrow_calendar_events = tomorrow_calendar_events[:]      
    else:
        tomorrow_calendar_events = tomorrow_calendar_events[0:GLOBAL_CONTROL_TO_DO_TOMORROW_BUTTON_NUMBER]
    return today_calendar_events, side_calendar_events, tomorrow_calendar_events

def get_todays_events(file_name=GLOBAL_CALENDAR_SAVE_FILE_NAME, read_if_reminded=False) -> list[CalendarEvent]:
    calendar_events = read_calendar_events(file_name, read_if_reminded=read_if_reminded)      # wczytujemy wydarzenia
    calendar_events = sort_calendar_events(calendar_events, sort_type=3)
    today_calendar_events = []
    for event in calendar_events:
        if event.datetime_format_date == datetime.datetime.now().date():
            today_calendar_events.append(event)
    return today_calendar_events    

def check_new_day():                            # sprawdza, czy jest właśnie północ, jeśli tak to wyświetla ostrzeżenie że rzeczy się mogą zepsuć
    if datetime.datetime.now().strftime("%H:%M") == datetime.datetime.strptime("00:00", "%H:%M").strftime("%H:%M") or datetime.datetime.now().strftime("%H:%M") == datetime.datetime.strptime("00:00", "%H:%M").strftime("%H:%M"):
        popup_warning("Uwaga! Już po północy! Dalsze korzystanie z programu może coś zepsuć! Sugeruję zamknięcie programu...", auto_close=False, avatar=GLOBAL_AVATAR_SLEEP)

def check_calendar_events_reminders():          # sprawdza, czy na liście wydarzeń do zrobienia dzisiaj jest jakieś wydarzenie, którego powiadomienie powinno się uruchomić w tej chwili, jeśli tak to włącza je
    todays_events = get_todays_events(GLOBAL_CALENDAR_TODAY_FILE_NAME, read_if_reminded=True)         # pobiera listę dzisiejszych wydarzeń z pliku z dzisiejszymi wydarzeniami, które już są "przygotowane"
    for event in todays_events:                 # poniższa linijka sprawdza, czy data pokrywa się z dzisiejszą, czy godzina powiadomienia jest, czy odpowiada godzinie w tym momencie oraz czy powiadomienie już było, czy jeszcze nie
        if event.date != "" and event.datetime_format_date == datetime.datetime.now().date() and event.if_reminded == False and event.datetime_format_reminder_hour != "" and event.datetime_format_reminder_hour <= datetime.datetime.now().time():
            event.if_reminded = True
            delete_calendar_event(event.id, GLOBAL_CALENDAR_TODAY_FILE_NAME)
            edited_calendar_event = CalendarEvent(event.name, event.date, event.date_end, event.hour_start, event.hour_end, event.info, event.importance, event.if_goout, event.if_deadline, event.positivity, event.repeat, event.if_constant, event.id, event.if_reminded)   # ostatnie powinno być zawsze =True
            edited_calendar_event.organise_data()
            edited_calendar_event.write_to_file(GLOBAL_CALENDAR_TODAY_FILE_NAME, append=True, write_if_reminded=True)
            popup_notify(event.name+" o godzinie "+event.hour_start+"!", "Przypomnienie!")
            break           # nie chcemy, żeby odpaliły się dwa przypomnienia na raz, więc drugie poczeka do kolejnego timeouta bądź innego eventu