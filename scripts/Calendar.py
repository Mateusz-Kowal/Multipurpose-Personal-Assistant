from functions import *

class CalendarEvent:                        # klasa odpowiadająca za poszczególne wydarzenie
    def __init__(self, name, date, date_end, hour_start, hour_end, info, importance, if_goout, if_deadline, positivity, repeat, if_constant, id, if_reminded=False):
        self.name = name
        self.date = date
        self.date_end = date_end
        self.hour_start = hour_start
        self.hour_end = hour_end
        self.info = info
        self.importance = int(importance)
        self.if_goout = if_goout
        self.if_deadline = if_deadline
        self.positivity = int(positivity)
        if repeat == "":
            self.repeat = 0
        else:
            self.repeat = int(repeat)
        self.if_constant = if_constant
        self.id = int(id)
        self.if_reminded = if_reminded
    
    def organise_data(self):                # w przypadku wprowadzenia danych w różnym formacie zamienia je na jednolite/uniwersalne, dodatkowo tworzy pomocnicze zmienne
        #self.reminder = ""                          # zmienna określająca na ile minut przed wydarzeniem wyświetli się przypomnienie o wydarzeniu
        # edycja godziny
        self.datetime_format_hour_start = ""
        self.datetime_format_hour_end = ""
        self.datetime_format_reminder_hour = ""
        if self.hour_start != "" and ':' not in self.hour_start:                    # dopisanie zer na końcu, jeżeli została wpisana np 14, a nie 14:00
            self.hour_start = self.hour_start+":00"
        if self.hour_start != "" and len(self.hour_start) == 4:                     # jeżeli godzina nie ma zera na początku (czyli ma 4 znaki - X:XX) (bo np była tak wpisana do kalendarza, to dodajemy zero)
            self.hour_start = "0"+self.hour_start
        if self.hour_start != "":
            self.datetime_format_hour_start = datetime.datetime.strptime(self.hour_start, "%H:%M")      # zamiana na format, w którym można porównywać i liczyć rzeczy;         !!! tutaj godzina już z zerem wiodącym
            if self.if_goout == True:   # w linijce powyżej i kilku linijkach poniżej odejmujemy czas wyprzedzenia przypomnienia od czasu wydarzenia, żeby otrzymać czas przypomnienia, jednak musimy to robić na typie datetime, a nie na time; dopiero potem z całej daty wyciągamy czas
                if self.datetime_format_hour_start >= datetime.datetime.strptime(GLOBAL_CALENDAR_NOTIFICATION_TIME_GOOUT, "%H:%M"):      # jak cofnięcie spowoduje przeniesienie sie na poprzedni dzień to w ogóle rezygnujemy z przypomnienia (zakładam, że jak będę gdzieś wychodził o 1 w nocy to raczej będę o tym wiedział :P)
                    self.datetime_format_reminder_hour = (self.datetime_format_hour_start - datetime.timedelta(hours=GLOBAL_CALENDAR_NOTIFICATION_TIME_GOOUT_HOURS)).time()
            else:
                if self.datetime_format_hour_start >= datetime.datetime.strptime(GLOBAL_CALENDAR_NOTIFICATION_TIME, "%H:%M"):
                    self.datetime_format_reminder_hour = (self.datetime_format_hour_start - datetime.timedelta(minutes=GLOBAL_CALENDAR_NOTIFICATION_TIME_MINUTES)).time()
            self.datetime_format_hour_start = self.datetime_format_hour_start.time()        # wyciąganie samego czasu z daty i zamknięcie segmentu ^
        if self.hour_end != "" and ':' not in self.hour_end:                # to samo dla końcowej, o ile jest
            self.hour_end = self.hour_end+":00"
        if self.hour_end != "" and len(self.hour_end) == 4:                   
            self.hour_end = "0"+self.hour_end
        if self.hour_end != "":
            self.datetime_format_hour_end = datetime.datetime.strptime(self.hour_end, "%H:%M").time()
        # edycja daty
        self.day_string = ""
        self.day_number = ""
        self.month_string = ""
        self.month_name = ""
        self.year = ""
        self.datetime_format_date = ""                  # używane tylko przez Menedżera do sortowania
        self.date_difference = 0                        # int;  różnica między datą wydarzenia, a dzisiejszą (liczba dni);  -1 oznacza, że nie ma podanej daty wydarzenia -> w sumie to niech będzie 0, po co dodawać punkty?
        #self.hour_difference = -1                      # nie wiadomo czy liczenie różnicy w godzinach w ogóle będzie działać - co jak różnica czasów będzie ujemna?
        self.day_end_string = ""
        self.day_end_number = ""
        self.month_end_string = ""
        self.month_end_name = ""
        self.year_end = ""
        self.datetime_format_date_end = ""
        self.length_days = 1
        self.show_on_calendar = False
        self.datetime_format_dates_list = []            # lista z datami, w których wydarzenie trwa (przydatne do wielodniowych wydarzeń)
        #if self.repeat == 0 or self.repeat >= GLOBAL_CALENDAR_SHOW_REPEAT_THRESHOLD:           # jak wydarzenie powtarza się zbyt często, to nie wyświetlamy go na kalendarzu bo to bez sensu
        if self.importance >= 3:                                                                # zmiana warunku na po prostu importancy >= 3, zobaczymy czy tak lepiej
            self.show_on_calendar = True
        if self.date != "":                                 # tworzenie dodatkowych zmiennych powiązanych z datą usprawniających różne operacje
            self.day_number = self.date.split('.')[0]
            if len(self.day_number)==1:
                self.day_string = "0"+self.day_number                   # string z ewentualnym zerem na początku
            else:
                self.day_string = self.day_number
            self.day_number = int(self.day_number)                      # upewnienie się że *_number to int (nie ma zera na początku)
            self.month_number = self.date.split('.')[1]
            if len(self.month_number)==1:
                self.month_string = "0"+self.month_number               # string z ewentualnym zerem na początku
            else:
                self.month_string = self.month_number
            self.month_number = int(self.month_number)                  # upewnienie się że *_number to int
            self.month_name = month_number_to_word(self.month_number)   # string z nazwą miesiąca po angielsku z dużej litery
            self.year = self.date.split('.')[2]
            self.date = self.day_string+"."+self.month_string+"."+self.year
            self.datetime_format_date = datetime.datetime.strptime(self.date, "%d.%m.%Y").date()            # chyba z zerem wiodącym???
            self.date_difference = (self.datetime_format_date-datetime.datetime.now().date()).days
            if self.date_difference<0:      # żeby nie było problemów z logarytmem poniżej
                self.date_difference=0
            if self.date_end != "":         # teraz cała sekcja dla daty zakończenia, to samo co wyżej
                self.day_end_number = self.date_end.split('.')[0]
                if len(self.day_end_number)==1:
                    self.day_end_string = "0"+self.day_end_number
                else:
                    self.day_end_string = self.day_end_number
                self.day_end_number = int(self.day_end_number)
                self.month_end_number = self.date_end.split('.')[1]
                if len(self.month_end_number)==1:
                    self.month_end_string = "0"+self.month_end_number
                else:
                    self.month_end_string = self.month_end_number
                self.month_end_number = int(self.month_end_number)
                self.month_end_name = month_number_to_word(self.month_end_number)
                self.year_end = self.date_end.split('.')[2]
                self.date_end = self.day_end_string+"."+self.month_end_string+"."+self.year_end
                self.datetime_format_date_end = datetime.datetime.strptime(self.date_end, "%d.%m.%Y").date()
                self.length_days = (self.datetime_format_date_end - self.datetime_format_date).days + 1         # +1, bo ta funkcja zaokrągla w dół, a chcemy liczbę dni do pokolorowania w kalendarzu (tutaj nie ma nigdzie godzin)
            for i in range(self.length_days):       # tworzy listę dat, w ciągu których jest wydarzenie (dla jednodniowych oczywiście jest jedno); wydarzenie trwa przez length_days dni; z tą listą porównujemy kolorując dni w kalendarzu
                self.datetime_format_dates_list.append(self.datetime_format_date+datetime.timedelta(days=i))
        if self.hour_start != "":
            self.hour_sort = self.hour_start
        else:
            self.hour_sort = "23:59"                    # przydzielamy wydarzeniom tymczasową godzinę równą 23:59, żeby móc posortować też wg godziny; pioryteryzujemy wydarzenia z godziną -> przydatne do sortowania napisów na przycisku kalendarza oraz w menedżerze
        self.datetime_format_hour_sort = datetime.datetime.strptime(self.hour_sort, "%H:%M")        # powyższą godzinę sprowadzamy do formatu datetime, żeby można było potem porównywać
        
        # tworzenie optymalności danego wydarzenia, które pomaga piorytaryzować wydarzenia w menedżerze, cały wzór na razie na czuja, potem trzeba się zastanowić, czy może jedne powinny być wyświetlane nad drugimi czy coś
        self.optimal_score = self.importance*GLOBAL_MANAGER_EVENT_IMPORTANCE_WEIGHT - log10(self.date_difference*GLOBAL_MANAGER_EVENT_DATE_DIFFERENCE_WEIGHT+1)+2 + self.positivity*GLOBAL_MANAGER_EVENT_POSITIVITY_WEIGHT + 1/(self.repeat*GLOBAL_MANAGER_EVENT_REPEAT_WEIGTH+1)
        
        # obliczanie ile linijek zajmuje nazwa (możliwe że działa dobrze, pytanie co jeśli suma wyrazów = max szerokość?)
        self.calendar_line_number = len(textwrap.wrap(self.name, GLOBAL_CALENDAR_DAY_BUTTONS_SIZE_CHARACTERS[0]))       # chyba tak najlepiej bo potem i tak z tego korzystamy XD;  jedyne co można tutaj poprawić, to żeby od razu totaj tworzył też sformatowany tekst na przycisk i potem go tylko sklejał
        # words = self.name.split(" ")              # ten algorytm fajny ale no chyba niepotrzebny
        # length = 0
        # self.calendar_line_number = 1
        # for i in range(len(words)):
        #     length = length + len(words[i])                     # słowo + następne słowo
        #     if i!=0:
        #         length += 1                                     # jeśli to nie jest pierwsze słowo to dodajemy jeszcze długość spacji pomiędzy nimi
        #     if length>GLOBAL_CALENDAR_DAY_BUTTONS_SIZE_CHARACTERS[0]:      # jeśli słowo + spacja + następne słowo będzie dłuższe niż maksymalna długość dla linijki, to wtedy się przeleje do następnej i dodamy 1
        #         length = len(words[i])                          # wtedy w następnej linijce będzie tylko to drugie słowo
        #         self.calendar_line_number += 1
        
        #self.calendar_line_number = int((len(self.name)-self.name.count(" ")-1)/GLOBAL_CALENDAR_DAY_BUTTONS_SIZE[0])+1             # STARA METODA Z LICZENIEM SPACJI, zostawić na razie;        odejmujemy 1, żeby przy idealnie wypełnionych n rzędach nie dodawało jeszcze jednego (np 18/9 = 2, a powinno być 1)      
        self.importance_inverted = 4-self.importance                                                            # potrzebne do sortowania przy piorytetyzacji wyświetlania nazw wydarzeń na przyciskach kalendarza
        # dobranie koloru
        if self.importance == 1:
            self.color = GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY1
        elif self.importance == 2:
            self.color = GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY2
        elif self.importance == 3:
            self.color = GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY3
        elif self.importance == 4:
            self.color = GLOBAL_MANAGER_EVENT_COLOR_IMPORTANCY4
        self.points = self.calculate_points()
    
    def write_to_file(self, save_file_name, append=True, write_if_reminded=False):            # zapisuje wydarzenie do pliku
        if append==True:
            save_file = open(get_calendar_file_path(save_file_name), "a", encoding='utf-8')              # bez ustalenia kodowania są krzaczki, mimo tego że niby jest już w UTF-8
        else:
            save_file = open(get_calendar_file_path(save_file_name), "w", encoding='utf-8')
        save_file.write("____________________________________________________________________________________________________\n")
        if self.date != "" and self.date_end != "":
            save_file.write(self.date+" - "+self.date_end+" | ")
        elif self.date != "":
            save_file.write(self.date+"              | ")
        else:
            save_file.write("                        | ")
        if self.hour_start != "":                               # rozmieszcza ładnie nazwę i ewentualne godziny
            save_file.write(self.hour_start)
            if self.hour_end != "":
                save_file.write(" - "+self.hour_end+" | "+self.name+"\n")
            else:
                save_file.write("         | "+self.name+"\n")
        else:
            save_file.write("              | "+self.name+"\n")
        save_file.write("Info: "+self.info+"\n")
        save_file.write(str(self.id)+" | "+str(self.repeat).rjust(3)+" | ")             # końcówka linijki tworzy 3 miejsca, w które wpisuje inta z repeatem (tzn zawsze ten zapis zajmie 3 znaki, bez znaczenia ile cyfr ma int)
        if self.if_goout == True:
            save_file.write("WYJSCIE | ")
        else:
            save_file.write("        | ")
        if self.if_deadline == True:
            save_file.write("ZADANIE | ")
        else:
            save_file.write("        | ")
        save_file.write(str(self.positivity).rjust(2)+" | ")
        save_file.write(str(self.importance)+" | ")
        if self.if_constant == True:
            save_file.write("1")
        else:
            save_file.write("0")
        if write_if_reminded == True:
            save_file.write(" | "+str(self.if_reminded))
        save_file.write("\n")
        save_file.close()

    def calculate_points(self):                     # oblicza punkty za wydarzenie
        sum = 100                                                               # zaczyna od bazowej wartości 100
        sum = sum - self.positivity*20                                          # +/- 20 w zależności od pozytywności
        if self.if_constant == True:                                        # jak to święta lub urodziny to /10 bo mało wkładu (wydarzenia np kupić prezent to oczywiście co innego)
            sum = sum / 10
        elif self.repeat == 0:                                                  # dla repeat == 0 testowa wartość 3
            sum = sum * 3
        else:
            sum = sum * (self.repeat ** (1/3))                                  # im większy repeat tym więcej punktów (jako rekompenesata że jest rzadziej) -> pierwiastek 3-go stopnia
        if self.importance == 1 or self.importance == 4:                        # ważności 1 traktujemy specjalnie - dostają duży bonus, zeby zachęcić do robienia, ważności 4 dostają mały bonusik
            sum = sum * 5
        else:
            sum = sum * self.importance
        if self.if_deadline == True:                                            # deadline'owe wydarzenia powinny wymagać więcej wysiłku więc dostają więcej punktów
            sum = sum * 1.5
        sum = int(sum/50)*50                                                    # zaokrągla do najbliższej 50 !!! zobaczyć, czy nie trzeba dodać 1 po zrzutowaniu, żeby zawsze było minimum 50 punktów
        return sum

