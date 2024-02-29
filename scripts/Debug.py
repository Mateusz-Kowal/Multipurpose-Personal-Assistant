from Control import *

def create_debug_layout(theme):         # tworzy layout dla zakładki Debug
    debug_tab_layout = [
        [sg.Text('Funkcje do testowania i zarządzania programem', justification='center', expand_x=True)],
        [sg.Button("Wykonaj funkcje timeoutu", key="-BUTTONDEBUGCHECKPERIODICEVENTS-"), sg.Push(), sg.Button(" \u2139 ", key="-BUTTONDEBUGCHECKPERIODICEVENTSINFO-")],
        [sg.Button("Policz linijki kodu", key="-BUTTONDEBUGCOUNTSCRIPTLINES-"), sg.Push(), sg.Button(" \u2139 ", key="-BUTTONDEBUGCOUNTSCRIPTLINESINFO-")],
        [sg.Button("Pokaż wykorzystanie pamięci", key="-BUTTONDEBUGPRINTMEMORY-"), sg.Push(), sg.Button(" \u2139 ", key="-BUTTONDEBUGPRINTMEMORYINFO-")],
        [sg.Button("Oblicz "+str(GLOBAL_CALENDAR_POINTS_SYMBOL)+" dla wszystkich miesięcy", key="-BUTTONDEBUGCALCULATECALENDARPOINTS-"), sg.Push(), sg.Button(" \u2139 ", key="-BUTTONDEBUGCALCULATECALENDARPOINTSINFO-")]
    ]
    return debug_tab_layout

def debug_calculate_calendar_points():                          # podlicza punkty kalendarza dla wszystkich miesięcy w historii programu
    month = get_beginning_date().month, get_beginning_date().year       
    file = open(get_calendar_file_path(GLOBAL_CALENDAR_POINTS_FILE_NAME), "w")        # szybkie wyczyszczenie pliku
    file.close()
    record_file = open(get_calendar_file_path(GLOBAL_CALENDAR_POINTS_RECORD_FILE_NAME), "w", encoding='utf-8')      # resetowanie pliku z rekordem punktów (skoro punktacja się zmienia, to rekord punktów też)
    record_file.write("2000 Miesiac 0\n")                               # tymczasowe wartości, przy pierwszej iteracji rekord 0 punktów będzie nadpisany
    record_file.close()
    while month != (gv.current_month_number, gv.current_year):          # pętla po wszystkich miesiącach aż do teraźniejszego
        calendar_events = read_calendar_events(get_month_calendar_file_name(*month), autocreate=True)
        points = calculate_total_points(calendar_events)
        write_monthly_points_to_file(calendar_events, points, *month)        # gwiazdka rozpakowuje tuple'a
        if (points > read_record_points()):                 # jak jest pobity rekord punktów to zapisuje je w pliku z rekordem
            write_points_record_to_file(points, *month)
        month = get_next_month(*month)

def debug_count_script_lines(background_color = GLOBAL_POPUP_COLOR, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):      # zlicza wszystkie linijki ze wszystkich plików .py kodu programu i wyświetla wynik w popupie
    if GLOBAL_IS_DEV_VERSION:           # jeśli to wersja deweloperska, to jesteśmy od razu w dobrym miejscu
        file_list = glob.glob("./scripts/*.py")     # szuka wszystkich plików z końcówką .py w danych folderze i zapisuje ścieżki do listy
    else:                               # jeśli to wersja oficjalna, to musimy się przedostać do folderu z wersją deweloperską, bo tylko tam znajdziemy surowy kod
        file_list = glob.glob(GLOBAL_DEV_FOLDER_PATH+"*.py")
    lines_sum = 0
    script_lines_layout = []
    info_text = wrap_text("Oto wszystkie skrypty programu wraz z ich liczbą linijek:", GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS/2)
    script_lines_layout.append([sg.Text(info_text, background_color=background_color, font=font1)])
    for file_path in file_list:
        script_file = open(file_path, encoding="utf8")
        lines_num = len(script_file.readlines())
        script_file.close()
        lines_sum += lines_num
        script_lines_layout.append([sg.Text(file_path.split('\\')[1], background_color=background_color, font=font2), sg.Push(background_color=background_color), sg.Text(str(lines_num), background_color=background_color, font=font2)])
    script_lines_layout.append([sg.Text("Suma linijek: "+str(lines_sum), background_color=background_color, font=font1)])
    script_lines_layout.append([sg.Push(background_color=background_color), sg.Button("OK", key='-POPUPDEBUGCOUNTLINESBUTTONOK-'), sg.Push(background_color=background_color)])
    popup_event, popup_values = sg.Window('Informacje o kodzie programu', script_lines_layout, modal=True, background_color=background_color, disable_close=True).read(close=True)  # zwracanie czegokolwiek chyba i tak niepotrzebne

