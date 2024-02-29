from functions import *

def create_monitor_layout(theme):                       # tworzy layout zakładki monitor
    monitor_layout = [
        [sg.Canvas(key="-MONITORCANVAS-"),],
        [sg.Text("Tryb wykresu:    "), sg.Radio('Użycie ', group_id='RadioMonitorPlotType', key='-RADIOMONITORPLOTUSAGE-', default=False, enable_events=True), sg.Radio('Temperatura', group_id='RadioMonitorPlotType', key='-RADIOMONITORPLOTTEMPERATURE-', default=True, enable_events=True), sg.Radio('Wentylatory', group_id='RadioMonitorPlotType', key='-RADIOMONITORPLOTFANSPEED-', default=False, enable_events=True)],
        #[sg.Text('Milliseconds per sample:'), sg.Slider((0,30), default_value=15, orientation='h', key='-DELAY-')],
        #[sg.Text('Pixels per sample:'), sg.Slider((1,30), default_value=graph_step_size, orientation='h', key='-STEP-SIZE-')],
        [sg.Text("Procesor:        "), sg.Checkbox("XXXX %", key='-CHECKBOXMONITORSHOWCPUUSAGE-', default=True, text_color=GLOBAL_CPU_USAGE_COLOR, enable_events=True), sg.Checkbox("XXXX\u00B0C" + "   XXXX\u00B0C", key='-CHECKBOXMONITORSHOWCPUTEMP-', default=True, text_color=GLOBAL_CPU_TEMP_COLOR, enable_events=True)],
        [sg.Text("Karta graficzna: "), sg.Checkbox("XXXX %", key='-CHECKBOXMONITORSHOWGPUUSAGE-', default=True, text_color=GLOBAL_GPU_USAGE_COLOR, enable_events=True), sg.Checkbox("XXXX\u00B0C" + "   XXXX\u00B0C", key='-CHECKBOXMONITORSHOWGPUTEMP-', default=True, text_color=GLOBAL_GPU_TEMP_COLOR, enable_events=True)],
        [sg.Text("Wentylatory:     "), sg.Checkbox("XXXX %", key='-CHECKBOXMONITORSHOWFANUSAGE-', default=True, text_color=GLOBAL_FAN_USAGE_COLOR, enable_events=True)],
        [sg.Text("   " + GLOBAL_FAN_SYMBOL + "   CPU FAN: "), sg.Checkbox("XXXX %", key='-CHECKBOXMONITORSHOWFAN2USAGE-', default=False, text_color=GLOBAL_FAN2_USAGE_COLOR, enable_events=True), sg.Checkbox("XXXX RPM", key='-CHECKBOXMONITORSHOWFAN2SPEED-', default=True, text_color=GLOBAL_FAN2_SPEED_COLOR, enable_events=True)],
        [sg.Text("   " + GLOBAL_FAN_SYMBOL + " BOOST FAN: "), sg.Checkbox("XXXX %", key='-CHECKBOXMONITORSHOWFAN5USAGE-', default=False, text_color=GLOBAL_FAN5_USAGE_COLOR, enable_events=True), sg.Checkbox("XXXX RPM", key='-CHECKBOXMONITORSHOWFAN5SPEED-', default=True, text_color=GLOBAL_FAN5_SPEED_COLOR, enable_events=True)],
        [sg.Text("   " + GLOBAL_FAN_SYMBOL + " FRONT FAN: "), sg.Checkbox("XXXX %", key='-CHECKBOXMONITORSHOWFAN6USAGE-', default=False, text_color=GLOBAL_FAN6_USAGE_COLOR, enable_events=True), sg.Checkbox("XXXX RPM", key='-CHECKBOXMONITORSHOWFAN6SPEED-', default=True, text_color=GLOBAL_FAN6_SPEED_COLOR, enable_events=True)],
        [sg.Text("   " + GLOBAL_FAN_SYMBOL + "  BACK FAN: "), sg.Checkbox("XXXX %", key='-CHECKBOXMONITORSHOWFAN3USAGE-', default=False, text_color=GLOBAL_FAN3_USAGE_COLOR, enable_events=True), sg.Checkbox("XXXX RPM", key='-CHECKBOXMONITORSHOWFAN3SPEED-', default=True, text_color=GLOBAL_FAN3_SPEED_COLOR, enable_events=True)],
        [sg.Text("RAM:             "), sg.Checkbox("XXXX %  /  32 GB  ", key='-CHECKBOXMONITORSHOWRAMUSAGE-', default=False, text_color=GLOBAL_RAM_USAGE_COLOR, enable_events=True)],
        [sg.Button("Update", key="-BUTTONMONITORUPDATE-"), sg.Push(), sg.Button("Wyświetl sensory", key="-BUTTONMONITORPRINTSENSORS-")],
        [sg.Push(),  sg.Button("Zapisz do pliku", key="-BUTTONMONITORSAVEDATATOFILE-")]
        # [sg.Push(), sg.Button("Włącz Monitor Popup", key="-BUTTONMONITORPOPUPTOGGLE-", size=(13, 2)), sg.VPush()],
        # [sg.VPush()]
    ]
    return monitor_layout