# tworzy układ kalendarza
def create_calendar_layout(theme, button_dates_numbers, month_word, year):
    # calendar_button_size = GLOBAL_CALENDAR_DAY_BUTTONS_SIZE_CHARACTERS    # to i tak nic nie robi
    calendar_tab_layout = [
        [sg.Text('Kalendarz', justification='center', expand_x=True)],
        [sg.Button('<', key='-BUTTONCALPREV-'), sg.Text("", size=15, font=GLOBAL_FONT_NOTIFICATIONS), sg.Push(), sg.Text(month_word, key='-MONTHTEXT-', justification='center', enable_events=True), sg.Text(year, key='-YEARTEXT-', justification='center'), sg.Push(), sg.Text("0/0"+GLOBAL_CALENDAR_POINTS_SYMBOL, key='-MONTHPOINTS-', size=15, justification='right', font=GLOBAL_FONT_NOTIFICATIONS), sg.Button('>', key='-BUTTONCALNEXT-')],
        [sg.Text('MON', justification='center', expand_x=True), sg.Text('TUE', justification='center', expand_x=True), sg.Text('WED', justification='center', expand_x=True), sg.Text('THU', justification='center', expand_x=True), sg.Text('FRI', justification='center', expand_x=True), sg.Text('SAT', justification='center', expand_x=True), sg.Text('SUN', justification='center', expand_x=True)]
    ]
    for w in range(6):      # automatyczne tworzenie przycisków kalendarza z odpowiednim numerem dnia, kluczem i innymi parametrami; dodatkowo w tej sekcji zarządzamy wyróżnianiem się dnia dzisiejszego na kalendarzu
        row = [sg.Push()]
        for d in range(7):      # poniżej wyróżnianie dnia dzisiejszego na kalendarzu - niestety, ale po zmianie miesiąca przycisk nadal jest "pogrubiony" ze względu na to, że nie da się zmienić tych parametrów
            #if button_dates_numbers[w][d] == str(datetime.datetime.now().day):       # jak się zgadza data z dzisiejszą
                #row.append(sg.Button(button_dates_numbers[w][d], key=f'-BUTTONCAL{7*w+d+1}-', size=calendar_button_size, pad=GLOBAL_CALENDAR_DAY_BUTTON_TODAY_PAD, border_width=GLOBAL_CALENDAR_DAY_BUTTON_TODAY_BORDER, font=GLOBAL_FONT_CALENDAR_BUTTONS))
            # w linijce powyżej oraz poniżej trzeba dobrać wartości pada i border_width tak, żeby dzień dzisiejszy miał pogrubioną ramkę, ale żeby ten przycisk nie powodował "wybrzuszanie się" kalendarza; znalezione odpowiednie wartości: [dzisiaj=(0, 5); inne=(3, 1)], ...
            # ^ tmp
            # poniżej opcja z obrazami zamiast kolorów
            row.append(sg.Button(button_dates_numbers[w][d], key=f'-BUTTONCAL{7*w+d+1}-', button_color="black", pad=GLOBAL_CALENDAR_DAY_BUTTONS_PAD, border_width=GLOBAL_CALENDAR_DAY_BUTTONS_BORDER, font=GLOBAL_FONT_CALENDAR_BUTTONS, image_source=get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_UNAVAILABLE, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1])))      # image_source=get_image_path(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_ONE_TASK), image_size=(60, 40); #złota_linijka za sprytne automatyczne tworzenie przycisków kalendarza - sporo mi zajęło wykminienie tego i to była jedna z pierwszych takich rzeczy
        row.append(sg.Push())
        calendar_tab_layout.append(row)
    calendar_tab_layout.append([sg.Button('Pokaż historię', key='-BUTTONSWITCHHISTORYLOADING-', font=GLOBAL_FONT_NOTIFICATIONS), sg.Push(), sg.Button('Zamień tekst', key='-BUTTONSWITCHBUTTONTEXT-')])
    calendar_tab_layout.append([sg.Text('Dodaj nową pozycję:')])
    calendar_tab_layout.append([sg.Text('Data:     Od:', key='-TEXTINPUTDATE-', enable_events=True), sg.Input(key='-INPUTDATE-', size=(10, 1)), sg.Text(' Do:', key='-TEXTINPUTDATEEND-', enable_events=True), sg.Input(key='-INPUTDATEEND-', size=(10, 1)), sg.Push(), sg.Checkbox('Stałe', key='-CHECKBOXCONSTANT-', default=False)])
    calendar_tab_layout.append([sg.Text('Godzina:       Od:'), sg.Input(key='-INPUTHOUR1-', size=(5, 1)), sg.Text('      Do:'), sg.Input(key='-INPUTHOUR2-', size=(5, 1))])
    calendar_tab_layout.append([sg.Text('Nazwa:'), sg.Input(key='-INPUTNAME-', size=(GLOBAL_CALENDAR_EVENT_NAME_MAX_LENGTH, 1))])
    calendar_tab_layout.append([sg.Text('Info:'), sg.Multiline(key='-INPUTINFO-', size=(30, 3), expand_x=True)])
    calendar_tab_layout.append([sg.Text('Ważność:'), sg.Radio('1', group_id='RadioCalendarImportance', key='-RADIOIMPORTANCE1-', default=False), sg.Radio('2', group_id='RadioCalendarImportance', key='-RADIOIMPORTANCE2-', default=False), sg.Radio('3', group_id='RadioCalendarImportance', key='-RADIOIMPORTANCE3-', default=True), sg.Radio('4', group_id='RadioCalendarImportance', key='-RADIOIMPORTANCE4-', default=False), sg.Push(), sg.Text('Pozytywność:'), sg.Radio('+', group_id='RadioCalendar', key='-RADIOPOSITIVE-'), sg.Radio('+/-', group_id='RadioCalendar', key='-RADIONEUTRAL-', default=True), sg.Radio('-', group_id='RadioCalendar', key='-RADIONEGATIVE-')])
    calendar_tab_layout.append([sg.Text('Powtarzaj co:'), sg.Input(key='-INPUTREPEAT-', size=(3, 1)), sg.Push(), sg.Checkbox('Wyjście z domu', key='-CHECKBOXGOOUT-'), sg.Checkbox('Termin to deadline', key='-CHECKBOXDEADLINE-')])
    calendar_tab_layout.append([sg.Text('        '), sg.Push(), sg.Button("DODAJ", key='-BUTTONADDCALENDAR-'), sg.Push(), sg.Button("Wyczyść", key='-BUTTONCLEARCALENDARINPUT-')])
    return calendar_tab_layout

