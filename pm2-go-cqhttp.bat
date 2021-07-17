setlocal
cd /d %~dp0
cd go-cqhttp-940fix5
pm2 start --no-autorestart start-go-cqhttp.bat --interpreter none