def initialize_computer_sensors():                      # inicjalizuje sensory, używa zewnętrznej biblioteki do tego, która została pobrana zzewnątrz
    #sys_path.append(getcwd()+"/packages/"+GLOBAL_PACKAGES_PATH)                # inne sposoby na dodanie dodatkowej ścieżki, w której będą szukane pliki .dll; ten sposób z bezpośrednią ścieżką wydaje się być najwygodniejszy
    #sys_path.append("C:/Users/matik/Desktop/python/BATI/versions/1.1.2/packages")
    
    if GLOBAL_IS_DEV_VERSION == True:                   # w wersji deweloperskiej paczki są przechowywane bezpośrednio razem ze skryptami (ponieważ odpalany jest plik main.py); w wersji normalnej pliki .dll będą w dedykowanym folderze
        clr.AddReference("OpenHardwareMonitorLib")      # e.g. clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib'), without .dll
    else:
        sys_path.append("./packages")                   # jeśli spróbuje się to zrobić w 1 linijce, to program się wywala, funkcja AddReference nie czyta ścieżek chyba
        clr.AddReference("OpenHardwareMonitorLib")    
    from OpenHardwareMonitor import Hardware

    gv.computer_data = Hardware.Computer()
    gv.computer_data.MainboardEnabled = True   # info o płycie głównej - jeśli nie ma praw administratora to nie widać w ogóle pola SubHardware
    gv.computer_data.CPUEnabled = True # get the Info about CPU
    gv.computer_data.GPUEnabled = True # get the Info about GPU
    gv.computer_data.RAMEnabled = True
    gv.computer_data.HDDEnabled = True
    gv.computer_data.Open()

    if len(gv.computer_data.Hardware[0].SubHardware) == 0:             # podzespoły płyty głównej są dostępne do odczytu tylko, gdy program się uruchomi z prawami administratora
        gv.run_as_administrator = False                 # ustalanie zmiennej globalnej na podstawie tego odczytu
    else:
        gv.run_as_administrator = True
    
    # updating sensors
    gv.computer_data.Hardware[1].Update()                              # nie ma sensu nieczego sprawdzać przed update'm, brakuje odczytu pewnych sensorów
    gv.computer_data.Hardware[2].Update()
    gv.computer_data.Hardware[3].Update()
    gv.computer_data.Hardware[4].Update()
    if gv.run_as_administrator:
        gv.computer_data.Hardware[0].SubHardware[0].Update()           # tutaj jest jeszcze element Subhardware -> patrz wypis OpenHardwareMonitor.exe albo OpenHardwareMonitorRaport.exe
    
    # sprawdzanie liczby dostępnych sensorów po update'cie (MB jest na końcu, bo to special case)       (DEBUG)
    #                                               # bez admina            # z adminem
    # print(len(gv.computer_data.Hardware[1].Sensors))               # 7                       24
    # print(len(gv.computer_data.Hardware[2].Sensors))               # 3                       3
    # print(len(gv.computer_data.Hardware[3].Sensors))               # 10                      10
    # print(len(gv.computer_data.Hardware[4].Sensors))               # 1                       2
    # print(len(gv.computer_data.Hardware[0].SubHardware))           # 0                       1
    # if gv.run_as_administrator:
    #     print(len(gv.computer_data.Hardware[0].SubHardware[0].Sensors))    # crash           29

    # if gv.run_as_administrator:
    #     for a in range(0, len(gv.computer_data.Hardware[0].SubHardware[0].Sensors)):
    #         print(str(gv.computer_data.Hardware[0].SubHardware[0].Sensors[a].Identifier), gv.computer_data.Hardware[0].SubHardware[0].Sensors[a].get_Value(), a)
    # for a in range(0, len(gv.computer_data.Hardware[1].Sensors)):
    #     print(str(gv.computer_data.Hardware[1].Sensors[a].Identifier), gv.computer_data.Hardware[1].Sensors[a].get_Value(), a)
    # for a in range(0, len(gv.computer_data.Hardware[2].Sensors)):
    #     print(str(gv.computer_data.Hardware[2].Sensors[a].Identifier), gv.computer_data.Hardware[2].Sensors[a].get_Value(), a)
    # for a in range(0, len(gv.computer_data.Hardware[3].Sensors)):
    #     print(str(gv.computer_data.Hardware[3].Sensors[a].Identifier), gv.computer_data.Hardware[3].Sensors[a].get_Value(), a)
    # for a in range(0, len(gv.computer_data.Hardware[4].Sensors)):
    #     print(str(gv.computer_data.Hardware[4].Sensors[a].Identifier), gv.computer_data.Hardware[4].Sensors[a].get_Value(), a)