# przypisuje odpowiednie napisy przyciskom na kalendarzu, które odpowiadają numerom dni
def assign_calendar_buttons_dates(year = int(datetime.datetime.now().strftime("%Y")), month = int(datetime.datetime.now().strftime("%m")), day = int(datetime.datetime.now().strftime("%d"))):
    button_dates_int = calendar.monthcalendar(year, month)
    for w in range(len(button_dates_int)):
        for d in range(7):
            if button_dates_int[w][d] == 0:
                button_dates_int[w][d] = " "            # jak tutaj oraz niżej są "" zamiast " " to zwęża przyciski kalendarza XDD co jest XD
    button_dates_numbers = [[str(s) for s in sublist] for sublist in button_dates_int]              # !!! rzutowanie wszystkich elementów w liście 2D z inta na string
    if len(button_dates_numbers) == 5:                      # zależności od tego ile rzędów zajmuje dany miesiąc uzupełniamy resztę pustymi przyciskami, tak żeby było 6x7
        tmp_butt = np.r_[button_dates_numbers, [[" ", " ", " ", " ", " ", " ", " "]]]
        button_dates_numbers = tmp_butt.tolist()
    if len(button_dates_numbers) == 4:
        tmp_butt = np.r_[button_dates_numbers, [[" ", " ", " ", " ", " ", " ", " "]]]
        tmp_butt = np.r_[tmp_butt, [[" ", " ", " ", " ", " ", " ", " "]]]
        button_dates_numbers = tmp_butt.tolist()
    return button_dates_numbers

