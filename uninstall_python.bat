@echo off
setlocal

set VENV_DIR=.venv
set PYTHON_VERSION=3.12.2

echo This will uninstall the virtual environment and optionally Python %PYTHON_VERSION%.
set /p CONFIRM="Are you sure you want to continue? (Y/N): "
if /i "%CONFIRM%" neq "Y" (
    echo Aborted.
    exit /b
)

:: Remove virtual environment
if exist %VENV_DIR% (
    echo Removing virtual environment...
    rmdir /s /q %VENV_DIR%
) else (
    echo No virtual environment found.
)

:: Ask user whether to uninstall Python
set /p UNINSTALL_PYTHON="Would you like to uninstall Python %PYTHON_VERSION% as well? (Y/N): "
if /i "%UNINSTALL_PYTHON%"=="Y" (
    echo Attempting to uninstall Python...

    :: Try to locate the uninstaller from the Windows registry uninstall paths
    for /f "tokens=*" %%G in ('reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall /s /f "Python %PYTHON_VERSION%" 2^>nul ^| findstr /i "UninstallString"') do (
        set "UNINSTALLER_LINE=%%G"
    )

    for /f "tokens=2*" %%A in ("%UNINSTALLER_LINE%") do (
        set "UNINSTALLER=%%B"
    )

    if defined UNINSTALLER (
        echo Found uninstaller: %UNINSTALLER%
        start /wait "" %UNINSTALLER% /quiet
    ) else (
        echo Could not find Python uninstaller automatically.
        echo Please uninstall Python manually through "Apps & Features" or the Control Panel.
    )
) else (
    echo Skipping Python uninstall.
)

echo Done.
pause
