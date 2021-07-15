# koyeb-nb2

## How to use

1. `cd go-cqhttp-940fix5` and run go-cqhttp and ready config.hjson and device.json 
	换到go-cqhttp-940fix5 目录里。运行go-cqhttp 生成config.hjson。填上机器人的qq号和密码。参考config.hjson- 修改reverse_url 及设置端口（8680）
2. run `docker build -t koyeb-nb -f Dockerfile.gocqhttp-nb2 .`
3. run `docker run --rm koyeb-nb`
