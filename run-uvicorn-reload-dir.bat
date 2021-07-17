setlocal
cd /d %~dp0
REM venv\Scripts\activate
set PATH=venv\Scripts;%PATH%
REM set PYTHONPATH=
uvicorn --port 8680 bot:app --reload --reload-dir koyeb_nb2
pause