def get_basic_monitor_values():                         # zwraca podstawowe wartości sensorów (6 wartości)
    # updating sensors
    gv.computer_data.Hardware[1].Update()
    gv.computer_data.Hardware[2].Update()
    gv.computer_data.Hardware[3].Update()
    gv.computer_data.Hardware[4].Update()
    if gv.run_as_administrator:
        gv.computer_data.Hardware[0].SubHardware[0].Update()

    # cpu_load_avg = (gv.computer_data.Hardware[1].Sensors[0].get_Value() + gv.computer_data.Hardware[1].Sensors[1].get_Value() + gv.computer_data.Hardware[1].Sensors[2].get_Value() + gv.computer_data.Hardware[1].Sensors[3].get_Value() + gv.computer_data.Hardware[1].Sensors[4].get_Value() + gv.computer_data.Hardware[1].Sensors[5].get_Value())/6
    # LOAD0 to jest TOTAL, a LOAD0 ma indeks 6, a nie 0, jak było tutaj powyżej wpisane ja pierdole; wartości te same, nie ma sensu liczyć ręcznie
    
    default_value = -1
    if gv.run_as_administrator:
        cpu_load_total = gv.computer_data.Hardware[1].Sensors[6].get_Value()
        cpu_temp1 = gv.computer_data.Hardware[1].Sensors[15].get_Value()
        cpu_temp2 = gv.computer_data.Hardware[1].Sensors[16].get_Value()
        gpu_load = gv.computer_data.Hardware[3].Sensors[7].get_Value()          # core load
        # gpu_load2 = gv.computer_data.Hardware[3].Sensors[8].get_Value()       # memory load
        gpu_temp1 = gv.computer_data.Hardware[3].Sensors[0].get_Value()
        gpu_temp2 = gv.computer_data.Hardware[3].Sensors[1].get_Value()
        fan2 = gv.computer_data.Hardware[0].SubHardware[0].Sensors[25].get_Value()      # CPU, Noctua NH-U12S redux - max 1700 RPM, w praktyce też max 1700 RPM; CPU FAN1
        fan3 = gv.computer_data.Hardware[0].SubHardware[0].Sensors[26].get_Value()      # wentylator domyślny, przód albo tył, nie wiadomo - max 1000 RPM, w praktyce max 940 RPM; SYS FAN1
        fan5 = gv.computer_data.Hardware[0].SubHardware[0].Sensors[27].get_Value()      # przód kolorowy, Noctua NF-A14 - max 1500 RPM, w praktyce max 1400 RPM; SYS FAN3
        fan6 = gv.computer_data.Hardware[0].SubHardware[0].Sensors[28].get_Value()      # wentylator domyślny, przód albo tył, nie wiadomo - max 1000 RPM, w praktyce max 940 RPM; SYS FAN4
        fan2_percentage = fan2*100/GLOBAL_FAN2_MAX_SPEED_MEASURED
        fan3_percentage = fan3*100/GLOBAL_FAN3_MAX_SPEED_MEASURED
        fan5_percentage = fan5*100/GLOBAL_FAN5_MAX_SPEED_MEASURED
        fan6_percentage = fan6*100/GLOBAL_FAN6_MAX_SPEED_MEASURED
        fan_percentage_avg = (fan3_percentage + fan5_percentage + fan6_percentage) / 3  # wentylatora CPU nie liczymy do średniej, bo on zwykle kręci się o wiele spokojniej!
    else:
        cpu_load_total = gv.computer_data.Hardware[1].Sensors[6].get_Value()
        cpu_temp1 = default_value
        cpu_temp2 = default_value
        gpu_load = gv.computer_data.Hardware[3].Sensors[7].get_Value()
        gpu_temp1 = gv.computer_data.Hardware[3].Sensors[0].get_Value()
        gpu_temp2 = gv.computer_data.Hardware[3].Sensors[1].get_Value()
        fan_percentage_avg = 0
    ram_usage = gv.computer_data.Hardware[2].Sensors[1].get_Value()
    return cpu_load_total, max(cpu_temp1, cpu_temp2), gpu_load, max(gpu_temp1, gpu_temp2), fan_percentage_avg, ram_usage

