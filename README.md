# ScratchAi-server

## 使用说明
- 安装依赖
    - 开发环境为python3.7,如果安装依赖后仍然有库不能使用,可能是库的版本问题,安装相应版本的库即可
```
$ pip install -r requirements.txt
```

- 创建数据库

- 修改server.steeing.py文件中数据库URI为对应的数据库
```
# 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/test'
```

- 自动生成数据库的数据
```
$ flask shell
>>> from server import fakes
>>> fakes.db_init()
```
