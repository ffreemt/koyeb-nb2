setlocal
cd /d %~dp0
cd go-cqhttp-940fix5
REM pm2 start --no-autorestart start-go-cqhttp.bat --interpreter none
pm2 start --max-restarts=5 start-go-cqhttp.bat --interpreter none
