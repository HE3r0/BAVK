@echo off
setlocal
cd /d "%~dp0"

echo === BAVK Git Sync ===
echo.

REM Initialize Git repository if this folder is not yet a Git repo.
if not exist ".git" (
    echo Initializing local Git repository...
    git init
    if errorlevel 1 goto :error
    git branch -M main
)

REM Configure GitHub remote if origin does not exist.
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Adding GitHub remote...
    git remote add origin https://github.com/HE3r0/BAVK.git
    if errorlevel 1 goto :error
)

echo.
git status
if errorlevel 1 goto :error

echo.
git add .
if errorlevel 1 goto :error

git diff --cached --quiet
if %errorlevel%==0 (
    echo.
    echo No changes to commit.
    exit /b 0
)

git commit -m "Update BAVK"
if errorlevel 1 goto :error

git push -u origin main
if errorlevel 1 goto :error

echo.
echo === Push completed ===
exit /b 0

:error
echo.
echo === Git operation failed ===
pause
exit /b 1
