# OhMyWhut.FastFetcher

> Python 怎么会 fast 呢？ 因为写起来很 fast

# web api

main.py 用于 fastapi 部署

功能如下

- 电费查询
- 图书查询
- 课表(JSON,ical,png)

样例

<img src="docs/course.png" width="35%" alt="课表示例图片">

接口参考,运行 [main.py](main.py) 后查看 http://127.0.0.1:8000/docs

## 部署

[Dockerfile](Dockerfile) 直接用就好，[config.py](config.py) 需要更改一下，字体呀，开学日期呀。

也可以用已经构建好的镜像
https://hub.docker.com/repository/docker/saicem/fast-fetcher

修改一下，本地的开放端口

```shell
docker pull saicem/fast-fetcher
docker run -d -p 8000:8000 saicem/fast-fetcher 
```

字体用的是[霞鹜文楷](https://github.com/lxgw/LxgwWenKai)，可以自行更改

## 爬虫

先执行 [get_room_csv.py](spider/get_room_csv.py)，
得到 room.csv，
再执行 [get_meter_csv.py](spider/get_meter_csv.py)，
得到 meter.csv。

> 可能因为登录状态丢失导致爬虫中途挂了，从断的地方继续就好。

数据（可以直接拿来用）

- [room_2210.csv](docs/room_2210.csv)
- [meter_2210.csv](docs/meter_2210.csv)