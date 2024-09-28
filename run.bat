@echo off
reg add "HKEY_CURRENT_USER\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f
set VIRTUAL_ENV=%~dp0.venv\Scripts\activate
if not exist %VIRTUAL_ENV% (
    echo Virtual environment not found.
    pause
    exit /b 1
)

echo Activating virtual environment...
call %VIRTUAL_ENV%

echo Running main.py...
python main.py

echo Deactivating virtual environment...
deactivate
echo Done.

pause
exit