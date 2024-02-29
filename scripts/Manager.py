from Calendar import *

def create_manager_layout(theme):       # tworzy layout zakładki z menedżerem
    sort_panel_layout = [                                               # panel z przyciskami do wybierania konkretnych grup wydarzeń
        [sg.Text("Sortuj według:"), sg.Radio("ID", group_id='ManagerSort', key='-CHECKBOXMANAGERSORTID-', enable_events=True), sg.Radio("daty", group_id='ManagerSort', key='-CHECKBOXMANAGERSORTDATE-', default=True, enable_events=True), sg.Radio("ważności", group_id='ManagerSort', key='-CHECKBOXMANAGERSORTIMPORTANCE-', enable_events=True), sg.Radio("optymalności", group_id='ManagerSort', key='-CHECKBOXMANAGERSORTOPTIMALSCORE-', enable_events=True)],        # czemu tutaj musi być enable_events?!
        [sg.Checkbox("wyjścia", key='-CHECKBOXMANAGERGOOUT-', enable_events=True, default=True), sg.Checkbox("zadania", key='-CHECKBOXMANAGERDEADLINE-', enable_events=True, default=True), sg.Checkbox("pozostałe", key='-CHECKBOXMANAGEROTHER-', enable_events=True, default=True), sg.Push(), sg.Checkbox("coroczne", key='-CHECKBOXMANAGERANNUAL-', enable_events=True, default=False)],
        [sg.Checkbox("ważność = 1", key='-CHECKBOXMANAGERIMPORTANCY1-', enable_events=True, default=True), sg.Checkbox("ważność = 2", key='-CHECKBOXMANAGERIMPORTANCY2-', enable_events=True, default=True), sg.Checkbox("ważność = 3", key='-CHECKBOXMANAGERIMPORTANCY3-', enable_events=True, default=True), sg.Checkbox("ważność = 4", key='-CHECKBOXMANAGERIMPORTANCY4-', enable_events=True, default=True)]
        #[sg.Checkbox("checkbox1", key='-CHECKBOXMANAGER9-'), sg.Checkbox("checkbox1", key='-CHECKBOXMANAGER10-'), sg.Checkbox("checkbox1", key='-CHECKBOXMANAGER11-'), sg.Checkbox("checkbox1", key='-CHECKBOXMANAGER12-')]
    ]
    event_panel_layout = []
    for i in range(GLOBAL_MANAGER_NUMER_OF_EVENT_BUTTONS):                    # pozwala wyświetlać maksymalnie X wydarzeń; większa liczba niestety powoduje że okno jest na długie, więc trzeba ustawić domyślny rozmiar okna, ale to psuje log_panel (wtf?) (wymyśleć jak to naprawić? nie ma max_size czy czegoś takiego)
        row = []
        row.append(sg.Button("", key=f'-BUTTONMANAGEREVENT{i+1}-', size=GLOBAL_MANAGER_EVENT_BUTTONS_SIZE, auto_size_button=True))
        event_panel_layout.append(row)
    manager_tab_layout = [                                                                   # czemu tu muszą być dwie kolumny na sobie?????
        [sg.Column(sort_panel_layout)],
        [sg.Column(event_panel_layout, scrollable=True, vertical_scroll_only=True, expand_y=True, size_subsample_height = float(GLOBAL_MANAGER_NUMER_OF_EVENT_BUTTONS)/10)]     # ostatnia część powoduje, że scrollbar może być mniejszy niż połowa okna wrrr
    ]
    return manager_tab_layout

