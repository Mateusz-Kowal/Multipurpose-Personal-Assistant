import PySimpleGUI as sg
from PIL import Image
from io import BytesIO
from pygame import mixer
from pygame import time as pygame_time
from random import random
import os
from psutil import Process
import glob
import textwrap
import itertools
import datetime
import time
import schedule
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import clr
from sys import path as sys_path
from sys import getsizeof as sys_getsizeof
import calendar
import numpy as np
import pandas as pd
from math import log as log10
import operator
from dateutil.relativedelta import relativedelta
import urllib.request
import yt_dlp
from typing import Type
import lyricsgenius as lg
import re


import globals as gv
from settings import *


# ścieżki do plików i nazwy

# WSZYSTKO CO TU SIĘ DZIEJE ZASŁUGUJE NA #ułomna_linijka
# jako że plikik graficzne (i inne) przechowuję w różnych folderach, to nie wiem jak najszybciej przygotować funkcje get_image i get_image_byte_value; na razie mam osobne funkcje dla każdej aplikacji, ale może powinno się ją przekazywać w argumencie? i potem dopisać np /calendar/ w środku ścieżki?

def get_avatar_path(name, path=GLOBAL_AVATARS_FOLDER_PATH) -> str:     # zwraca ścieżkę avatara dla podanej nazwy pliku; używać do pola image= w popupach
    return path+name

def get_calendar_image_path(name, path=GLOBAL_CALENDAR_IMAGES_FOLDER_PATH) -> str:       # zwraca ścieżkę pliku graficzngo dla podanej nazwy pliku; używać do pola image= w popupach; de facto to samo co powyżej, ale nie chce mi się dopisywać parametrów
    return path+name

def get_media_player_image_path(name, path=GLOBAL_MEDIA_PLAYER_IMAGES_FOLDER_PATH) -> str:       # zwraca ścieżkę pliku graficzngo dla podanej nazwy pliku; używać do pola image= w popupach; de facto to samo co powyżej, ale nie chce mi się dopisywać parametrów
    return path+name

def get_media_player_thumbnail_path(name, path=GLOBAL_MEDIA_PLAYER_THUMBNAILS_FOLDER_PATH) -> str:       # ścieżka do pliku z miniaturką
    return path+name

def get_sound_path(name, path=GLOBAL_SOUNDS_FOLDER_PATH) -> str:       # zwraca ścieżkę pliku dźwiękowego dla podanej nazwy pliku
    return path+name

def get_song_path(name, path=GLOBAL_SONGS_FOLDER_PATH) -> str:       # zwraca plik o nazwie name z folderu piosenki - w name trzeba podać też str(id) folderu piosenki
    return path+name

def get_log_file_path(name, path=GLOBAL_CONTROL_TEXT_FILES_FOLDER_PATH) -> str:  # zwraca ścieżkę pliku z logami programu
    return path+name

def get_calendar_file_path(name, path=GLOBAL_CALENDAR_TEXT_FILES_FOLDER_PATH) -> str:        # zwraca ścieżkę pliku kalendarza dla podanej nazwy pliku
    return path+name

def get_monitor_file_path(name, path=GLOBAL_MONITOR_TEXT_FILES_FOLDER_PATH) -> str:          # zwraca ścieżkę pliku monitora dla podanej nazwy pliku
    return path+name

def get_media_player_file_path(name, path=GLOBAL_MEDIA_PLAYER_TEXT_FILES_FOLDER_PATH) -> str:          # zwraca ścieżkę pliku media_playera dla podanej nazwy pliku
    return path+name

def get_is_bati_running_path(name=GLOBAL_IS_BATI_RUNNING_FILE_NAME, path=GLOBAL_IS_BATI_RUNNING_FOLDER_PATH):      # zwraca ścieżkę dla pliku is_bati_running.txt
    return path+name

