@echo off
setlocal

goto not38

python -V | find "3.8"
if errorlevel 1 goto not38
::python -V
echo pyinstaller only works with versions up to 3.7
pause
goto :eof

:not38
set path=c:\Python36;c:\Python36\scripts;%path%
set path=%path%;"C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64"


if exist env\scripts 	set path=%path%;env\Scripts
if not exist env\scripts	python.exe -m venv env && env/Scripts/activate && python -m pip install -r requirements.txt 

::  --hiddenimport pkg_resources.py2_warn   Fixes ModuleNotFoundError: No module named 'pkg_resources.py2_warn'

pyinstaller ^
  --onefile ^
  --distpath . ^
  --hiddenimport pkg_resources.py2_warn ^
  "%~dp0\create_file.py "
pause

