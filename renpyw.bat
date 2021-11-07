@echo off
setlocal

rem Version of the Ren'Py SDK to be installed
set renpy_version=6.99.12.4

rem Python architecture to use
set renpy_arch=windows-i686

if not exist "lib\renpy\lib\%renpy_arch%\python.exe" (
    echo INFO: Download Ren'Py SDK v%renpy_version%
    del renpy.7z.exe 2>nul
    rmdir /s /q lib\renpy-%renpy_version%-sdk 2>nul
    bitsadmin /transfer renpy "https://www.renpy.org/dl/%renpy_version%/renpy-%renpy_version%-sdk.7z.exe" %~dp0\renpy.7z.exe >nul
    if errorlevel 1 goto :error
    start /wait renpy.7z.exe x -y -olib
    del renpy.7z.exe
    timeout /t 1 >nul
    xcopy /e /q /s lib\renpy lib\renpy-%renpy_version%-sdk >nul
    rmdir /s /q lib\renpy
    rename lib\renpy-%renpy_version%-sdk renpy
)

.\lib\renpy\lib\%renpy_arch%\python.exe -O ./renpyw.py %*
goto :EOF

:error
    echo Error: unknown error
    pause
