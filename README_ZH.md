# Database-Migration

数据库迁移工具，支持部分数据迁移并保证数据完整性

## 文档

中文|[English](./README.md)

## 状态

持续研发中

## 需求

- [x] 迁移数据库和表结构
- [x] 迁移数据库表数据并做简单数量限制
- [x] Conda 以及 pip 安装的支持
- [ ] Docker 环境支持
- [x] Yaml 配置文件支持
- [ ] Json 配置文件支持
- [ ] 迁移完整的依赖数据（外键）
- [ ] 强大的筛选器规则

## 如何安装

下载项目并在命令行中进入到项目根目录，包括了`environment.yaml`/`requirements.txt`/`migration.template.yaml`/`migration.py` 等文件。

### Conda 环境

```shell
conda env create -f environment.yaml
activate database-migration
```

### PIP

> 开发 python 版本: Python 3.6.10

```shell
pip install -r requirements.txt
```

### Docker

>  稍后更新

## 如何使用

在安装完成后，可以执行 `python migration.py -h` 获取更多帮助信息

```shell
# python migration.py -h
usage: migration.py [-h] [-v] [-f FILE] [-y]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f FILE, --file FILE  migration config file, default: migration.yaml
  -y, --yes             without warning information
```

然后，拷贝`migration.template.yaml`或者下面的模板文件到 `migration.yaml` 然后把你需要迁移的正确配置写进去。

> 安全起见，建议 src 连接到只读库中

Yaml config:

```yaml
src:
  type: mysql
  host: 127.0.0.1
  port: 3306
  user: root
  passwd: root
dst:
  type: mysql
  host: 127.0.0.1
  port: 3306
  user: root
  passwd: root
rules:
  limit: 10000
database:
  - database1
  - name: database2
    tables:
      - table1
      - name: table3
        rules:
          limit: 100
      - table2
```

JSON config **(开发中)**:

```json
{
  "src": {
    "type": "mysql",
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "root"
  },
  "dst": {
    "type": "mysql",
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "root"
  },
  "rules": {
    "limit": 10000
  },
  "database": [
    "database1",
    {
      "name": "database2",
      "tables": [
        "table1",
        {
          "name": "table3",
          "rules": {
            "limit": 100
          }
        },
        "table2"
      ]
    }
  ]
}
```

| 参数       | 备注                                                         | 必填 |
| ---------- | ------------------------------------------------------------ | ---- |
| src        | 源数据库                                                     | 是   |
| src.type   | 源数据库类型，目前只支持MySQL                                | 是   |
| src.port   | 源数据库端口                                                 | 是   |
| src.user   | 源数据库用户                                                 | 是   |
| src.passwd | 源数据库密码                                                 | 是   |
| dst        | 目标数据库                                                   | 是   |
| dst.type   | 目标数据库类型，目前只支持MySQL                              | 是   |
| dst.port   | 目标数据库端口                                               | 是   |
| dst.user   | 目标数据库用户                                               | 是   |
| dst.passwd | 目标数据库密码                                               | 是   |
| rules      | 需要是一个映射对象，支持参数 limit: number, order_filed: order field, order: asc/desc, 默认: `{"limit": None, "order_field": None, "order": 'asc'}` | 否   |
| database   | 迁移的数据库，可以写为扩展形式 `{"name": "database name", "tables": ["table1", "table2", {"name": "table3", "rules": {...}}]}` | 是   |

> database 和 database.tables 支持简写为一个名称

最后，执行  `python migration.py -f migration.yaml` 并且确认迁移，脚本将会自动进行迁移操作，如果不想点确认或者想在定时任务里边运行，可以运行 `/path/to/python /path/to/migration.py -y -f migration.yaml`。