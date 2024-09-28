@echo off
reg add "HKEY_CURRENT_USER\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f
setlocal enabledelayedexpansion

set VIRTUAL_ENV_DIR=%~dp0.venv

if not exist !VIRTUAL_ENV_DIR! (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create the virtual environment.
        pause
        exit /b 1
    )
    
    if exist requirements.txt (
        echo Installing dependencies from requirements.txt...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo Failed to install dependencies.
            pause
            deactivate
            exit /b 1
        )
    )
)

call !VIRTUAL_ENV_DIR!\Scripts\activate

echo Running main.py...
python main.py
if errorlevel 1 (
    echo An error occurred while running main.py.
    pause
    deactivate
    exit /b 1
)

echo Deactivating virtual environment...
deactivate
echo Done.

pause
exit /b 0