def get_advanced_monitor_values():                      # zwraca więcej odczytów sensorów (17 wartości)         !!!!! USAGE jest w %, LOAD jest w GB, SPEED jest w RPM
    # updating sensors
    gv.computer_data.Hardware[1].Update()
    gv.computer_data.Hardware[2].Update()
    gv.computer_data.Hardware[3].Update()
    gv.computer_data.Hardware[4].Update()
    if gv.run_as_administrator:
        gv.computer_data.Hardware[0].SubHardware[0].Update()
    
    default_value = -1              # wartość, która jest przypisywana w przypadku braku dostępu do sensorów
    if gv.run_as_administrator:                         # gdy program został uruchomiony w trybie administratora
        cpu_usage_total = gv.computer_data.Hardware[1].Sensors[6].get_Value()   # wartość w %
        cpu_temp1 = gv.computer_data.Hardware[1].Sensors[15].get_Value()
        cpu_temp2 = gv.computer_data.Hardware[1].Sensors[16].get_Value()
        gpu_usage = gv.computer_data.Hardware[3].Sensors[7].get_Value()          # core usage
        # gpu_usage2 = gv.computer_data.Hardware[3].Sensors[8].get_Value()       # memory usage
        gpu_temp1 = gv.computer_data.Hardware[3].Sensors[0].get_Value()
        gpu_temp2 = gv.computer_data.Hardware[3].Sensors[1].get_Value()
        # gpu_fan = gv.computer_data.Hardware[3].Sensors[3].get_Value()         # zawsze wskazuje 0 ???
                                                                                        # !!!!! WYJAŚNIENIE KTÓRE WENTYLATORY SĄ KTÓRE!!!
        fan2 = gv.computer_data.Hardware[0].SubHardware[0].Sensors[25].get_Value()      # CPU, Noctua NH-U12S redux - max 1700 RPM, w praktyce też max 1700 RPM; CPU FAN1
        fan3 = gv.computer_data.Hardware[0].SubHardware[0].Sensors[26].get_Value()      # wentylator domyślny, przód albo tył, nie wiadomo - max 1000 RPM, w praktyce max 940 RPM; SYS FAN1; strzelam że to tylny, bo ma numerek slota obok fana CPU
        fan5 = gv.computer_data.Hardware[0].SubHardware[0].Sensors[27].get_Value()      # przód kolorowy, "boost fan" Noctua NF-A14 - max 1500 RPM, w praktyce max 1400 RPM; SYS FAN3
        fan6 = gv.computer_data.Hardware[0].SubHardware[0].Sensors[28].get_Value()      # wentylator domyślny, przód albo tył, nie wiadomo - max 1000 RPM, w praktyce max 850 RPM; SYS FAN4, strzelam że to przedni, bo ma numerek slotu obok boost fana
        fan2_percentage = fan2*100/GLOBAL_FAN2_MAX_SPEED_MEASURED
        fan3_percentage = fan3*100/GLOBAL_FAN3_MAX_SPEED_MEASURED
        fan5_percentage = fan5*100/GLOBAL_FAN5_MAX_SPEED_MEASURED
        fan6_percentage = fan6*100/GLOBAL_FAN6_MAX_SPEED_MEASURED
        fan_percentage_avg = (fan3_percentage + fan5_percentage + fan6_percentage) / 3  # wentylatora CPU nie liczymy do średniej, bo on zwykle kręci się o wiele spokojniej!
    else:
        cpu_usage_total = gv.computer_data.Hardware[1].Sensors[6].get_Value()
        cpu_temp1 = default_value
        cpu_temp2 = default_value
        gpu_usage = gv.computer_data.Hardware[3].Sensors[7].get_Value()
        gpu_temp1 = gv.computer_data.Hardware[3].Sensors[0].get_Value()
        gpu_temp2 = gv.computer_data.Hardware[3].Sensors[1].get_Value()
        fan2 = default_value
        fan3 = default_value
        fan5 = default_value
        fan6 = default_value
        fan2_percentage = default_value
        fan3_percentage = default_value
        fan5_percentage = default_value
        fan6_percentage = default_value
        fan_percentage_avg = default_value
    ram_usage = gv.computer_data.Hardware[2].Sensors[0].get_Value()
    ram_value = gv.computer_data.Hardware[2].Sensors[1].get_Value()

    # dopisywanie danych do list z wartościami, które będą wyświetlone w funkcji update_monitor
    if len(gv.monitor_timestamps) > GLOBAL_MONITOR_MAX_PLOT_LENGTH:
        gv.monitor_data["Time"].pop(0)
        gv.monitor_data["CPU_temp"].pop(0)
        gv.monitor_data["CPU_usage"].pop(0)
        gv.monitor_data["GPU_temp"].pop(0)
        gv.monitor_data["GPU_usage"].pop(0)
        gv.monitor_data["RAM_usage"].pop(0)
        gv.monitor_data["FAN_usage"].pop(0)
        gv.monitor_data["FAN2_usage"].pop(0)
        gv.monitor_data["FAN3_usage"].pop(0)
        gv.monitor_data["FAN5_usage"].pop(0)
        gv.monitor_data["FAN6_usage"].pop(0)
        gv.monitor_data["FAN2_speed"].pop(0)
        gv.monitor_data["FAN3_speed"].pop(0)
        gv.monitor_data["FAN5_speed"].pop(0)
        gv.monitor_data["FAN6_speed"].pop(0)
        gv.monitor_timestamps.pop(0)
    gv.monitor_data["Time"].append(datetime.datetime.now().strftime("%H:%M:%S"))
    gv.monitor_data["CPU_temp"].append(max(cpu_temp1, cpu_temp2))
    gv.monitor_data["CPU_usage"].append(cpu_usage_total)
    gv.monitor_data["GPU_temp"].append(max(gpu_temp1, gpu_temp2))
    gv.monitor_data["GPU_usage"].append(gpu_usage)
    gv.monitor_data["RAM_value"].append(ram_value)
    gv.monitor_data["RAM_usage"].append(ram_usage)
    gv.monitor_data["FAN_usage"].append(fan_percentage_avg)
    gv.monitor_data["FAN2_usage"].append(fan2_percentage)
    gv.monitor_data["FAN3_usage"].append(fan3_percentage)
    gv.monitor_data["FAN5_usage"].append(fan5_percentage)
    gv.monitor_data["FAN6_usage"].append(fan6_percentage)
    gv.monitor_data["FAN2_speed"].append(fan2)
    gv.monitor_data["FAN3_speed"].append(fan3)
    gv.monitor_data["FAN5_speed"].append(fan5)
    gv.monitor_data["FAN6_speed"].append(fan6)
    gv.monitor_timestamps.append(datetime.datetime.now())

    # oprócz tego i tak zwracamy wartości, żeby je wyświetlić jako tekst pod wykresem
    return cpu_usage_total, cpu_temp1, cpu_temp2, gpu_usage, gpu_temp1, gpu_temp2, fan_percentage_avg, fan2_percentage, fan3_percentage, fan5_percentage, fan6_percentage, fan2, fan3, fan5, fan6, ram_usage, ram_value

