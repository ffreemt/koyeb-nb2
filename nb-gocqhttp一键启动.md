# 一键启动 `Nonebot2 + go-cqhttp ` 环境
`Windows 10`里写`nonebot2`插件

[英文（本地及云里docker运行noenbot2）](https://github.com/ffreemt/koyeb-nb2/blob/master/README.md)

## 准备工具
    *   安装 `python 3.7` 或以上（谷歌bing或百度）
    *   安装 `nodejs` （谷歌bing或百度）
    *   安装 `pm2`
        *  命令行运行 `npm install pm2 -g` # [https://www.npmjs.com/package/pm2/v/4.4.0](https://www.npmjs.com/package/pm2/v/4.4.0)
    *  下载 koyeb-nb repo
        例如命令行运行 git clone https://github.com/ffreemt/koyeb-nb2
## 建立 Python 虚拟环境`venv`
```bash
cd path-to-koyeb-nb
python -V  # 确认 python 版本是 3.7 或更高
python -m venv
venv\Scripts\activate
python -m pip install pip -U
python -m pip install -r requirements-win.txt
```
如果系统里装了Python3.7，也可以命令行运行 `setup-windows-python-venv.bat` 或点击 `setup-windows-python-venv.bat`

##   设置机器人qq号、密码及验证
    * 目录行运行`go-cqhttp-940fix5` 目录里的`go-cqhttp_windows_amd64.exe`
        * 参考`config.json-`用文本编辑器（如`vscode`）编辑修改 `config.json`: 机器人`qq`号(`uin`)和密码(`password`)以及``go-cqhttp_windows_amd64.exe``
    * 再次运行`go-cqhttp_windows_amd64.exe`, 并按要求验证qq号。

## 启动 `nonebot2` 及 `go-cqhttp`
命令行运行或点击koyeb-nb目录里的
    `start-dev.bat`

## 写插件
在`koyeb_nb2\plugins`目录里新开 `.py`插件文件，编辑、存盘时`nonebot2`会重新启动载入新的插件文件。