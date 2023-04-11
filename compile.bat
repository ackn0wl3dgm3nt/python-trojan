@echo off

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

if "%1" == "number_counter" (
pyinstaller --onefile --noconsole number_counter.py
copy dist\number_counter.exe c:\users\user\desktop
del number_counter.spec
)

:: rmdir /s /q build