def create_monitor_plot():                      # tworzy wykres dla monitora z wartościami sensorów w czasie
    axes = gv.monitor_plot_figure.axes                                                                              # mamy tylko jeden obiekt axes, bo mamy tylko jeden subplot, ale tak jest lepiej to zrobić -> większa kontrola i więcej metod
    axes[0].clear()                                                                                                 # czyści wszystkie wykresy
    series_count = 0
    if gv.monitor_view_mode == "temp":                                                                              # rysowanie danych na wykresie dzielimy na różne tryby wykresu: temperaturowy, użycia i prędkości wentylatorów
        if gv.monitor_dict["CPU_temp"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["CPU_temp"], '-', color=GLOBAL_CPU_TEMP_COLOR, label="Procesor")         # w tym momencie nic jeszcze się nie pojawia na wykresie, można potem dodawać legendy, osie itd.
            series_count+=1
        if gv.monitor_dict["GPU_temp"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["GPU_temp"], '-', color=GLOBAL_GPU_TEMP_COLOR, label="Karta graficzna")
            series_count+=1
        axes[0].set_ylabel("Temperatura [\u00B0C]")                                                                 # ustawiamy odpowiedni opis osi Y
    elif gv.monitor_view_mode == "usage":
        if gv.monitor_dict["CPU_usage"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["CPU_usage"], '-', color=GLOBAL_CPU_USAGE_COLOR, label="CPU")
            series_count+=1
        if gv.monitor_dict["GPU_usage"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["GPU_usage"], '-', color=GLOBAL_GPU_USAGE_COLOR, label="GPU")
            series_count+=1
        if gv.monitor_dict["RAM_usage"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["RAM_usage"], '-', color=GLOBAL_RAM_USAGE_COLOR, label="RAM")
            series_count+=1
        if gv.monitor_dict["FAN_usage"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["FAN_usage"], '-', color=GLOBAL_FAN_USAGE_COLOR, label="Fan_average")
            series_count+=1
        if gv.monitor_dict["FAN2_usage"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["FAN2_usage"], '-', color=GLOBAL_FAN2_USAGE_COLOR, label="Fan_CPU")
            series_count+=1
        if gv.monitor_dict["FAN6_usage"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["FAN6_usage"], '-', color=GLOBAL_FAN6_USAGE_COLOR, label="Fan_Front")
            series_count+=1
        if gv.monitor_dict["FAN5_usage"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["FAN5_usage"], '-', color=GLOBAL_FAN5_USAGE_COLOR, label="Fan_Boost")
            series_count+=1
        if gv.monitor_dict["FAN3_usage"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["FAN3_usage"], '-', color=GLOBAL_FAN3_USAGE_COLOR, label="Fan_Back")
            series_count+=1
        axes[0].set_ylabel("Użycie [%]")
    else:
        if gv.monitor_dict["FAN2_speed"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["FAN2_speed"], '-', color=GLOBAL_FAN2_USAGE_COLOR, label="Fan_CPU")
            series_count+=1
        if gv.monitor_dict["FAN5_speed"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["FAN5_speed"], '-', color=GLOBAL_FAN5_USAGE_COLOR, label="Fan_Boost")
            series_count+=1
        if gv.monitor_dict["FAN6_speed"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["FAN6_speed"], '-', color=GLOBAL_FAN6_USAGE_COLOR, label="Fan_Front")
            series_count+=1
        if gv.monitor_dict["FAN3_speed"]:
            axes[0].plot(gv.monitor_timestamps, gv.monitor_data["FAN3_speed"], '-', color=GLOBAL_FAN3_USAGE_COLOR, label="Fan_Back")
            series_count+=1
        axes[0].set_ylabel("Prędkość wentylatora [RPM]")
    if series_count > 4:
        axes[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.18), fancybox=True, shadow=False, ncol=4)         # bbox_to_anchor przesuwa legendę w dokładne miejsce, nawet poza wykres (na górę canvasa)
    else:
        axes[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.14), fancybox=True, shadow=False, ncol=4)         # 1.18 i 1.14 to wartości dobrane tak, by legenda była w ładnym miejscu (można się pobawić)
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))                                                # formatuje oś X w podany sposób
    axes[0].set_xlabel("Czas")

    gv.figure_canvas_agg.draw()                                                                                     # moment rysowania
    gv.figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)                                    # to chyba umieszcza rysunek na canvasie w okienku PySimpleGUI

