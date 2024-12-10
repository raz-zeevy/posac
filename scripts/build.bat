@echo off
cd ../

:: Load the version from the .env file
for /f "tokens=2 delims==" %%A in ('findstr APP_VERSION .env') do (
    set "APP_VERSION=%%A"
)

:: Check if APP_VERSION is set
if "%APP_VERSION%"=="" (
    echo Error: APP_VERSION is not set in the .env file.
    exit /b 1
)

:: Ensure that APP_VERSION has 4 components (e.g., 1.1.6.0)
setlocal enabledelayedexpansion
set dot_count=0
for /l %%i in (1,1,255) do (
    if "!APP_VERSION:~%%i,1!"=="" goto check_done
    if "!APP_VERSION:~%%i,1!"=="." set /a dot_count+=1
)

:check_done
if not "%dot_count%"=="3" (
    echo Error: The APP_VERSION is not formatted as major.minor.build.revision
    exit /b 1
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Run PyInstaller with the version passed to the .spec file
@REM venv\Scripts\python.exe -m PyInstaller app.spec --noconfirm

:: Load the version from the .env file
echo Version format to be used in Inno Setup: %APP_VERSION%

:: Create a temporary .iss file with AppVersion and VersionInfoVersion replaced
(for /f "usebackq delims=" %%i in ("scripts/setup.iss") do (
    set "line=%%i"
    if "!line!"=="AppVersion={#MyAppVersion}" (
        echo AppVersion=%APP_VERSION%
    ) else if "!line!"=="VersionInfoVersion={#MyAppVersion}" (
        echo VersionInfoVersion=%APP_VERSION%
    ) else (
        echo !line!
    )
)) > setup_temp.iss

:: Run Inno Setup with the temporary file
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup_temp.iss
@REM del setup_temp.iss
