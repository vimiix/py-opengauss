### 关于

该分支是基于 py-postgresql 1.3.0 版本，新增了两个特性：
- 支持 opengauss 数据库连接
- 支持多 IP 连接

区别于主分支的是，当前分支用于手动通过源码安装，安装后的在代码中引用的包名依旧是 `postgresql`，
这样做的目的是便于集成到 ORM 框架中使用，比如 **sqlalchemy** 等。
而主分支的版本主要用于直接使用驱动执行sql的场景，便于直接通过 pip 安装。

### 安装方式

	$ git clone -b for-orm https://github.com/vimiix/py-opengauss.git
	$ cd py-opengauss
	$ python3 setup.py install

### 连接方式：

> 支持的连接协议列表: ['pq', 'postgres', 'postgresql', 'og', 'opengauss']

```python
>>> import postgresql
# General Format:
>>> db = postgresql.open('pq://user:password@host:port/database')

# Also support opengauss scheme:
>>> db = postgresql.open('opengauss://user:password@host:port/database')

# multi IP support, will return PRIMARY instance connect:
>>> db = postgresql.open('opengauss://user:password@host1:123,host2:456/database')

# Connect to 'postgres' at localhost.
>>> db = postgresql.open('localhost/postgres')
```

### 基本用法

```python
import postgresql
db = postgresql.open('opengauss://user:password@host:port/database')

get_table = db.prepare("SELECT * from information_schema.tables WHERE table_name = $1")
print(get_table("tables"))

# Streaming, in a transaction.
with db.xact():
	for x in get_table.rows("tables"):
		print(x)
```

### sqlalchemy 集成用法

由于 sqlalchemy 仅支持单个主机的连接方式，所以要想使用多主机的连接方式，需下载定制版的 sqlalchemy 

https://github.com/vimiix/sqlalchemy

```python
from sqlalchemy import create_engine
# 初始化opengauss数据库多主机连接（适用于没有固定虚拟IP的数据库主备集群）:
engine = create_engine('postgresql+pyopengauss://user:password@host1:port1,host2:port2/db')
```

### Documentation

http://py-postgresql.readthedocs.io

### Related

- http://postgresql.org
- http://python.org