def get_sensor_name(full: str) -> str:          # zwraca nazwę sensora czytelną dla człowieka
    if "ram" in full:
        return full.split('/', 2)[2].ljust(10)            # jeśli jest człon "ram", to wycina część po drugim wystąpieniu slasha
    else:
        return full.split('/', 3)[3].ljust(10)            # w pozostałych przypadkach potrzebujemy części po trzecim slashu

def popup_print_computer_sensors(background_color=GLOBAL_POPUP_COLOR, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):     # tworzy popup z wszystkimi dostępnymi (no prawie) polami wydarzenia (prawie wszystkie, bo niektóre są bardzo nieczytelne)
    #info_wrapped = wrap_text(calendar_event.info, GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS)
    layout = []
    scrollbar_layout = []
    if gv.run_as_administrator == False:
        info_text = wrap_text("Uwaga! Ze względu na to, że program nie został uruchomiony w trybie administratora, liczba sensorów jest ograniczona.", GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS/2)
        layout.append([sg.Push(background_color=background_color), sg.Text(info_text, background_color=background_color, font=font1), sg.Push(background_color=background_color)])
        layout.append([sg.Text("", background_color=background_color, font=font2)])
    else:
        scrollbar_layout.append([sg.Text("Płyta główna:", background_color=background_color, font=font1)])
        for a in range(0, len(gv.computer_data.Hardware[0].SubHardware[0].Sensors)):
            scrollbar_layout.append([sg.Text(str(a)+"\t"+get_sensor_name(str(gv.computer_data.Hardware[0].SubHardware[0].Sensors[a].Identifier))+"\t\t"+str(round(gv.computer_data.Hardware[0].SubHardware[0].Sensors[a].get_Value(), 2)), background_color=background_color, font=font2)])       # dużo się tutaj dzieje, ogólnie formatowanie tekstu i wartości każdego z sensorów
        scrollbar_layout.append([sg.Text("", background_color=background_color, font=font2)])
    scrollbar_layout.append([sg.Text("Procesor:", background_color=background_color, font=font1)])
    for a in range(0, len(gv.computer_data.Hardware[1].Sensors)):
        scrollbar_layout.append([sg.Text(str(a)+"\t"+get_sensor_name(str(gv.computer_data.Hardware[1].Sensors[a].Identifier))+"\t\t"+str(round(gv.computer_data.Hardware[1].Sensors[a].get_Value(), 2)), background_color=background_color, font=font2)])
    scrollbar_layout.append([sg.Text("", background_color=background_color, font=font2)])
    scrollbar_layout.append([sg.Text("RAM:", background_color=background_color, font=font1)])
    for a in range(0, len(gv.computer_data.Hardware[2].Sensors)):
        scrollbar_layout.append([sg.Text(str(a)+"\t"+get_sensor_name(str(gv.computer_data.Hardware[2].Sensors[a].Identifier))+"\t\t"+str(round(gv.computer_data.Hardware[2].Sensors[a].get_Value(), 2)), background_color=background_color, font=font2)])
    scrollbar_layout.append([sg.Text("", background_color=background_color, font=font2)])
    scrollbar_layout.append([sg.Text("Karta graficzna:", background_color=background_color, font=font1)])
    for a in range(0, len(gv.computer_data.Hardware[3].Sensors)):
        scrollbar_layout.append([sg.Text(str(a)+"\t"+get_sensor_name(str(gv.computer_data.Hardware[3].Sensors[a].Identifier))+"\t\t"+str(round(gv.computer_data.Hardware[3].Sensors[a].get_Value(), 2)), background_color=background_color, font=font2)])
    scrollbar_layout.append([sg.Text("", background_color=background_color, font=font2)])
    scrollbar_layout.append([sg.Text("Dysk twardy:", background_color=background_color, font=font1)])
    for a in range(0, len(gv.computer_data.Hardware[4].Sensors)):
        scrollbar_layout.append([sg.Text(str(a)+"\t"+get_sensor_name(str(gv.computer_data.Hardware[4].Sensors[a].Identifier))+"\t\t"+str(round(gv.computer_data.Hardware[4].Sensors[a].get_Value(), 2)), background_color=background_color, font=font2)])

    layout.append([sg.Column(scrollbar_layout, scrollable=True, vertical_scroll_only=True, expand_y=True, size_subsample_height = 3, background_color=background_color, expand_x=True)])
    layout.append([sg.Push(background_color=background_color), sg.Button("OK", key='-POPUPPRINTEVENTBUTTONOK-'), sg.Push(background_color=background_color)])
    popup_event, popup_values = sg.Window('Sensory komputera', layout, modal=True, background_color=background_color, disable_close=True).read(close=True)  # zwracanie czegokolwiek chyba i tak niepotrzebne
    return popup_event

