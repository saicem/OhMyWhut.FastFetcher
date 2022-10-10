# OhMyWhut.FastFetcher

> Python 怎么会 fast 呢？ 因为写起来很 fast

# web api

main.py 用于 fastapi 部署

## 爬虫

先执行 [get_room_csv.py](spider/get_room_csv.py)，
得到 room.csv，
再执行 [get_meter_csv.py](spider/get_meter_csv.py)，
得到 meter.csv。

> 可能因为登录状态丢失导致爬虫中途挂了，从断的地方继续就好。

数据（可以直接拿来用）

- [room_2210.csv](docs/room_2210.csv)
- [meter_2210.csv](docs/meter_2210.csv)
