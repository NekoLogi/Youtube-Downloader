@echo off
call ".\env\Scripts\activate"

python ".\main.py"

start "" ".\downloads"

pause