def create_popup_monitor_window():              # tworzy przezroczysty popup w prawym górnym rogu ekranu, na którym co sekundę wyświetlane są odczyty sensorów komputera
    layout = [
        [sg.Text("CPU: XX %", text_color=GLOBAL_CPU_USAGE_COLOR, key="-MONITORPOPUPCPULOAD-"), sg.Text(" GPU: XX %", text_color=GLOBAL_GPU_USAGE_COLOR, key="-MONITORPOPUPGPULOAD-"), sg.Text(" FANS:  XX %", text_color=GLOBAL_FAN_USAGE_COLOR, key="-MONITORPOPUPFANLOAD-")],
        [sg.Text("     XX\u00B0C", text_color=GLOBAL_CPU_TEMP_COLOR, key="-MONITORPOPUPCPUTEMP-"), sg.Text("      XX\u00B0C", text_color=GLOBAL_GPU_TEMP_COLOR, key="-MONITORPOPUPGPUTEMP-"), sg.Text(" RAM: XXXX GB", text_color=GLOBAL_RAM_USAGE_COLOR, key="-MONITORPOPUPRAMUSAGE-")],
        [sg.Push(), sg.Button(" \u2190 ", key="-POPUPMONITORBUTTONLEFT-", button_color="white on black", highlight_colors=None, font=GLOBAL_FONT_BIG, pad=(0, 0), border_width=0), sg.Button(" \u2191 ", key="-POPUPMONITORBUTTONUP-", button_color="white on black", highlight_colors=None, font=GLOBAL_FONT_BIG, pad=(0, 0), border_width=0), sg.Button(" \u2193 ", key="-POPUPMONITORBUTTONDOWN-", button_color="white on black", highlight_colors=None, font=GLOBAL_FONT_BIG, pad=(0, 0), border_width=0), sg.Button(" \u2192 ", key="-POPUPMONITORBUTTONRIGHT-", button_color="white on black", highlight_colors=None, font=GLOBAL_FONT_BIG, pad=(0, 0), border_width=0)]
        # !!! napis [color] on [color] oznacza [kolor tekstu] na [kolorze tła przycisku]
    ]
    return sg.Window('MONITOR WINDOW', layout, resizable=False, keep_on_top=True, finalize=True, no_titlebar=True, transparent_color="black")