def get_avatar_byte_value(name, width_pixels=100, height_pixels=100):      # zwraca wartość bitową (chyba) pliku graficznego, przy okazji zmienia rozmiar (TO SĄ PIKSELE A NIE %!!!); używać do sg.Image(data= ), albo do sg.Button(image_data= )
    image = Image.open(get_avatar_path(name))
    image = image.resize((width_pixels, height_pixels))
    bio = BytesIO()
    type = name.split('.')[1]
    if type=='png':
        type='PNG'
    elif type=="gif":
        type="GIF"
    else:
        print("Zły typ pliku graficznego:", name, type)
    image.save(bio, type)
    return bio.getvalue()

def get_calendar_image_byte_value(name,  width_pixels=100, height_pixels=100):      # zwraca wartość bitową (chyba) pliku graficznego, przy okazji przeskalowuje (TO SĄ PIKSELE A NIE %!!!); używać do sg.Image(data= ), albo do sg.Button(image_data= )
    image = Image.open(get_calendar_image_path(name))
    image = image.resize((width_pixels, height_pixels))
    bio = BytesIO()
    type = name.split('.')[1]
    if type=='png':
        type='PNG'
    elif type=="gif":
        type="GIF"
    else:
        print("Zły typ pliku graficznego:", name, type)
    image.save(bio, type)
    return bio.getvalue()

def get_media_player_image_byte_value(name,  width_pixels=100, height_pixels=100):      # zwraca wartość bitową (chyba) pliku graficznego, przy okazji przeskalowuje (TO SĄ PIKSELE A NIE %!!!); używać do sg.Image(data= ), albo do sg.Button(image_data= )
    image = Image.open(get_media_player_image_path(name))
    image = image.resize((width_pixels, height_pixels))
    bio = BytesIO()
    type = name.split('.')[1]
    if type=='png':
        type='PNG'
    elif type=="gif":
        type="GIF"
    else:
        print("Zły typ pliku graficznego:", name, type)
    image.save(bio, type)
    return bio.getvalue()

def get_media_player_thumbnail_byte_value(name,  width_pixels=100, height_pixels=100):      # zwraca wartość bitową (chyba) pliku graficznego, przy okazji przeskalowuje (TO SĄ PIKSELE A NIE %!!!); używać do sg.Image(data= ), albo do sg.Button(image_data= )
    image = Image.open(get_media_player_thumbnail_path(name))
    image = image.resize((width_pixels, height_pixels))
    bio = BytesIO()
    type = name.split('.')[1]
    if type=='png':
        type='PNG'
    elif type=="gif":
        type="GIF"
    else:
        print("Zły typ pliku graficznego:", name, type)
    image.save(bio, type)
    return bio.getvalue()

# pliki ze zmiennymi globalnymi

def is_bati_running(file_name=GLOBAL_IS_BATI_RUNNING_FILE_NAME, path=GLOBAL_IS_BATI_RUNNING_FOLDER_PATH) -> bool:                   # zwraca informację, czy Bati jest już uruchomiony (służy do zabezpieczenia przed uruchomieniem dwóch instancji programu)
    file = open(get_is_bati_running_path(file_name, path), "r")
    is_it = file.readline()
    file.close()
    if is_it == "yes":              #ułomna_linijka, no bo XD
        return True
    else:
        return False

def update_is_bati_running(is_it: str, file_name=GLOBAL_IS_BATI_RUNNING_FILE_NAME, path=GLOBAL_IS_BATI_RUNNING_FOLDER_PATH):        # nadpisuje zmienną w pliku mówiącą o tym, czy Bati jest już uruchomiony
    file = open(get_is_bati_running_path(file_name, path), "w")
    file.write(is_it)
    file.close()


# konwersje

def day_number_to_string(num) -> int:           # konwersja numeru dnia z liczby na string
    if len(num)==1:
        string = "0"+str(num)
    else:
        string = str(num)
    return string

def day_string_to_number(string) -> int:        # konwersja numeru dnia ze strina na liczbę
    if string[0]=="0":
        num = int(string[1])
    else:
        num = int(string)
    return num