# przypisuje odpowiednie kolory przyciskom w kalendarzu, zwraca także tablicę z wydarzeniami dla kolejnych dni
def assign_calendar_buttons_colors(button_dates_numbers, calendar_events: list[CalendarEvent], year = datetime.datetime.now().strftime("%Y"), month = datetime.datetime.now().strftime("%m"), day = datetime.datetime.now().strftime("%d")):
    button_colors = []
    events_month_array = []             # dla każdego dnia tworzona jest lista z wydarzeniami (dla większości dni jest ona pusta)
    # obrazy ładujemy od razu (hehe), robimy to 7-8 razy zamiast 42 w mainie w update_calendar()
    image_unavaiable = get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_UNAVAILABLE, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1])
    image_free = get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_FREE, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1])
    image_imp3 = get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1])
    image_imp3_3 = get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_3, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1])
    image_imp3_4 = get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_4, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1])
    image_imp4 = get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP4, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1])
    image_imp4_4 = get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP4_4, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1])
    for w in range(6):                  # dla każdego dnia sprawdzamy, czy kolejne wydarzenia są akurat tego dnia, co rozpatrywany przycisk
        row = []
        event_row = []
        for d in range(7):
            found_date = 0
            found_important_date = 0
            event_row_list = []        # wydarzenia danego dnia [w][d]
            if button_dates_numbers[w][d] != " " and button_dates_numbers[w][d] != "":            # jeżeli nie ma numerka dnia, to na pewno nie ma tam wydarzeń i kolor będzie szary
                calendar_button_datetime_format_date = datetime.datetime.strptime(button_dates_numbers[w][d]+"."+str(month)+"."+str(year), "%d.%m.%Y").date()         # tworzy datę, za którą odpowiada dany przycisk kalendarza, w formacie datetime, by łatwo porównać z datami w których jest dane wydarzenie
                for event in calendar_events:               # gdy data (dzień, miesiąc (wyraz) i rok) eventu pokrywa się z dniem na przycisku, to będzie on czerwony; jednak trzeba uważać gdy przycisk oraz event nie mają dnia
                    if calendar_button_datetime_format_date in event.datetime_format_dates_list and event.show_on_calendar == True:
                        found_date += 1                       # ^ do tych linijek jeszcze uwaga, że dla wydarzeń powtarzających się nie kolorujemy kalendarza (bo by był pewnie cały czerwony)
                        if event.importance == 4:               # jak wydarzenie jest ważne, to zostanie pomalowane na niebiesko
                            found_important_date += 1 
                        event_row_list.append(event)            # dodajemy wydarzenia do listy dla danego dnia i potem doklejemy do tablicy z całym miesiącem
            event_row.append(event_row_list)
            # tutaj sprawdzamy różne kombinacje wydarzeń i przypisujemy odpowiednie kolory przycisków
            if button_dates_numbers[w][d] != " " and button_dates_numbers[w][d] != "" and (int(button_dates_numbers[w][d]) != gv.current_day or month != gv.current_month_number or year != gv.current_year):   # gdy data przycisku NIE jest równa dzisiejszej i gdy przycisk nie jest pusty
                if button_dates_numbers[w][d] == "" or button_dates_numbers[w][d] == " ":
                    row.append(image_unavaiable)                    # niedostępny dzień (szary)
                elif found_date == 0:
                    row.append(image_free)                           # wolny dzień (zielony)
                else:
                    if found_date == 1:
                        if found_important_date == 0:
                            row.append(image_imp3)                   # 1x imp3 (czerwony)
                        else:
                            row.append(image_imp4)                   # 1x imp4 (błękitny)
                    else:
                        if found_important_date == 0:
                            row.append(image_imp3_3)                 # 2x imp3 (bordowy)
                        elif found_important_date == found_date:
                            row.append(image_imp4_4)                 # 2x imp4 (niebieski)
                        else:
                            row.append(image_imp3_4)                 # 1x imp3 + 1x imp4 (fioletowy)
            else:                                                                           # gdy data przycisku JEST równa dzisiejszej to wybieramy tło z obwódką
                if button_dates_numbers[w][d] == "" or button_dates_numbers[w][d] == " ":
                    row.append(image_unavaiable)                          # niedostępny dzień (szary)
                elif found_date == 0:                   # ładujemy od razu tło na dzisiaj (jako że jest tylko jedno to nie robi to problemu)
                    row.append(get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_FREE_TODAY, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1]))                           # wolny dzień (zielony)
                else:
                    if found_date == 1:
                        if found_important_date == 0:
                            row.append(get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_TODAY, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1]))                   # 1x imp3 (czerwony)
                        else:
                            row.append(get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP4_TODAY, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1]))                   # 1x imp4 (błękitny)
                    else:
                        if found_important_date == 0:
                            row.append(get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_3_TODAY, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1]))                 # 2x imp3 (bordowy)
                        elif found_important_date == found_date:
                            row.append(get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP4_4_TODAY, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1]))                 # 2x imp4 (niebieski)
                        else:
                            row.append(get_calendar_image_byte_value(GLOBAL_CALENDAR_DAY_BUTTON_IMAGE_IMP3_4_TODAY, GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[0], GLOBAL_CALENDAR_DAY_BUTTONS_IMAGE_SIZE_PIXELS[1]))                 # 1x imp3 + 1x imp4 (fioletowy)
        button_colors.append(row)
        events_month_array.append(event_row)
    return button_colors, events_month_array

def assign_new_calendar_event_id(read_file = GLOBAL_CALENDAR_NEW_ID_FILE_NAME):        # przypisuje nowy numer ID dla wydarzenie CalendarEvent utworzonego w przyszłości, informację to poprzednim najwięjszym ID pobiera z pliku z historią wydarzeń (domyślnie calendar_history.txt); TRZEBA SIĘ UPEWNIĆ, ŻE NUMERY ID SĄ AKTUALNE W STOSUNKU DO TEGO CO JEST W PLIKU calendar_save.txt, żeby nie nadpisało ID
    id_file = open(get_calendar_file_path(read_file), "r")                                          # wczytujemy plik z nowym ID dla wydarzenia
    gv.calendar_new_event_id = int(id_file.readline())                 # to już jest nowe ID (bez dodawania!)
    id_file.close()

def sort_event_names(today_event_list: list[CalendarEvent]) -> str:                             # sortuje nazwy wydarzeń w celu optymalnego wyświetlania na przyciskach kalendarza
    if len(today_event_list) == 1:
        event_string = wrap_text(today_event_list[0].name, GLOBAL_CALENDAR_DAY_BUTTONS_SIZE_CHARACTERS[0])
        event_string = event_string[0:-1]           # wszystkie znaki ze stringa poza ostatnim
    # elif len(today_event_list) > 2:                         # sprawdzanie jak działa to całe sortowanie po kilku kryteriach, zostawić na przyszłość, fajny kod, TYLKO SZKODA ŻE NIE DZIAŁA AAAAAAAAAAAAAAAAAAAA
        
    #     list_import = [2, 3, 4]
    #     list_lines = [1, 2, 3]

    #     events_name_list = []
    #     events_id_list = []
    #     id = 10
    #     event_import_list = []
    #     event_lines_list = []
    #     for i in list_import:
    #         for j in list_lines:
    #             events_name_list.append("nazwa_"+str(i)+"_"+str(j))
    #             events_id_list.append(id)
    #             id += 1
    #             event_import_list.append(4-i)
    #             event_lines_list.append(j)
    #     for i in range(len(events_name_list)):
    #         print(events_id_list[i], event_import_list[i], event_lines_list[i], events_name_list[i])

    #     print("")
    #     print("")
    #     z = list(zip(events_id_list, event_import_list, event_lines_list, events_name_list))                    # shufflowanie kilku list na raz !!!
    #     random.shuffle(z)
    #     events_id_list, event_import_list, event_lines_list, events_name_list = zip(*z)

    #     for i in range(len(events_name_list)):
    #         print(events_id_list[i], event_import_list[i], event_lines_list[i], events_name_list[i])

    #     print("")
    #     print("")

    #     cos = [(id,i,l,e) for id,i,l,e in sorted(zip(events_id_list, event_import_list, event_lines_list, events_name_list), reverse=False)]

    #     for i in range(len(events_name_list)):
    #         print(cos[i][0], cos[i][1], cos[i][2], cos[i][3])

    #     event_string = "test"

    else:
        sorted_today_event_list = sorted(today_event_list, key=operator.attrgetter("calendar_line_number", "importance_inverted", "repeat", "datetime_format_hour_sort", "id"), reverse=False)           # sortuje wydarzenia z danego dnia wg podanych kryteriów; najpierw wg liczby zajmowanych linijek rosnąco, potem ważności malejąco, potem powtarzania rosnąco, na końcu wg id (ostatnie kryterium musi być rozróżnialne dla każdego wydarzenia)
        line_number_list = []
        for i in range(len(sorted_today_event_list)):                                                       # tworzy listę z liczbą linijek do sprawdzania później czy nazwa się jeszcze zmieści
            line_number_list.append(sorted_today_event_list[i].calendar_line_number)
        event_string = ""
        total_lines = 0
        for i in range(len(sorted_today_event_list)):
            if total_lines <= GLOBAL_CALENDAR_DAY_BUTTONS_SIZE_CHARACTERS[1]:                                           # jeśli jeszcze są wolne linijki na przycisku
                if line_number_list[i] <= GLOBAL_CALENDAR_DAY_BUTTONS_SIZE_CHARACTERS[1]-total_lines:                  # jeśli nazwa wydarzenia nie przekracza liczby wolnych linijek na przycisku
                    event_string += wrap_text(sorted_today_event_list[i].name, GLOBAL_CALENDAR_DAY_BUTTONS_SIZE_CHARACTERS[0])      # wrapujemy tekst i doliczamy linijki, ile już zostało zajęte
                    total_lines += line_number_list[i]
                else:
                    event_string += "+"         # jeśli nie starcza linijek to dopisujemy plusik
                    break
            if i == len(sorted_today_event_list)-1 and event_string[-1] == "\n":               # gdy nie ma plusika, po ostatnim wydarzeniu usuwamy enter pozostały z textwrapa
                event_string = event_string[0:-1]
    return event_string

