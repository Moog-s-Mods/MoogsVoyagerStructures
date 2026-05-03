@echo off
if "%MOOGS_VALIDATOR_PATH%"=="" (
    echo ERROR: MOOGS_VALIDATOR_PATH is not set.
    echo.
    echo Point it at the local validator.py - example:
    echo   setx MOOGS_VALIDATOR_PATH "C:\path\to\moogs-structure-validator\validator.py"
    echo.
    echo Restart the terminal after running setx so the new value is visible.
    exit /b 1
)
if not exist "%MOOGS_VALIDATOR_PATH%" (
    echo ERROR: validator not found at %MOOGS_VALIDATOR_PATH%
    exit /b 1
)
python "%MOOGS_VALIDATOR_PATH%" ^
  --config "%~dp0validator.json" ^
  --project-root "%~dp0."
