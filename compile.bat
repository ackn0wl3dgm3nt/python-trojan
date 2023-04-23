@echo off
title Compiling...

if "%1" == "malware" (
pyinstaller specs\payload.spec
python update_payload.py
del dist\payload.exe
pyinstaller --upx-dir=C:\UPX specs\malware.spec
echo Malware compiled!
)

if "%1" == "server" (
pyinstaller specs\server.spec
echo Server compiled!
)

title cmd.exe
