@echo off
sc stop ABC
taskkill /IM payload.exe /F