def change_month_prev():                # zmienia na poprzedni miesiąc w kalendarzu;            TO NIE SĄ FUNKCJE DO DODAWANIA/ODEJMOWANIA MIESIĘCY TAK SOBIE !!!
    gv.calendar_month_number = gv.calendar_month_number - 1
    if gv.calendar_month_number == 0:
        gv.calendar_month_number = 12
        gv.calendar_year = gv.calendar_year - 1
    gv.calendar_month_word = month_number_to_word(gv.calendar_month_number)

def change_month_next():                # zmienia na nastepny miesiąc w kalendarzu
    gv.calendar_month_number = gv.calendar_month_number + 1
    if gv.calendar_month_number == 13:
        gv.calendar_month_number = 1
        gv.calendar_year = gv.calendar_year + 1
    gv.calendar_month_word = month_number_to_word(gv.calendar_month_number)

def change_month_current():             # zmienia na obecny miesiąc w kalendarzu (wraca do obecnego miesiąca)
    gv.calendar_month_number = gv.current_month_number
    gv.calendar_year = gv.current_year
    gv.calendar_month_word = month_number_to_word(gv.calendar_month_number)

def read_calendar_events(read_file_name=GLOBAL_CALENDAR_SAVE_FILE_NAME, read_if_reminded=False, autocreate=False) -> list[CalendarEvent]:       # wczytuje i zwraca wszystkie wydarzenia zapisane w pliku
    file_path = get_calendar_file_path(read_file_name)
    if os.path.exists(file_path) == False and autocreate == True:      # sprawdza, czy istnieje podany plik (cała ścieżka) z wydarzeniami kalendarza - jeśli nie, to tworzy taki plik; ma tak robić tylko gdy program nie był używany przez ponad miesiąć i nie został utworzony pewien plik miesięczny przy comiesięcznym sprawdzaniu pierwszego dnia miesiąca 
        print("Nie ma podanego pliku z wydarzeniami kalendarza:")
        print(file_path)
        read_file = open(file_path, "w", encoding='utf-8')
        read_file.close()
    read_file = open(file_path, "r", encoding='utf-8')         # bez ustalenia kodowania są krzaczki, mimo tego że niby jest już w UTF-8
    calendar_event_list = []
    while True:
        line = read_file.readline().strip("\n")                                # usuwa znak końca linii;    raczej nie polecam używać rstrip(), bo to usuwa też spacje na końcu (a przy info mogą być spacje na końcu)
        if not line:
            read_file.close()
            break
        if "__________________________________________________" in line:            # znak początku pozycji w pliku - resetowanie pozostałych rzeczy
            name = ""
            info = ""
            date1 = ""
            date2 = ""
            hour1 = ""
            hour2 = ""
            if_goout = False
            if_deadline = False
            importance = 1
            positivity = 0
            if_constant = False
            line = read_file.readline()                                             # czyta następną linijkę z datą, godzinami i nazwą
            rzeczy = line.split('|')                                                # rodziela linijkę na części
            rzeczy = [x.strip() for x in line.split('|')]                           # usuwa spacje na początku i na końcu (w środku stringa nie :) )
            dates = rzeczy[0]
            if '-' in dates:                                                        # jeśli są podane dwie daty (przedział), to je rozdziela do osobnych zmiennych
                date1 = dates.split('-')[0].strip()                                 # dodatkowo stripuje ze spacji pomiędzy ewentualnymi "-"
                date2 = dates.split('-')[1].strip()
            elif dates != "":                                                       # jeśli nie ma myślnika, a jest cokolwiek, to znaczy że tam jest jedna godzina i jest ona przypisana do hour1
                date1 = dates
            hours = rzeczy[1]
            if '-' in hours:                                                        # jeśli są podane dwie godziny (przedział), to je rozdziela do osobnych zmiennych
                hour1 = hours.split('-')[0].strip()
                hour2 = hours.split('-')[1].strip()
            elif hours != "":                                                       # jeśli nie ma myślnika, a jest cokolwiek, to znaczy że tam jest jedna godzina i jest ona przypisana do hour1
                hour1 = hours
            name = rzeczy[2]
            line = read_file.readline().strip("\n")
            if line == "Info: ":                                                    # jak cała linijka jest równa Info: to znaczy, że nie ma info (xD)
                info = ""
            else:
                info = line.split("Info: ")[1]                                      # usuwa "Info: " ze stringa
            line = read_file.readline().strip("\n")
            rzeczy = [x.strip() for x in line.split('|')]                           # tutaj już możemy wszędzie usunąć spacje
            id = int(rzeczy[0])
            repeat = int(rzeczy[1])
            if rzeczy[2] == "WYJSCIE":
                if_goout = True                             # '=' działa tutaj lepiej niż '=='  :V
            if rzeczy[3] == "ZADANIE":
                if_deadline = True
            positivity = int(rzeczy[4])
            importance = int(rzeczy[5])
            if len(rzeczy)>=7 and int(rzeczy[6]) == 1:                          # czy wydarzenie jest stałe (najpierw sprawdzamy, czy w ogóle jest takie pole, bo stare wydarzenia go nie mają)
                if_constant = True                                          # jak constant ma wartość 1, to zmieniamy pole na True (wcześniej ustawiliśmy domyślną wartość na False)
            if_reminded = False                             # rzeczy[len(rzeczy)-1] (ostatnie) to if_reminded, o ile będziemy tego w ogóle potrzebować
            if read_if_reminded == True:                    # !!! to musi być ostatnie w pliku, bo tego elementu czasem w ogóle nie ma; jak będę cokolwiek nowego dodawał, to to musi być tuż przed
                if rzeczy[len(rzeczy)-1] == "True":                       # podobno nie da się zrzutować stringa na boola, śmieszne
                    if_reminded = True                                  # jak if_reminded ma wartość = True, to zmieniamy pole na True (wcześniej ustawiliśmy domyślną wartość na False)
            event = CalendarEvent(name, date1, date2, hour1, hour2, info, importance, if_goout, if_deadline, positivity, repeat, if_constant, id, if_reminded)
            event.organise_data()
            calendar_event_list.append(event)
    read_file.close()
    return calendar_event_list

def load_calendar_events(read_file_name=GLOBAL_CALENDAR_SAVE_FILE_NAME, read_if_reminded=False) -> list[CalendarEvent]:       # wczytuje i przy okazji wykonuje dodatkowe operacje, w porównaniu do funkcji wyżej
    calendar_events = read_calendar_events(read_file_name)
    if gv.load_calendar_history == True:        # jeśli przycisk "załaduj historię" był wciśnięty
        if gv.calendar_month_number == gv.current_month_number and gv.calendar_year == gv.current_year:     # jak jesteśmy na obecnym miesiącu to wczytujemy z pliku calendar_month_completion.txt
            completed_events = read_calendar_events(GLOBAL_CALENDAR_MONTH_COMPLETION_FILE_NAME)
            calendar_events += completed_events
        else:                                                                                               # jak nie to patrzymy czy jest plik z ukończonymi wydarzeniami z danego miesiąca
            completed_file_name = get_month_calendar_file_name(gv.calendar_month_number, gv.calendar_year)
            if os.path.exists(GLOBAL_CALENDAR_TEXT_FILES_FOLDER_PATH+completed_file_name) == True:           # sprawdza, czy w podanej ścieżke istnieje podany plik
                completed_events = read_calendar_events(completed_file_name)       # pobiera wydarzenia z pliku z wykonanymi wydarzeniami z minionego miesiąca (o ile istnieje) i dołącza do wydarzeń z calendar_save
                calendar_events += completed_events
    return calendar_events

