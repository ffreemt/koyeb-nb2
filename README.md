# koyeb-nb2
[![nonebot2](https://img.shields.io/static/v1?label=nonebot&message=v2.0.0b4&color=green)](https://v2.nonebot.dev/)[![onebot](https://img.shields.io/static/v1?label=driver&message=onebot&color=green)](https://v2.nonebot.dev/guide/cqhttp-guide.html)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Nonebot2 up and running with ease

<!--Dockerfile.gocqhttp-nb2 for go-cqhttp-940fix5 and nonebot2-->
([中文](https://github.com/ffreemt/koyeb-nb2/blob/master/dumbot.md))

## Oneclick start
- Authenticate when necessary

    `cd go-cqhttp` && `go-cqhttp`

    or copy valid `config.yml` `session.token` `session.token` to the `go-cqhttp` directory.
- Run `start_nb.py` in  the `koyeb-nb2` directory
    ```python
    python start_nb2.py
    ```

## Setup for plugin dev

### Clone/fork this repo

E.g.
```bash
git clone https://github.com/ffreemt/koyeb-nb2
```

### Authenticate
In `go-cqhttp-940fix5`, run `go-cqhttp` and ready `config.hjson`/` device.json`

换到`go-cqhttp`目录里。运行`go-cqhttp` 生成config.hjson。编辑`config.hjson`填上机器人的qq号和密码，参考config.hjson- 修改reverse_url 及设置端口（8680）。再次运行 `go-cqhttp` 完成验证生成 `device.json`

## Three ways to use it

### Run it in Docker Locally

In `koyeb-nb`

1.   run
         ```
        docker build -t koyeb-nb -f Dockerfile.gocqhttp-nb2 .`
         ```
2.   run `docker run --rm koyeb-nb`

3.   (Optional) Upload to Docker Hub ([https://hub.docker.com/](https://hub.docker.com/))
    ```
    export DOCKER_ID=your_docker_id  # hub.docker.com
    docker tag koyeb-nb:latest $DOCKER_ID/koyeb-nb:latest
    docker push $DOCKER_ID/koyeb-nb:latest
    ```
4.   Test the bot
    *  Send a private message to the bot: `/echo hey ya`
    *  Send a group message to the bot: `@botname /echo sup`

5.  Install more plugins and repeat 1-2.

    For example, `poetry add nonebot-plugin-guess`

    Readily made plugins are available
    [https://v2.nonebot.dev/store.html](https://v2.nonebot.dev/store.html)

    You can also copy plugin directly to koyeb_nb2/plugins.

### Run it in Docker in Cloud
 For example, in `koyeb` and such serverless services that support docker deployments.

### **For Testing Plugins Locally 本地开发测试插件**
Optionally use a venv, e.g., `python -m venv venv && source venv/bin/activate` in Linux or `python -m venv venv && venv/Scripts/activate` in Windows.

1. Install packages
In `koyeb-nb`, run `pip install -r requirements.text`

    Or run `poetry install` and **`pip install nonebot2 -U`** since we need `nonebot2a13post1` but poetry cannot handle `post`.

2. Run `go-cqhttp`/`nonebot` and make your own plugin
    *   In `go-cqhttp-940fix5`, run `go-cqhttp`
        N.B. For Windows, download and run go-cqhttp.exe

    *   In `koyeb-nb`, run `uvicorn --port 8680 bot:app --reload --reload-dir koyeb_nb2`
    *   In `koyeb_nb2/plugins`, create/edit/save `fancy_plugin.py`