def month_number_to_word(num) -> str:           # konwersja z numeru miesiąca na nazwę z dużej litery
    if num==1 or num =="01":
        word='January'
    if num==2 or num =="02":
        word='February'
    if num==3 or num =="03":
        word='March'
    if num==4 or num =="04":
        word='April'
    if num==5 or num =="05":
        word='May'
    if num==6 or num =="06":
        word='June'
    if num==7 or num =="07":
        word='July'
    if num==8 or num =="08":
        word='August'
    if num==9 or num =="09":
        word='September'
    if num==10 or num =="10":
        word='October'
    if num==11 or num =="11":
        word='November'
    if num==12 or num =="12":
        word='December'
    return str(word)

def month_word_to_number(word, zeros=False) -> str:         # konwersja z nazwy miesiąca z dużej litery na jego numer, jak zeros=True to zwraca stringa z ewentualnym zerem
    if zeros == False:
        if word=='January':
            num=1
        if word=='February':
            num=2
        if word=='March':
            num=3
        if word=='April':
            num=4
        if word=='May':
            num=5
        if word=='June':
            num=6
        if word=='July':
            num=7
        if word=='August':
            num=8
        if word=='September':
            num=9
        if word=='October':
            num=10
        if word=='November':
            num=11
        if word=='December':
            num=12
    else:
        if word=='January':
            num="01"
        if word=='February':
            num="02"
        if word=='March':
            num="03"
        if word=='April':
            num="04"
        if word=='May':
            num="05"
        if word=='June':
            num="06"
        if word=='July':
            num="07"
        if word=='August':
            num="08"
        if word=='September':
            num="09"
        if word=='October':
            num="10"
        if word=='November':
            num="11"
        if word=='December':
            num="12"
    return str(num)

def datetime_format_date_to_calendar_event_date(datetime_format_date) -> str:       # zamienia format daty z tego dziwnego, w którym się da sumować itd na ten akceptowalny w kodzie i konstruktorach, tj dd.mm.yyyy z zerem wiodącym
    day = str(datetime_format_date).split('-')[2]
    month = str(datetime_format_date).split('-')[1]
    year = str(datetime_format_date).split('-')[0]
    calendar_event_date = day+"."+month+"."+year
    return calendar_event_date

def calendar_event_date_to_datetime_format_date(calendar_event_date) -> datetime.date:        # zamienia format dany z tego w kodzie w CalendarEvent na format datetime.date();      możliwe że możnaby tej oraz powyższej funkcji użyć gdzieś w konstrukturach czy optymalizacjach klasy CalendarEvent, ale to kiedy indziej
    return datetime.datetime.strptime(calendar_event_date, "%d.%m.%Y").date()

def get_beginning_date() -> datetime.date:                  # zwraca początek istnienia BATIego - datę 01.08.2023 - przed tą datą w kalendarzu nic nie było
    return datetime.datetime.strptime(GLOBAL_CALENDAR_BEGINNING_DATE, "%d.%m.%Y").date()


# dźwięk

def play_sound(name, volume=1.0, channel=0):                          # odtwarza pliki dźwiękowe za pomocą VLC; jeżeli coś będzie do zmienienia w przyszłości, to w tej funkcji
    mixer_sound = mixer.Sound(get_sound_path(name))
    mixer_sound.set_volume(volume)
    mixer.Channel(0).play(mixer_sound)              # kanał 0 jest zadedykowany dla dźwięków systemowych, kanał 1 dla piosenek

# popupy i notyfikacje

def popup_info(message, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS, auto_close=False):          # wyświetla popup z informacją dla użytkownika
    message = wrap_text(message, GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS, drop_endline_characters=False)
    column = [[sg.Text(message, font=font2)]]
    layout = [
        [sg.Push(), sg.Text("Info \u2139", font=font1), sg.Push()],
        [sg.Image(data = get_avatar_byte_value(GLOBAL_AVATAR_INFO), pad=((10, 0), 3)), sg.Column(column, pad=(0, 0))],
        [sg.Push(), sg.Button("OK"), sg.Push()]
        ]
    window = sg.Window('Informacja', layout, finalize=True, auto_close=auto_close, auto_close_duration=3, disable_close=True).read(close=True)