def get_calendar_event_by_id(event_id, file_name=GLOBAL_CALENDAR_SAVE_FILE_NAME) -> CalendarEvent:       # wyszukuje wydarzenie w pliku na podstawie podanego ID i je zwraca
    calendar_events = read_calendar_events(file_name)
    found_event = ""
    for event in calendar_events:
        if str(event.id) == str(event_id):
            found_event = event
    if found_event == "":
        print("Nie udało się znaleźć wydarzenia o podanym ID: ", event_id)                             # tutaj dorobić error loga kiedyś
        return None
    else:
        return found_event

def delete_calendar_event(id, file_name=GLOBAL_CALENDAR_SAVE_FILE_NAME):            # usuwa dane wydarzenie wyszukując je po ID w calendar_save.txt
    lines = ""                                                      # string z całym tekstem, dopisujemy do niego na bieżąco linijki, oprócz tych od eventu, który mamy usunąć
    read_file = open(get_calendar_file_path(file_name), "r", encoding='utf-8')
    while True:
        line = read_file.readline().strip("\n")                                # usuwa znak końca linii
        if not line:
            read_file.close()
            break
        if "__________________________________________________" in line:    # nowe wydarzenie w pliku
            line1 = line                                                    # dla każdego wydarzenia są 4 linijki
            line2 = read_file.readline().strip("\n")
            line3 = read_file.readline().strip("\n")
            line4 = read_file.readline().strip("\n")
            if str(id) not in line4:                                             # jeżeli to nie jest id, którego wydarzenie mamy usunąć, to dopisujemy te 4 linijki do stringa z całym tekstem, trzeba dodać znaki końca linii, bo przedtem je usunęliśmy
                lines = lines+line1+"\n"+line2+"\n"+line3+"\n"+line4+"\n"
            else:                                                           
                rzeczy = line2.split('|')                                    # szybko znajdujemy nazwę wydarzenia, które jest usuwane i zwracamy, dla informacji i logów
                rzeczy = [x.strip() for x in line2.split('|')]
                event_name = rzeczy[2]
    read_file.close()
    write_file = open(get_calendar_file_path(file_name), "w", encoding='utf-8')
    write_file.write(lines)
    write_file.close()
    return event_name

def complete_calendar_event(id, file_name=GLOBAL_CALENDAR_MONTH_COMPLETION_FILE_NAME) -> str:
    event = get_calendar_event_by_id(id)
    event.write_to_file(file_name)
    if event.repeat == 0:
        delete_calendar_event(id)
    else:
        postpone_calendar_event(event, event.repeat)
    return event.name

def edit_calendar_event(old_calendar_event: CalendarEvent, name, date, date_end, hour_start, hour_end, info, importance, if_goout, if_deadline, positivity, repeat, if_constant) -> CalendarEvent:         # edycja wydarzenia - nowe wydarzenie dostaje nowe ID (sprawdzić)
    assign_new_calendar_event_id()
    edited_calendar_event = CalendarEvent(name, date, date_end, hour_start, hour_end, info, importance, if_goout, if_deadline, positivity, repeat, if_constant, gv.calendar_new_event_id)
    edited_calendar_event.organise_data()
    edited_calendar_event.write_to_file(GLOBAL_CALENDAR_SAVE_FILE_NAME)
    edited_calendar_event.write_to_file(GLOBAL_CALENDAR_MONTH_HISTORY_FILE_NAME)
    id_file = open(get_calendar_file_path(GLOBAL_CALENDAR_NEW_ID_FILE_NAME), "w")
    id_file.write(str(gv.calendar_new_event_id+1))
    id_file.close()
    if edited_calendar_event.datetime_format_date != "" and edited_calendar_event.datetime_format_date == datetime.datetime.now().date():
        edited_calendar_event.write_to_file(GLOBAL_CALENDAR_TODAY_FILE_NAME, append=True, write_if_reminded=True)
    delete_calendar_event(old_calendar_event.id)            # podmieniamy jedno wydarzenie na drugie, nowe
    return edited_calendar_event

def postpone_calendar_event(calendar_event: CalendarEvent, postpone_days=1) -> CalendarEvent:               # przesuwa wydarzenie o ileś dni (domyślnie 1, na nastepny dzień)
    #print(calendar_event.name, "typCE:", type(calendar_event.datetime_format_date), calendar_event.datetime_format_date, "typTD:", type(datetime.timedelta(days=postpone_days)), datetime.timedelta(days=postpone_days))
    if calendar_event.if_constant==True:                                # jeśli wydarzenie jest stałe, tzn. nieprzekładalne, to znaczy że musi być konkretnie tego danego dnia miesiąca lub roku
        if postpone_days == 365:
            new_date = datetime_format_date_to_calendar_event_date(calendar_event.datetime_format_date + relativedelta(years=1))    # jak przesuwamy o 365 dni, to dodajemy rok (żeby nie było problemu z przestępnymi); timedelta nie obsługuje lat (wtf)
        elif postpone_days == 30:
            new_date = datetime_format_date_to_calendar_event_date(calendar_event.datetime_format_date + relativedelta(months=1))   # jak przesuwamy o 30 dni to dodajemy miesiąc
        else:
            print("Coś nie halo")
    else:
        if calendar_event.datetime_format_date <= datetime.datetime.now().date():       # jeśli wydarzenie jest dzisiaj lub jest spóźnione, to przenosimy normalnie o tyle ile trzeba lub tyle ile trzeba + zaległość (wyliczone wcześniej)
            new_date = datetime_format_date_to_calendar_event_date(calendar_event.datetime_format_date + datetime.timedelta(days=postpone_days))    # dodaje odpowiednią liczbę dni do daty i zamienia ją w datę, którą można podać do konstruktora
        else:                                                                           # jeśli wydarzenie dopiero będzie, ale już je chcemy przełożyć (bo np wcześniej coś wykonaliśmy), to liczymy od dnia dzisiejszego!
            new_date = datetime_format_date_to_calendar_event_date(datetime.datetime.now().date() + datetime.timedelta(days=postpone_days))
    postponed_calendar_event = edit_calendar_event(calendar_event, calendar_event.name, new_date, calendar_event.date_end, calendar_event.hour_start, calendar_event.hour_end, calendar_event.info, calendar_event.importance, calendar_event.if_goout, calendar_event.if_deadline, calendar_event.positivity, calendar_event.repeat, calendar_event.if_constant)
    return postponed_calendar_event                                                     # ^ przekazujemy wszystkie stare parametry wydarzenia oprócz daty, która jest nowa, odpowiednio przesunięta, i edytujemy wydarzenie

def manage_past_calendar_events():                       # zarządza wydarzeniami, których data już minęła - usuwa je, przekłada na jutro bądź na dzień oddalony o repeat dni
    calendar_events = read_calendar_events()
    postponed_events = []
    deleted_events = []                                                     # ta sekcja jest trudna, trzeba zadecydować, które wydarzenia są to przeniesienia, które do usunięcia, a które można automatycznie wykonać
    decide_events = []
    for event in calendar_events:
        if event.date != "":
            if event.datetime_format_date < datetime.datetime.now().date():       # jeżeli data (dzień) jest starsza niż obecna
                if event.repeat == 0:           # jak wydarzenie się nie powtarza to trzeba podjąć decyzję manualnie, przekazujemy dalej do wyświetlenia
                    # print("nie wiem co z tym zrobić", event.name, event.id)
                    decide_events.append(event)
                    # delete_calendar_event(event.id)                   # początkowo miałem usuwać te wydarzenia, ale może jednak lepiej samemu podejmować o nich decyzje...
                    # deleted_events.append(event)
                    # print("usuwam", event.name, event.id)
                elif event.if_constant == True:                     # automatycznie wykonuje wydarzenie, czyli przekłada je o rok lub miesiąć (lub tydzień jeśli już jest to zaprogramowane?) (bez przełożenia na dzisiaj)
                    complete_calendar_event(event.id)
                else:                           # jak się powtarza, to to pewnie obowiązek domowy, więc przenosimy na dzień dzisiejszy, jak w końcu go wykonamy to wtedy zostanie przeniesiony o repeat (ale to już w complete_calendar_event)
                    days_to_postpone = (datetime.datetime.now().date()-event.datetime_format_date).days         # przenosi o tyle dni, o ile jesteśmy "spóźnieni" z eventem, tj jak event był 3 dni temu, a przekładamy go dopiero dzisiaj, to przekładamy go o 3 dni, na dzisiaj, zawsze na dzisiaj
                    postponed_event = postpone_calendar_event(event, days_to_postpone)              # przekłada na dzisiaj
                    # print("przekładam", event.name, event.id)
                    postponed_events.append(postponed_event)
    return postponed_events, deleted_events, decide_events

