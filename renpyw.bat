@echo off

rem Version of the Ren'Py SDK to be installed
set renpy_version=6.99.12.4

set try_download=0

:find_by_renpy
if exist "lib\renpy\lib\windows-i686\python.exe" (
    .\lib\renpy\lib\windows-i686\python.exe -O ./build.py
    goto :EOF
)

:download_renpy_sdk
if %try_download% == 1 goto :error
set try_download = 1
bitsadmin /TRANSFER RENPY https://www.renpy.org/dl/%renpy_version%/renpy-%renpy_version%-sdk.7z.exe %~dp0\renpy.7z.exe
if errorlevel 1 goto :error
start /wait renpy.7z.exe x -y -olib
del renpy.7z.exe
timeout /T 1
rename lib\renpy-%renpy_version%-sdk renpy
goto :find_by_renpy

:error
    echo Error: unknown error
