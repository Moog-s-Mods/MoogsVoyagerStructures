@echo off
python "C:\Users\finn\Programming Projects\moogs-structure-validator\validator.py" ^
  --config "%~dp0validator.json" ^
  --project-root "%~dp0."
