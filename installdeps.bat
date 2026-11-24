
@echo off
setlocal
cd /d "%~dp0"
title GTA VI Setup

set "ROOT=%~dp0"
set "ASSETS=%ROOT%deps\assets"

if not exist "deps\Main.pyw" (
    echo ERROR: deps\Main.pyw not found.
    pause
    exit /b 1
)

if not exist "%ASSETS%\logo.ico" (
    echo ERROR: logo.ico not found.
    pause
    exit /b 1
)

if not exist "%ASSETS%\intro.mp4" (
    echo ERROR: intro.mp4 not found.
    pause
    exit /b 1
)

echo Installing deps
py -m pip install PySide6

if errorlevel 1 (
    echo ERROR: Error
    pause
    exit /b 1
)

echo Configuring launcher...

set "LAUNCHER=%ROOT%deps\Launch.vbs"

> "%LAUNCHER%" echo Set shell = CreateObject("WScript.Shell")
>> "%LAUNCHER%" echo Set files = CreateObject("Scripting.FileSystemObject")
>> "%LAUNCHER%" echo folder = files.GetParentFolderName(WScript.ScriptFullName)
>> "%LAUNCHER%" echo shell.CurrentDirectory = folder
>> "%LAUNCHER%" echo shell.Run "pythonw.exe ""Main.pyw""", 1, False

echo Making Gta 6 shortcut

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$root = (Get-Location).Path; ^
$shell = New-Object -ComObject WScript.Shell; ^
$link = $shell.CreateShortcut((Join-Path $root 'GTA VI.lnk')); ^
$link.TargetPath = Join-Path $env:SystemRoot 'System32\wscript.exe'; ^
$link.Arguments = '""' + (Join-Path $root 'deps\Launch.vbs') + '""'; ^
$link.WorkingDirectory = $root; ^
$link.IconLocation = (Join-Path $root 'deps\assets\logo.ico') + ',0'; ^
$link.Description = 'GTA VI'; ^
$link.Save()"

if errorlevel 1 (
    echo ERROR: Shortcut failed.
    pause
    exit /b 1
)

echo.
echo Setup complete
echo You can now open the GTA VI shortcut
echo.
pause
