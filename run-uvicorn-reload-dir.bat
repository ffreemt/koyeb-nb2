setlocal
cd /d %~dp0

REM venv\Scripts\activate
set PATH=venv\Scripts;%PATH%

REM set PYTHONPATH=

REM default to 8000
REM uvicorn bot:app --reload --reload-dir koyeb_nb2

REM uvicorn --port 8680 bot:app --reload --reload-dir koyeb_nb2
uvicorn --host 0.0.0.0 --port 8680 bot:app --reload --reload-dir koyeb_nb2

pause