def debug_print_memory_usage(background_color = GLOBAL_POPUP_COLOR, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):                                 # wyświetla użycie pamięci przez BATIego
    memory = Process(os.getpid()).memory_info().rss / 1024 ** 2
    memory_usage_layout = []
    scrollbar_layout = []
    info_text = wrap_text("Pamięć użyta przez BATIego:", GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS/2)
    memory_usage_layout.append([sg.Text(info_text, background_color=background_color, font=font1)])
    memory_usage_layout.append([sg.Push(background_color=background_color), sg.Text(str(round(memory, 2))+" MB", key='-POPUPDEBUGMEMORY-', background_color=background_color), sg.Push(background_color=background_color)])
    memory_usage_layout.append([sg.Text("", background_color=background_color)])
    scrollbar_layout.append([sg.Text("Własne zmienne globalne:", justification="left", font=font1, background_color=background_color)])

    # cudowna, ale w dużej mierze kradziona linijka poniżej bierze zbiór wszystkich zmiennych z modułu gv, który jest jakby moim własnym zbiorem zmiennych globalnych;
    # następnie wyciąga z tych zmiennych ich nazwy i wartości, z wartości (!) obliczamy ile miejsca zajmują (rozmiar nazwy określa długość stringu nazwy), potem te wartości w odpowiednich jednostkach sortujemy 
    for name, size, value in sorted(((name, sys_getsizeof(value), value) for name, value in list(vars(gv).items()) if not name.startswith('_')), key= lambda x: -x[1]):     #złota_linijka     # dodać/usunąć [:10] tuż przed ostatnim ":", aby wyświetlić tylko Top10 największych zmiennych
        scrollbar_layout.append([sg.Text("{:>50}: {:>8}".format(name, sizeof_fmt(size)), background_color=background_color, font=font2)])
    scrollbar_layout.append([sg.Text("Systemowe zmienne globalne i ustawienia:", justification="left", font=font1, background_color=background_color)])
    for name, size, value in sorted(((name, sys_getsizeof(value), value) for name, value in list(globals().items()) if not name.startswith('_')), key= lambda x: -x[1]):    # to samo
        scrollbar_layout.append([sg.Text("{:>50}: {:>8}".format(name, sizeof_fmt(size)), background_color=background_color, font=font2)])
    scrollbar_layout.append([sg.Text("Zmienne lokalne:", justification="left", font=font1, background_color=background_color)])
    for name, size in sorted(((name, sys_getsizeof(value)) for name, value in list(locals().items()) if not name.startswith('_')), key= lambda x: -x[1]):                   # to samo
        scrollbar_layout.append([sg.Text("{:>50}: {:>8}".format(name, sizeof_fmt(size)), background_color=background_color, font=font2)])
    memory_usage_layout.append([sg.Column(scrollbar_layout, scrollable=True, vertical_scroll_only=True, size=(500, 700), size_subsample_height = 10, background_color=background_color, expand_x=True)])
    memory_usage_layout.append([sg.Push(background_color=background_color), sg.Button("OK", key='-POPUPDEBUGMEMORYOK-'), sg.Push(background_color=background_color)])
    popup_event, popup_values = sg.Window('Informacje o pamięci programu', memory_usage_layout, modal=True, background_color=background_color, disable_close=True).read(close=True)

def sizeof_fmt(num, suffix='B'):        # by Fred Cirera,  https://stackoverflow.com/a/1094933/1870254, modified; wzięte z https://stackoverflow.com/questions/24455615/python-how-to-display-size-of-all-variables
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

