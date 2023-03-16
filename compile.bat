@echo off

if "%1" == "payload" (
pyinstaller --hiddenimport win32timezone --onefile --name payload main.py
del payload.spec
)

if "%1" == "loader" (
set script_name=loader
set program_name=malware
set upx_dir=C:\UPX

python update_payload.py
pyinstaller --clean --onefile --noconsole --upx-dir %upx_dir% %script_name%.py --name %program_name%

del %program_name%.spec
)

if "%1" == "number_counter" (
pyinstaller --onefile --noconsole number_counter.py
copy dist\number_counter.exe c:\users\user\desktop
del number_counter.spec
)

rmdir /s /q build

