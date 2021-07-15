# koyeb-nb2
Dockerfile.gocqhttp-nb2 for go-cqhttp-940fix5 and nonebot2

## How to use

1. `cd go-cqhttp-940fix5`, run `go-cqhttp` and ready `config.hjson`/` device.json`

	换到`go-cqhttp-940fix5`目录里。运行`go-cqhttp` 生成config.hjson。填上机器人的qq号和密码。参考config.hjson- 修改reverse_url 及设置端口（8680）。再次运行 `go-cqhttp` 完成验证生成 `device.json`
2. run `docker build -t koyeb-nb -f Dockerfile.gocqhttp-nb2 .`
3. run `docker run --rm koyeb-nb`

## Where to use
 in `koyeb` and such serverless services that support docker deployments.