def popup_warning(message, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS, auto_close=True, avatar=GLOBAL_AVATAR_WARNING):                 # wyświetla ostrzeżenie, bez potwierdzenia, sama informacja, zawsze blokuje akcję, którą chcieliśmy wykonać
    #sg.PopupQuick(message, image=get_image_path("EZY.png"), background_color=GLOBAL_POPUP_COLOR)
    message = wrap_text(message, GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS)
    column = [[sg.Text(message, font=font2)]]
    layout = [
        [sg.Push(), sg.Text("WARNING!", font=font1), sg.Push()],
        [sg.Image(data = get_avatar_byte_value(avatar), pad=((10, 0), 3)), sg.Column(column, pad=(0, 0))],
        [sg.Push(), sg.Button("OK"), sg.Push()]
        ]
    window = sg.Window('WARNING!', layout, finalize=True, auto_close=auto_close, auto_close_duration=3, disable_close=True).read(close=True)
    #image = window['-TESTKEY-']            # dodać ten klucz do image'a wyżej
    # while True:                                           # eksperymentowanie z gifami
    #     event, values = window.read(timeout=100)  
    #     if event == 'Exit':
    #         break
    #     image.update_animation_no_buffering(get_image_path(GLOBAL_AVATAR_WARNING), 100)

def popup_warning_confirm(message, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):         # wyświetla ostrzeżenie, które pyta się czy na pewno chcemy coś wykonać i zwraca odpowiedź
    message = wrap_text(message, GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS)
    column = [[sg.Push(), sg.Text("WARNING!", font=font1), sg.Push()], [sg.Text(message, font=font2)]]
    layout = [[sg.Image(data = get_avatar_byte_value(GLOBAL_AVATAR_WARNING_CONFIRM), pad=((0, 0), 3)), sg.Column(column, pad=(0, 0))], [sg.Push(), sg.Button("TAK", key='-POPUPWARNINGBUTTONYES-'), sg.Button("NIE", key='-POPUPWARNINGBUTTONNO-'), sg.Push()]]
    event, values = sg.Window('WARNING!', layout, finalize=True, disable_close=True).read(close=True)
    return event, values

def popup_confirm(message1, message2, title, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):
    message2 = wrap_text(message2, GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS)
    layout = [
        [sg.Text(message1, font=font1)],
        [sg.Text(message2, font=font2)] if len(message2) < 500 else [sg.Column([[sg.Text(message2, font=font2)]], scrollable=True, vertical_scroll_only=True, expand_y=True, size_subsample_height = 10, expand_x=True)],        #złota_linijka
        [sg.Push(), sg.Button("TAK", key='-POPUPWARNINGBUTTONYES-'), sg.Button("NIE", key='-POPUPWARNINGBUTTONNO-'), sg.Push()]
    ]
    event, values = sg.Window(title, layout, finalize=True, disable_close=True).read(close=True)
    return event, values

def popup_enter(question, title, textbox_text="", font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):
    message = wrap_text(question, GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS-5)
    layout = [
        [sg.Text(message, font=font1)],
        [sg.Input(key='-POPUPENTERTEXT-', default_text=textbox_text, font=font1)],
        [sg.Push(), sg.Button("OK"), sg.Push()]
    ]
    event, values = sg.Window(title, layout, finalize=True, disable_close=True).read(close=True)
    return event, values

def popup_double_enter(question, title, textbox_text1="", textbox_text2="", font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):
    message = wrap_text(question, GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS-5)
    layout = [
        [sg.Text(message, font=font1)],
        [sg.Input(key='-POPUPENTERTEXT1-', default_text=textbox_text1, font=font1)],
        [sg.Input(key='-POPUPENTERTEXT2-', default_text=textbox_text2, font=font1)],
        [sg.Push(), sg.Button("OK"), sg.Push()]
    ]
    event, values = sg.Window(title, layout, finalize=True, disable_close=True).read(close=True)
    return event, values