def move_month_events(current_month_file, past_month_file):       # przenosi wydarzenia z pliku z historią z teraźniejszego (albo tego co właśnie był) miesiąca do pliku z całą historią
    month_events = read_calendar_events(current_month_file)
    for event in month_events:                          # dla każdego wydarzenia z tego miesiąca najpierw je przenosi do pliku z całą historią, a potem usuwa z pliku z historią z danego miesiąca
        event.write_to_file(past_month_file)
        delete_calendar_event(event.id, current_month_file)

def get_month_calendar_file_name(month: int, year: int, is_completion = True) -> str:      # zwraca nazwę pliku z historią/ukończonymi wydarzeniami z danego miesiąca
    name = "calendar_" + str(year) + "_" + month_number_to_word(month) + ("_completion.txt" if is_completion == True else "_history.txt")
    return name

def calculate_total_points(event_list: list[CalendarEvent]) -> int:         # oblicza sumę punktów wydarzeń przekazanych w parametrze
    sum=0
    for event in event_list:
        sum += event.points
    return sum

def write_monthly_points_to_file(event_list: list[CalendarEvent], points, month=None, year=None, file_name=GLOBAL_CALENDAR_POINTS_FILE_NAME):       # zapisuje punkty z danego miesiąca do pliku z punktami; przy teraźniejszym/najnowszym miesiącu nie podajemy argumentów month i year
    save_file = open(get_calendar_file_path(file_name), "a", encoding='utf-8')
    if month is None:
        month, year = get_previous_month(gv.calendar_month_number, gv.calendar_year)            # chyba jest ok, ale ogólnie funkcja wchodzi tutaj tylko jak calendar_month = current_month
    save_file.write(str(year) + " " + month_number_to_word(month) + " " + str(points) + "\n")
    # print(month, year)
    # print(str(year) + " " + month_number_to_word(month) + " " + str(points) + "\n")
    save_file.close()

def write_points_record_to_file(points: int, month: int, year: int, file_name=GLOBAL_CALENDAR_POINTS_RECORD_FILE_NAME):   # zapisuje rekord punktów z podanego miesiąca do specjalnego pliku
    save_file = open(get_calendar_file_path(file_name), "w", encoding='utf-8')
    save_file.write(str(year) + " " + month_number_to_word(month) + " " + str(points) + "\n")
    save_file.close()

def read_monthly_points(file_name=GLOBAL_CALENDAR_POINTS_FILE_NAME) -> int:                 # odczytuje punkty dla danego miesiąca z pliku z punktami; używa do tego zmiennych globalnych dla miesiąca i roku
    read_file = open(get_calendar_file_path(file_name), "r", encoding='utf-8')
    while True:
        line = read_file.readline().strip("\n")                                # usuwa znak końca linii;
        if not line:
            read_file.close()
            break
        rzeczy = line.split()
        if rzeczy[0] == str(gv.calendar_year) and rzeczy[1] == gv.calendar_month_word:      # czy się zgadza rok, miesiąc; jak tak to zwracamy punkty
            read_file.close()
            return int(rzeczy[2])
    read_file.close()
    return 0                # jak nie znajdzie miesiąca to zwraca 0

def read_record_points(file_name=GLOBAL_CALENDAR_POINTS_RECORD_FILE_NAME) -> int:           # odczytuje rekord punktowy ze specjalnego pliku
    read_file = open(get_calendar_file_path(file_name), "r", encoding='utf-8')
    line = read_file.readline().strip("\n")
    rzeczy = line.split()
    read_file.close()
    return int(rzeczy[2])

def create_calendar_right_click_menu(event_list: list[CalendarEvent]):             # tworzy layout menu pojawiające się po kliknęciu prawym przyciskiem myszy na przycisk;       MUSI DOSTAĆ LISTĘ!!! (nawet składającą się z jednego elementu, dlatego przy przekazywaniu argumentu piszemy [calendar_event])
    menu = ["Menu"]
    row = []
    for event in event_list:
        if event is not []:                 # dla każdego wydarzenia danego dnia (w przypadku kalendarza wydarzeń może być więcej niż 1)
            row.append(event.name)
            row.append(["!Wykonano" if gv.load_calendar_history==True or event.if_constant==True else "Wykonano     \u2611::RCMDONE_"+str(event.id),    # wydarzenie można wykonać, tylko gdy nie jesteśmy w trybie przegląania historii (bo się wszystko zepsuje) oraz jeśli event jest przekładalny (tzn nie jest urodzinami, świętami itd) - nie ma po co wykonywać czegoś takiego
            "!Info" if event.info == "" or event.info == "\n" else "Info         \u2139::RCMINFO_"+str(event.id),                                           # zacieniamy info, jeżeli jest ono puste (brak znaku lub enter)
            "!Godzina" if event.hour_start == "" else ("Godzina      \u231A", [event.hour_start]) if event.hour_end == "" else ("Godzina      \u231A", ["Od: "+event.hour_start, "Do: "+event.hour_end]),
            "Więcej       ->",                                                  # ^ jak jest tylko początkowa to dajemy tego tuple'a                    ^ jak jest też końcowa to dajemy to;    podwójnie zagnieżdzony if :DDD    
                ["Ważność: "+str(event.importance), "Powtarzanie: "+str(event.repeat),              # <- dodatkowe informacje nie potrzebne w pierwszym rzędzie, więc przerzucamy je to submenu "Więcej ->"
                "Pozytywność: "+str(event.positivity), "Wyjście: "+str(event.if_goout),
                "Zadanie: "+str(event.if_deadline),  "Stałe: "+str(event.if_constant),
                "Punkty: "+str(event.points)+GLOBAL_CALENDAR_POINTS_SYMBOL, "ID: "+str(event.id),
                "Wyświetl wszystko::RCMPRINT_"+str(event.id)],
            "!Edytuj" if gv.load_calendar_history==True else "Edytuj       \u270E::RCMEDIT_"+str(event.id),         # za pomocą "::" ukrywamy klucz eventu i potem go można przypasować przy odczytywaniu eventu
            "!Usuń" if gv.load_calendar_history==True else "Usuń         \u2620::RCMDELETE_"+str(event.id)])        #złota_linijka no bo ja pierdole spójrz tylko na to xDDD
    menu.append(row)
    return menu

def popup_calendar_event_info(calendar_event: CalendarEvent, background_color=GLOBAL_POPUP_COLOR):                 # tworzy popup z informacją o wydarzeniu
    tmp = sg.PopupOK("Info:\n"+calendar_event.info, title=calendar_event.name, line_width=GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS, background_color=background_color)        # zobaczyć, czy dodać modal=False, żeby można było wchodzić w interakcję z oknem

