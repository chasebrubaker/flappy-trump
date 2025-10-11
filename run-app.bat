@echo off
setlocal

set PYTHON_VERSION=3.12.2
set PYTHON_EXE=python
set VENV_DIR=.venv
set PYTHON_INSTALLER=python-installer.exe
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

:: Check if Python is installed
where %PYTHON_EXE% >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed.

    set /p INSTALL_ALL="Install Python for all users?  Note: will need admin privileges(Y/N): "
    if /i "%INSTALL_ALL%"=="Y" (
        set INSTALL_ARGS=/quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    ) else (
        set INSTALL_ARGS=/quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    )

    echo Downloading Python...
    curl -L -o %PYTHON_INSTALLER% %PYTHON_URL%
    echo Installing Python...
    start /wait %PYTHON_INSTALLER% %INSTALL_ARGS%
    del %PYTHON_INSTALLER%
) else (
    echo Python is already installed.
)

:: Use py.exe if available
where py >nul 2>nul
if %errorlevel%==0 (
    set PYTHON_EXE=py -3
)

:: Create virtual environment if it doesn't exist
if not exist %VENV_DIR%\Scripts\activate (
    echo Creating virtual environment in %VENV_DIR%...
    %PYTHON_EXE% -m venv %VENV_DIR%
)

:: Activate venv
call %VENV_DIR%\Scripts\activate.bat

:: Upgrade pip and install requirements
echo Installing dependencies...
python -m pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
)

:: Run your app
echo Running the app...
python main.py

endlocal
pause

