setlocal
cd /d %~dp0
call pm2-go-cqhttp.bat
call run-uvicorn-reload-dir.bat
pause