def sort_calendar_events(calendar_events: list[CalendarEvent], sort_type, if_goout=True, if_todo=True, if_others=True, if_annual=True, if_imp1=True, if_imp2=True, if_imp3=True, if_imp4=True) -> list[CalendarEvent]:      # 1 - ID; 2 - data; 3 - ważność; 4 - optymalność        # sortuje podane wydarzenia wg różnych kluczy z możliwością filtrowania przed sortowaniem
    
    filtered_calendar_events = calendar_events          # wydarzenia, które spełniają warunki sortowania
    other_calendar_events = []

    # każda sekcja poniżej filtruje pulę wszystkich wydarzeń wg poszczególnych kryteriów podanych w parametrach tej funkcji
    tmp = []
    if if_imp1 == False:                                # jak imp1 nie jest zaznaczone, to wszystkie pozostałe wydarzenia z ważnościami innymi niż 1 "przechodzą dalej", czyli są wyciągane 
        for i in range(len(filtered_calendar_events)):
            if filtered_calendar_events[i].importance != 1:
                tmp.append(filtered_calendar_events[i])     # jak ważność inna niż to przepisujemy do tablicy tmp, która pójdzie dalej
        filtered_calendar_events = tmp                  # przepisujemy tmp spowrotem do filtered_calendar_events
    tmp = []
    if if_imp2 == False:                                # analogicznie robimy dla pozostałych ważności, każdy blok odfiltrowywuje daną ważność
        for i in range(len(filtered_calendar_events)):
            if filtered_calendar_events[i].importance != 2:
                tmp.append(filtered_calendar_events[i])     
        filtered_calendar_events = tmp
    tmp = []
    if if_imp3 == False:                               
        for i in range(len(filtered_calendar_events)):
            if filtered_calendar_events[i].importance != 3:
                tmp.append(filtered_calendar_events[i])     
        filtered_calendar_events = tmp
    tmp = []
    if if_imp4 == False:                               
        for i in range(len(filtered_calendar_events)):
            if filtered_calendar_events[i].importance != 4:
                tmp.append(filtered_calendar_events[i])     
        filtered_calendar_events = tmp
    tmp = []
    if if_todo == False:                                # podobnie robimy z pozostałymi flagami
        for i in range(len(filtered_calendar_events)):
            if filtered_calendar_events[i].if_deadline == False:
                tmp.append(filtered_calendar_events[i])     
        filtered_calendar_events = tmp
    tmp = []
    if if_goout == False:                               
        for i in range(len(filtered_calendar_events)):
            if filtered_calendar_events[i].if_goout == False:
                tmp.append(filtered_calendar_events[i])     
        filtered_calendar_events = tmp
    tmp = []
    if if_others == False:                                          # odfiltrowywuje wydarzenia, które nie są ani zadaniami ani wyjściami - zostają tylko zadania i wyjścia
        for i in range(len(filtered_calendar_events)):
            if filtered_calendar_events[i].if_goout == True or filtered_calendar_events[i].if_deadline == True:
                tmp.append(filtered_calendar_events[i])     
        filtered_calendar_events = tmp
    tmp = []
    if if_annual == False:                                          # odfiltrowywuje urodziny, święta...
        for i in range(len(filtered_calendar_events)):
            if filtered_calendar_events[i].repeat != 365:
                tmp.append(filtered_calendar_events[i])     
        filtered_calendar_events = tmp
    tmp = []

    if sort_type == 1:              # jak sortujemy wg ID to nic nie robimy, bo to już czyta wg kolejności dodania do pliku kalendarza (czyli wg ID) -> co z powtarzającymi się wydarzeniami? hmmm...
        sorted_calendar_events = filtered_calendar_events
    else:                           # w pozostałych wypadkach najpierw zawsze sortujemy wg daty (jako drugie kryterium)
        events_with_date = []
        events_without_date = []
        for i in range(len(filtered_calendar_events)):
            if filtered_calendar_events[i].datetime_format_date == "":          # jeśli data jest równa pustemu stringowi, to znaczy że wydarzenie nie ma daty (a przynajmniej tak powinno być)
                events_without_date.append(filtered_calendar_events[i])
            else:
                events_with_date.append(filtered_calendar_events[i])
        date_sorted_calendar_events = sorted(events_with_date, key=operator.attrgetter("datetime_format_date", "datetime_format_hour_sort"))+events_without_date      # to jest OK; wydarzenia bez daty doklejamy chyba na koniec no, bo co z nimi zrobić, może ich w ogóle nie będzie w praktyce?
        if sort_type == 2:            # sortowanie wg daty        
            sorted_calendar_events = date_sorted_calendar_events                      # nic nie robimy
        elif sort_type == 3:          # sortowanie wg ważności, do najważniejszych
            sorted_calendar_events = sorted(date_sorted_calendar_events, key=operator.attrgetter("importance"), reverse=True)
        else:                         # sortowanie wg optymalności
            sorted_calendar_events = sorted(date_sorted_calendar_events, key=operator.attrgetter("optimal_score"), reverse=True)
    return sorted_calendar_events
