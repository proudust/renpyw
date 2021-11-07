@echo off

set try_download=0
goto :find_by_renpy

:find_by_path
where $path:python /q
if errorlevel 1 (
    python ./build
    goto :EOF
) else (
    python ./build
    goto :EOF
)

:find_by_renpy
if exist "lib\renpy\lib\windows-i686\python.exe" (
    .\lib\renpy\lib\windows-i686\python.exe -O ./build
    goto :EOF
)

:download_renpy_sdk
if %try_download% == 1 goto :error
set try_download = 1
bitsadmin /TRANSFER RENPY https://www.renpy.org/dl/6.99.12.4/renpy-6.99.12.4-sdk.7z.exe %~dp0\renpy.7z.exe
if errorlevel 1 goto :error
start /wait renpy.7z.exe x -y -olib
del renpy.7z.exe
timeout /T 1
rename lib\renpy-6.99.12.4-sdk renpy
goto :find_by_renpy

:error
    echo Error: unknown error
