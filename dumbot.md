# `dumbot`机器人
[![nonebot2](https://img.shields.io/static/v1?label=nonebot&message=v2.0.0a16&color=green)](https://v2.nonebot.dev/)[![cqhttp](https://img.shields.io/static/v1?label=driver&message=cqhttp&color=green)](https://v2.nonebot.dev/guide/cqhttp-guide.html)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`Windows 10`里写`nonebot2`插件（基于`Nonebot2 + go-cqhttp`）

（[英文（本地及云里docker运行noenbot2）](https://github.com/ffreemt/koyeb-nb2/blob/master/README.md)）

## 准备工具
*   安装 `python 3.7` 或以上（谷歌bing或百度）
*  下载 koyeb-nb repo

    例如，命令行运行 `git clone https://github.com/ffreemt/koyeb-nb2`

## (可选）建立 Python 虚拟环境`venv`
```bash
cd path-to-koyeb-nb
python -V  # 确认 python 版本是 3.7 或更高
python -m venv venv
# 或用 py -3.7 -m venv venv

venv\Scripts\activate
python -m pip install pip -U
```
如果系统里装了Python3.7，也可以命令行运行 `setup-windows-python-venv.bat` 或点击 `setup-windows-python-venv.bat`

## 安装`pip`包
命令行换到`koyeb-nb`目录（例如`cd path-to-koyeb-nb`）运行
```bash
python -m pip install -r requirements-win.txt
```

或进入建立好的`Python`虚拟环境`venv`里命令行下运行

*   `venv\Scripts\activate`

需要注意的是，如果`python -m pip install -r requirements-win.txt`是在`Python`虚拟环境`venv`做的，则一下各步都必须先进入`Python`虚拟环境`venv`。

##   设置机器人qq号、密码及验证
* 命令行运行`go-cqhttp-940fix5` 目录里的`go-cqhttp_windows_amd64.exe`
    * 参考`config.json-`用文本编辑器（如`vscode`）编辑修改 `config.json`: 机器人`qq`号(`uin`)和密码(`password`)以及``reverse_url``
* 再次运行`go-cqhttp_windows_amd64.exe`, 并按要求验证qq号

## 启动 `nonebot2` 及 `go-cqhttp`
分开启动`go-cqhttp`和`nonebot2`
*   命令行在`go-cqhttp-940fix5` 目录里运行`go-cqhttp_windows_amd64.exe`
*   命令行在`koyeb-nb`目录里运行 `uvicorn --host 0.0.0.0 --port 8680 bot:app --reload --reload-dir koyeb_nb2`

如希望做到一键启动，则需要安装`pm2`:
*   安装 `nodejs` （谷歌bing或百度）
*   安装 `pm2`
    *  命令行运行 `npm install pm2 -g`  # 参看[https://www.npmjs.com/package/pm2/v/4.4.0](https://www.npmjs.com/package/pm2/v/4.4.0)

**一键启动**：命令行运行或点击`koyeb-nb`目录里的
    `start-dev.bat`

## 写插件
在`koyeb_nb2\plugins`目录里新开或修改 `.py`插件文件，编辑、存盘时`nonebot2`会重新启动载入新的插件文件。

`koyeb_nb2\plugins`含几个插件的雏形
*   `admin_page`：类似`server`酱私人推送服务
*   `wotd`: `thefreedictionary.com`每日一字一短语随机推送
*   `welcome_memb`：欢迎新人入群
*   `news`: 新闻一览，/news /新闻 /xinwen
*   中英德法四语闲聊：群里艾特或发私信给bot，中：青云客接口，英：微软GPT对话小模型，德法： 基于恐龙AIML语言

## 可选

充分利用`package.json`:

*  安装 `nodejs`
*  安装`nodemon` + `yarn` 或 `npm`
    *   命令行在`koyeb-nb`目录运行`yarn`或`npm install`
*  安装`pip`包: pyright, pydocstyle, pep257, black, flake8

    命令行运行 `yarn style` 等等，参看`package.json`。
