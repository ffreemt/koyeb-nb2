setlocal
cd /d %~dp0

REM py -3.8 -m venv venv
py -3.7 -m venv venv
venv\Scripts\activate
python -m pip install pip -U
python -m pip install -r requirements-win.txt

:END
pause
