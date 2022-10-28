# OhMyWhut.FastFetcher

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/)
![lines](https://img.shields.io/tokei/lines/github/saicem/OhMyWhut.FastFetcher)
![size](https://img.shields.io/github/repo-size/saicem/OhMyWhut.FastFetcher)
![issues](https://img.shields.io/github/issues/saicem/OhMyWhut.FastFetcher)
![closed issues](https://img.shields.io/github/issues-closed/saicem/OhMyWhut.FastFetcher)
[![Docker Image CI](https://github.com/saicem/OhMyWhut.FastFetcher/actions/workflows/docker-image.yml/badge.svg)](https://github.com/saicem/OhMyWhut.FastFetcher/actions/workflows/docker-image.yml)
> Python 怎么会 fast 呢？ 因为写起来很 fast

# Web API

[main.py](main.py) 用于 fastapi 部署

## 接口示例

可运行 [main.py](main.py) 后访问 http://127.0.0.1:8000/docs 查看 swagger UI

- username: 智慧理工大账号
- password: 智慧理工大密码

### 电费查询

查询 body

```json
{
  "username": "string",
  "password": "string",
  "meterId": "string",
  "factoryCode": "string"
}
```

- meterId: 查看 [meter_2210.csv](docs/meter_2210.csv)，或自行爬取，代码参考 [spider](spider) 文件夹
- factoryCode: 固定为 "E035"

返回样例

```json
{
  "data": {
    "remainPower": "88.17度",
    "remainFee": "51.14"
  }
}
```

### 图书查询

查询 body

```json
{
  "username": "string",
  "password": "string"
}
```

返回样例

```json
{
  "data": {
    "books": [
      {
        "name": "现代操作系统",
        "expire": "2023-09-24",
        "borrow": "2022-09-12"
      }
    ]
  }
}
```

### 课表 JSON

```json
{
  "data": {
    "courses": [
      {
        "Name": "形势与政策",
        "Room": "东教-合一",
        "Teacher": "南北",
        "StartWeek": 5,
        "EndWeek": 8,
        "StartSection": 6,
        "EndSection": 7,
        "DayOfWeek": 4
      }
    ]
  }
}
```

### 课表日历

```text
BEGIN:VCALENDAR
VERSION:2.0
PRODID:c505d5e6-03c9-4fa5-88ee-d0b1d23033b4
BEGIN:VEVENT
UID:74f9b8b6-65a2-4c73-a08a-ffe408aff08f
SUMMARY:形势与政策
LOCATION:东教-合一
DESCRIPTION:神马
DTSTART:20221110T060000Z
DTEND:20221110T073500Z
RRULE:FREQ=WEEKLY;INTERVAL=1;COUNT=4
END:VEVENT
END:VCALENDAR
```

或者[下载文件](docs/courses.ics)试试

> 因为 markdown 不能直接提供下载链接，所以得自己手动下载一下。

### 课表图片

<img src="docs/course.png" width="35%" alt="课表示例图片">

### 校园卡余额

```json
{
  "data": {
    "cardMoney": "8.93元"
  }
}
```

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