def popup_print_calendar_event(calendar_event: CalendarEvent, background_color=GLOBAL_POPUP_COLOR, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):     # tworzy popup z wszystkimi dostępnymi (no prawie) polami wydarzenia (prawie wszystkie, bo niektóre są bardzo nieczytelne)
    info_wrapped = wrap_text(calendar_event.info, GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS)
    layout = [
        [sg.Push(background_color=background_color), sg.Text(calendar_event.name, background_color=background_color, font=font1), sg.Push(background_color=background_color)],
        [sg.Text("ID:\t\t\t\t"+str(calendar_event.id), background_color=background_color, font=font2)],
        [sg.Text("date:\t\t\t\t"+str(calendar_event.date), background_color=background_color, font=font2)],
        [sg.Text("date_end:\t\t\t"+str(calendar_event.date_end), background_color=background_color, font=font2)],
        [sg.Text("length_days:\t\t\t"+str(calendar_event.length_days), background_color=background_color, font=font2)],
        #[sg.Text("datetime_format_dates_list:\t"+str(calendar_event.datetime_format_dates_list), background_color=background_color, font=font2)],      # w przypadku wielodniowych wydarzeń będzie przeskakiwać do następnych linijek i będzie brzydko, poza tym no raczej działa
        [sg.Text("date_difference:\t\t"+str(calendar_event.date_difference), background_color=background_color, font=font2)],
        [sg.Text("hour_start:\t\t\t"+str(calendar_event.hour_start), background_color=background_color, font=font2)],
        [sg.Text("hour_end:\t\t\t"+str(calendar_event.hour_end), background_color=background_color, font=font2)],
        [sg.Text("datetime_format_hour_sort:\t"+str(calendar_event.datetime_format_hour_sort), background_color=background_color, font=font2)],
        [sg.Text("date_format_reminder_hour:\t"+str(calendar_event.datetime_format_reminder_hour), background_color=background_color, font=font2)],
        [sg.Text("importance:\t\t\t"+str(calendar_event.importance), background_color=background_color, font=font2)],
        #[sg.Text("importance_inverted:\t\t"+str(calendar_event.importance_inverted), background_color=background_color, font=font2)],                  # come on, na pewno jest ok
        [sg.Text("repeat:\t\t\t\t"+str(calendar_event.repeat), background_color=background_color, font=font2)],
        [sg.Text("positivity:\t\t\t"+str(calendar_event.positivity), background_color=background_color, font=font2)],
        [sg.Text("if_goout:\t\t\t"+str(calendar_event.if_goout), background_color=background_color, font=font2)],
        [sg.Text("if_deadline:\t\t\t"+str(calendar_event.if_deadline), background_color=background_color, font=font2)],
        [sg.Text("if_constant:\t\t\t"+str(calendar_event.if_constant), background_color=background_color, font=font2)],
        [sg.Text("if_reminded:\t\t\t"+str(calendar_event.if_reminded), background_color=background_color, font=font2)],
        [sg.Text("show_on_calendar:\t\t"+str(calendar_event.show_on_calendar), background_color=background_color, font=font2)],
        [sg.Text("calendar_line_number:\t\t"+str(calendar_event.calendar_line_number), background_color=background_color, font=font2)],
        [sg.Text("optimal_score:\t\t\t"+str(calendar_event.optimal_score), background_color=background_color, font=font2)],
        [sg.Text("color:\t\t\t\t"+str(calendar_event.color), background_color=background_color, font=font2)],
        [sg.Text("points:\t\t\t\t"+str(calendar_event.points), background_color=background_color, font=font2)],
        [sg.Text("Info:\n"+str(info_wrapped), background_color=background_color, font=font2)],
        [sg.Push(background_color=background_color), sg.Button("OK", key='-POPUPPRINTEVENTBUTTONOK-'), sg.Push(background_color=background_color)]
    ]
    popup_event, popup_values = sg.Window('Wszystkie informacje o wydarzeniu \"'+calendar_event.name+'\"', layout, modal=True, background_color=background_color, disable_close=True).read(close=True)  # zwracanie czegokolwiek chyba i tak niepotrzebne
    return popup_event

def popup_edit_calendar_event(calendar_event: CalendarEvent, background_color=GLOBAL_POPUP_COLOR):                 # tworzy popup z możliwością edycji wydarzenia (interfejs taki sam jak w kalendarzu)
    layout = [
        [sg.Push(background_color=background_color), sg.Image(data = get_avatar_byte_value(GLOBAL_AVATAR_EDIT_BACKGROUND), pad=((0, 0), 3)), sg.Push(background_color=background_color)],
        [sg.Text('Edytuj wydarzenie:', background_color=background_color)],
        [sg.Text('Data:     Od:', background_color=background_color), sg.Input(calendar_event.date, key='-POPUPEDITINPUTDATE-', size=(10, 1)), sg.Text(' Do:', background_color=background_color), sg.Input(calendar_event.date_end, key='-POPUPEDITINPUTDATEEND-', size=(10, 1)), sg.Push(background_color=background_color), sg.Checkbox("Stałe", key='-POPUPEDITCONSTANT-', default=calendar_event.if_constant, background_color=background_color)],
        [sg.Text('Godzina:       Od:', background_color=background_color), sg.Input(calendar_event.hour_start, key='-POPUPEDITINPUTHOUR1-', size=(5, 1)), sg.Text('      Do:', background_color=background_color), sg.Input(calendar_event.hour_end, key='-POPUPEDITINPUTHOUR2-', size=(5, 1))],
        [sg.Text('Nazwa:', background_color=background_color), sg.Input(calendar_event.name, key='-POPUPEDITINPUTNAME-', size=(GLOBAL_CALENDAR_EVENT_NAME_MAX_LENGTH, 1))],
        [sg.Text('Info:', background_color=background_color), sg.Multiline(calendar_event.info, key='-POPUPEDITINPUTINFO-', size=(40, 3), expand_x=True)],
        [sg.Text('Ważność:', background_color=background_color), sg.Radio('1', group_id='PopupEditRadioCalendarImportance', key='-POPUPEDITRADIOIMPORTANCE1-', default=(True if calendar_event.importance==1 else False), background_color=background_color), sg.Radio('2', group_id='PopupEditRadioCalendarImportance', key='-POPUPEDITRADIOIMPORTANCE2-', default=(True if calendar_event.importance==2 else False), background_color=background_color), sg.Radio('3', group_id='PopupEditRadioCalendarImportance', key='-POPUPEDITRADIOIMPORTANCE3-', default=(True if calendar_event.importance==3 else False), background_color=background_color), sg.Radio('4', group_id='PopupEditRadioCalendarImportance', key='-POPUPEDITRADIOIMPORTANCE4-', default=(True if calendar_event.importance==4 else False), background_color=background_color), sg.Push(background_color=background_color), sg.Text('Pozytywność:', background_color=background_color), sg.Radio('+', group_id='PopupEditRadioCalendar', key='-POPUPEDITRADIOPOSITIVE-', background_color=background_color, default = True if calendar_event.positivity==1 else False), sg.Radio('+/-', group_id='PopupEditRadioCalendar', key='-POPUPEDITRADIONEUTRAL-', background_color=background_color, default = True if calendar_event.positivity==0 else False), sg.Radio('-', group_id='PopupEditRadioCalendar', key='-POPUPEDITRADIONEGATIVE-', background_color=background_color, default = True if calendar_event.positivity==-1 else False)],
        [sg.Text('Powtarzaj co:', background_color=background_color), sg.Input(calendar_event.repeat, key='-POPUPEDITINPUTREPEAT-', size=(3, 1)), sg.Checkbox('Wyjście z domu', key='-POPUPEDITCHECKBOXGOOUT-', background_color=background_color, default = True if calendar_event.if_goout==True else False), sg.Checkbox('Termin to deadline', key='-POPUPEDITCHECKBOXDEADLINE-', background_color=background_color, default = True if calendar_event.if_deadline==True else False)],
        [sg.Push(background_color=background_color), sg.Button("Zamień", key='-POPUPEDITBUTTONEDITCALENDAR-'), sg.Button("Anuluj", key='-POPUPEDITBUTTONCANCELCALENDAR-'), sg.Push(background_color=background_color)]
    ]
    popup_event, popup_values = sg.Window('Edytowanie wydarzenia \"'+calendar_event.name+'\"', layout, modal=True, background_color=background_color, disable_close=True).read(close=True)
    return popup_event, popup_values