def popup_error(message, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):                   # wyświetla informację o błędzie
    message = wrap_text(message, GLOBAL_MAIN_WINDOW_WIDTH_CHARACTERS)
    layout = [[sg.Push(), sg.Image(data = get_avatar_byte_value(GLOBAL_AVATAR_ERROR), pad=((0, 0), 3)), sg.Push()],
            [sg.Push(), sg.Text("ERROR!", font=font1, text_color="red"), sg.Push()],
            [sg.Text("BATI wziął umarł. Zostawił coś takiego:\n\n"+message+"\nProgram się zakończy.", font=font2)],
            [sg.Push(), sg.Button("OK"), sg.Push()]]
    window = sg.Window('ERROR!', layout, finalize=True, auto_close=False, disable_close=True).read(close=True)

def popup_notify(message, title, font1=GLOBAL_FONT, font2=GLOBAL_FONT_NOTIFICATIONS):           # wyświetla powiadomienie w rogu ekranu
    column = [[sg.Text(title, font=font1)], [sg.Text(message, font=font2)]]
    layout = [[sg.Image(data = get_avatar_byte_value(GLOBAL_AVATAR_NOTIFY), key="-POPUPNOTIFYIMAGEAVATAR-", pad=((10, 0), 3)), sg.Column(column, pad=(0, 0))]]
    w1, h1 = location = sg.Window.get_screen_size()     # pobiera rozmiar monitora
    window = sg.Window('Notification', layout, no_titlebar=True, margins=(0, 0), alpha_channel=0, finalize=True, location=location, keep_on_top=True)
    w2, h2 = window.current_size_accurate()             # pobiera całkowity rozmiar właśnie stworzonego okienka
    window.move(0, h1-h2-10)                            # przesuwa okienko w lewy dolny róg;    -10 bo coś nie gra, wystaje za bardzo na dół poza ekran z jakiegoś powodu
    #window.TKroot['cursor'] = 'hand2'                  # jak się najedzie to się zamienia na rączkę do kliknięcia
    #window.bind('<Button-1>', "Window")                # dzięki temu kliknięcie na okienko robi event
    alpha, count = 0, 0
    image = window['-POPUPNOTIFYIMAGEAVATAR-']
    play_sound(GLOBAL_SOUND_NOTIFICATION, 0.1)
    while True:                     # ta pętla pięknie robi fade in oraz fade out
        event, values = window.read(timeout=50)
        if event == sg.TIMEOUT_EVENT:
            count += 1
            if count <= 5:
                alpha += 0.2
                image.update_animation_no_buffering(get_avatar_path(GLOBAL_AVATAR_NOTIFY), 50)
                window.set_alpha(alpha)
            elif count <= 100:
                image.update_animation_no_buffering(get_avatar_path(GLOBAL_AVATAR_NOTIFY), 50)
                pass
            else:
                alpha -= 0.1
                image.update_animation_no_buffering(get_avatar_path(GLOBAL_AVATAR_NOTIFY), 50)
                window.set_alpha(alpha)
                if alpha <= 0:
                    break
        elif event == "Window":
            break
    window.close()


# inne rzeczy ułatwiające życie, różne get'y

def get_previous_month(month: int, year: int) -> tuple[int, int]:           # zwraca numer poprzedniego miesiąca (i zmniejsza też rok o 1 jeśli trzeba);    !!! tuple[int, int], a nie tuple(int, int)
    month = month-1
    if month==0:
        month = 12
        year = year-1
    return (month, year)

def get_next_month(month: int, year: int) -> tuple[int, int]:           # zwraca numer następnego miesiąca (i zwiększa też rok o 1 jeśli trzeba)
    month = month+1
    if month==13:
        month = 1
        year = year+1
    return month, year

def wrap_text(message, max_width_characters, drop_endline_characters=False) -> str:                           # zawija text po iluś znakach, tzn dodaje znaki końca linii po każdej linijce 
    if drop_endline_characters==False:
        mylist = [textwrap.wrap(i, width = max_width_characters) for i in message.split('\n') if i != '']
        split_message = list(itertools.chain.from_iterable(mylist))
    else:
        split_message = textwrap.wrap(text=message, width=max_width_characters)
    message = ""
    for line in split_message:
        message = message+line+"\n"
    return message