def save_monitor_records(monitor_file_name=GLOBAL_MONITOR_RECORDS_FILE_NAME, append=False):     # zapisuje ciekawe najciekawsze odczytane wartości do pliku, w przyszłości nie potrzebne???
    file = open(get_monitor_file_path(monitor_file_name), "r", encoding='utf-8')
    cpu_fan_values = file.readline().rstrip().split()                   # odczytywanie maksymalnych wartości zapisanych w pliku
    boost_fan_values = file.readline().rstrip().split()
    front_fan_values = file.readline().rstrip().split()
    back_fan_values = file.readline().rstrip().split()
    file.close()
    file = open(get_monitor_file_path(monitor_file_name), "w", encoding='utf-8')
    file.write("CPU_fan\t\t"+str(max(int(gv.monitor_data["FAN2_speed"][-1]), int(cpu_fan_values[1])))+"\n")             # porównywanie maksymalnych wartości z nowo-odczytanymi i zapisywanie większych z nich do pliku
    file.write("Boost_fan\t"+str(max(int(gv.monitor_data["FAN5_speed"][-1]), int(boost_fan_values[1])))+"\n")
    file.write("Front_fan\t"+str(max(int(gv.monitor_data["FAN6_speed"][-1]), int(front_fan_values[1])))+"\n")
    file.write("Back_fan\t"+str(max(int(gv.monitor_data["FAN3_speed"][-1]), int(back_fan_values[1])))+"\n")
    file.close()

def save_monitor_data(monitor_file_name=GLOBAL_MONITOR_DATA_FILE_NAME):                         # zapisuje dane z ostatniej godziny do pliku
    file = open(get_monitor_file_path(monitor_file_name), "w", encoding='utf-8')
    monitor_df = pd.DataFrame(gv.monitor_data)
    file.write(monitor_df.to_string())
    file.close()