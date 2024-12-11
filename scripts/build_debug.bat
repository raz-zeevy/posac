@echo off
setlocal EnableDelayedExpansion

:: Get version from .env file
for /f "tokens=2 delims==" %%a in ('type ..\.env ^| findstr "VERSION"') do set VERSION=%%a
set VERSION=%VERSION: =%

:: Change to root directory
cd ..

:: Activate virtual environment
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo Error: Virtual environment not found at venv\Scripts\activate
    exit /b 1
)

:: Create debug spec file
echo Creating debug spec file...
if not exist app.spec (
    echo Error: app.spec file not found
    exit /b 1
)
copy app.spec app_debug.spec
powershell -Command "(Get-Content app_debug.spec) | ForEach-Object { $_ -replace 'name=''Posac''', 'name=''PosacDebug''' -replace 'console=False', 'console=True' -replace 'debug=False', 'debug=True' } | Set-Content app_debug.spec"

:: Copy setup.iss to setup_debug.iss and modify it
echo Creating debug setup file...
if not exist scripts\setup.iss (
    echo Error: setup.iss file not found
    exit /b 1
)
copy scripts\setup.iss setup_debug.iss
powershell -Command "(Get-Content setup_debug.iss) | ForEach-Object { $_ -replace '#define MyAppName \"Posac\"', '#define MyAppName \"Posac Debug\"' -replace '#define MyAppExeName \"posac.exe\"', '#define MyAppExeName \"PosacDebug.exe\"' -replace 'OutputBaseFilename=PosacSetup', 'OutputBaseFilename=PosacSetupDebug' -replace 'setup.iss', 'setup_debug.iss' -replace '{param:MyAppVersion\|1.1.8.0}', '%VERSION%' -replace 'dist\\Posac', 'dist\\PosacDebug' } | Set-Content setup_debug.iss"

:: Build debug version
echo Building debug version...
python -m PyInstaller app_debug.spec --noconfirm
if errorlevel 1 (
    echo Error: PyInstaller build failed
    exit /b 1
)

:: Verify the executable was created
if not exist "dist\PosacDebug\PosacDebug.exe" (
    echo Error: PyInstaller build did not create PosacDebug.exe
    exit /b 1
)

:: Build debug installer with version
echo Building debug installer...
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo Error: Inno Setup compiler not found
    exit /b 1
)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup_debug.iss
if errorlevel 1 (
    echo Error: Inno Setup compilation failed
    exit /b 1
)

:: Clean up temporary files
echo Cleaning up...
del setup_debug.iss
del app_debug.spec

echo Debug build complete! Version: %VERSION%