# def own_wrap_text(message, max_width_characters):         # raz że bez sensu, a dwa że nie działa
#     split_message = message.split(" ")
#     message = ""
#     length_lines = 0
#     line_letters_left = max_width_characters
#     for word in split_message:
        
#         if len(word) > line_letters_left:                # jak słowo jest dłuższe od max_length
#             message += word[0:max_width_characters-1]+"-\n"+word[max_width_characters-1:len(word)-1]        # dodajemy myślnik i przenosimy resztę do następnej linijki
#             line_letters_left = max_width_characters - (len(word)-max_width_characters)                     # teraz a następnej linijce jest mniej miejsca o tyle, o ile liter przenieśliśmy tamto słowo
#         else:
#             message += word+"\n"
#             line_letters_left = max_width_characters
#     return message



# FUNKCJE DO CZYSZCZENIA TEKSTU
# pobrane skądś z githuba, od typa, któremu też lyricsgenius pobiera zaśmiecony tekst; funkcje do edycji, zależy jaka będzie potrzeba

# STRING STUFF
# def remove_punctuation(s):
#     no_punc = str.maketrans('', '', string.punctuation)
#     return s.translate(no_punc)

def remove_extra_spaces(s):
    return ' '.join(s.split())

def remove_apostrophe(s):
    return s.replace('’', '')

def replace_apostrophe(s):
    return s.replace('’', "'")

def remove_zero_width_space(s):
    return s.replace('\u200b', '')

def remove_right_to_left_mark(s):
    return s.replace('\u200f', '')

def scrub_string(s):
    '''
    Removes opinionated unwanted characters from 
    string, namely:
        - zero width spaces '\u200b' ---> ''
        - apostrophe '’' ---> ''
        - extra spaces '    ' ---> ' '
    '''
    s = remove_zero_width_space(s)
    s = remove_right_to_left_mark(s)
    s = replace_apostrophe(s)
    s = remove_extra_spaces(s)
    return s


def replace_br(s):
    s = s.replace('<br/>', '\n')
    return s

# def keep_until(s, substr, case_insensitive=False):
#     # Look for substr index and slice
#     if case_insensitive:
#         try:
#             index = s.lower().index(substr.lower())
#             return s[:index]
#         except ValueError:
#             # NOTE: index not found
#             return s
        
#     # Just split and take first
#     until, *after_ = s.split(substr)[0]
#     return until


def until_embed(s, case_insensitive=False, use_regex=True):
    if use_regex:
        pattern = r"Embed\d*\b"
        found = re.findall(pattern, s,  flags=re.IGNORECASE)
        for f in found:
            s = s.replace(f, '')
        return s
    # else:
    #     s = keep_until(s, 'Embed', case_insensitive=case_insensitive)
    #     # NOTE: could be Embed1, Embed27, etc
    #     if s != '':
    #         while s[-1].isnumeric():
    #             s = s[:-1]
    #     return s
    return s

def remove_see_live_ad(s, include_word_boundaries=True):
    pattern = r"\bSee .+ Live\b" if include_word_boundaries else r"See .+ Live"
    ads = re.findall(pattern, s,  flags=re.IGNORECASE)
    for ad in ads:
        s = s.replace(s, '')
    return s

def remove_you_may_like_ad(s, include_word_boundaries=True):
    pattern = r"\bYou might also.+ like\b" if include_word_boundaries else r"You might also.+ like"
    ads = re.findall(pattern, s,  flags=re.IGNORECASE)
    for ad in ads:
        s = s.replace(s, '')
    return s

# def remove_square_brackets(s):
#     pattern = r"\[([A-Za-z0-9_]+)\]"
#     brackets = re.findall(pattern, s,  flags=re.IGNORECASE)
#     for found in brackets:
#         s.replace(found, '')
#     return s


# główna funkcja, która czyści każdą linijkę
def clean_line(s):
    s = scrub_string(s)
    s = remove_see_live_ad(s)
    s = remove_you_may_like_ad(s)
    s = replace_br(s)
    s = until_embed(s)
    return s