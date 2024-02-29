$old_ver = "1.1.4"                                                                                  # tworzy zmienną, która jest nazwą starej wersji (do edycji)
$new_ver = "1.1.5"                                                                                  # tworzy zmienną, która jest nazwą nowej wersji (też do edycji)

Write-Host "Rozpoczynam tworzenie programu BATI v.$new_ver"


cd C:\Users\matik\Desktop\python\BATI\versions\                                                     # wchodzi do folderu versions
mkdir $new_ver                                                                                      # tworzy folder o nazwie nowej wersji
cd $new_ver
                                                                                         # wchodzi do niego
Write-Host "Rozpoczynam tworzenie pliku wykonywalnego"
pyinstaller --onefile --uac-admin --icon ..\_DEV\avatars\EZY.ico --name BATI_v.$new_ver -w ..\_DEV\scripts\main.py      # instaluje w tym folderze plik wykonywalny (w jednym pliku) z ikoną pod podaną ścieżką z nazwą nawierającą nową wersję, jest to aplikacja okienkowa (bez konsoli), która jest uruchamiana w trybie administratora oraz jej głównym plikiem jest main.py pod podaną ścieżką
Write-Host "Tworzenie pliku wykonywalnego zakonczone"

Write-Host "Rozpoczynam kopiowanie plików"
cp -r ..\_DEV\avatars .\dist\                                                                   # kopiuje wszystkie pliki z avatarami z wersji deweloperskiej do nowej lokacji
cp -r ..\_DEV\sounds .\dist\                                                                    # kopiuje wszystkie pliki z dźwiękami z wersji deweloperskiej do nowej lokacji
cp -r ..\_DEV\images .\dist\                                                                    # kopiuje wszystkie pliki z obrazami z wersji deweloperskiej do nowej lokacji
cp -r ..\$old_ver\dist\text_files .\dist\                                                       # kopiuje folder z plikami tekstowymi ze starej wersji do nowej lokacji (niniejszego skryptu ma tam nie być, nie jest on potrzebny)
mkdir .\dist\packages                                                                           # tworzy folder packages, do którego będą przeniesione wszystkie wszystkie pliki .dll (w _DEV ten folder nie istnieje)
cp -r ..\_DEV\scripts\*.dll .\dist\packages\                                                    # przenosi pliki .dll do dedykowanego folderu packages
Write-Host "Kopiowanie plikow zakonczone"                                                       # albo folderów z plikami z _DEVa albo z ostatniej wersji -> zoptymalizować jakoś?

$name = "BATI_startup"         # to też działa zajebiście, aktualizowanie zadania
Write-Host "Rozpoczynam edytowanie zadania $name z Harmonogramie Zadan"
# $name = "AAAAA_BATI_test"         # tworzenie nowego zadania działa zajebiście, zostawiam gdybym kiedyś potrzebował
# $location = "C:\Users\matik\Desktop\python\BATI\versions\$new_ver\dist"
# $exe = "BATI_v.$new_ver.exe"
# $action = New-ScheduledTaskAction -Execute "$location\$exe" -WorkingDirectory $location
# $trigger = New-ScheduledTaskTrigger -AtStartup
# $principal = New-ScheduledTaskPrincipal -RunLevel Highest
# #$settings = New-ScheduledTaskSettingsSet
# $task = New-ScheduledTask -Action $action -Trigger $trigger -Principal $principal
# Register-ScheduledTask -taskName $name -InputObject $task

$location = "C:\Users\matik\Desktop\python\BATI\versions\$new_ver\dist"
$exe = "BATI_v.$new_ver.exe"
$action = New-ScheduledTaskAction -Execute "$location\$exe" -WorkingDirectory $location
Set-ScheduledTask -TaskName "$name" -Action $action
Write-Host "Edytowanie zadania $name z Harmonogramie Zadan zakonczone"


Write-Host "Program BATI v.$new_ver gotowy do uzytku"