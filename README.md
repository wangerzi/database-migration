# Database-Migration

For database migration, support partial data migration with complete dependency data.

## Document

English|[中文](./README_ZH.md)

## Status

developing

## Features

- [x] migration database and table struct
- [x] migration table data with sample limit
- [x] Conda and pip support
- [ ] Docker environment support
- [x] Yaml config support
- [ ] Json config support
- [ ] migration with complete dependency data (foreign key).
- [ ] strongth filter rules

## How to install

Clone this project and open terminal to project root folder what contains `environment.yaml`/`requirements.txt`/`migration.template.yaml`/`migration.py` etc.

### Conda Environment

```shell
conda env create -f environment.yaml
activate database-migration
```

### PIP

> Development python version: Python 3.6.10

```shell
pip install -r requirements.txt
```

### Docker

>  Comming soon

## How to use

After installation, you can execute `python migration.py -h` to got more help information.

```shell
# python migration.py -h
usage: migration.py [-h] [-v] [-f FILE] [-y]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f FILE, --file FILE  migration config file, default: migration.yaml
  -y, --yes             without warning information
```

Then, copy `migration.template.yaml` or this following yaml content to `migration.yaml` and customize your own migration config.

>  For safety, it is recommended that src connect to the read-only database

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

JSON config **(Developing)**:

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

| param      | Comment                                                      | required |
| ---------- | ------------------------------------------------------------ | -------- |
| src        | source of the database                                       | true     |
| src.type   | type of the source database, support mysql only at now.      | true     |
| src.port   | port of the source database                                  | true     |
| src.user   | User of the source database                                  | true     |
| src.passwd | password of the source database                              | true     |
| dst        | target of the database                                       | true     |
| dst.type   | type of the target database, support mysql only at now.      | true     |
| dst.port   | port of the target database                                  | true     |
| dst.user   | User of the target database                                  | true     |
| dst.passwd | password of the target database                              | true     |
| rules      | should be a map, support limit: number, order_filed: order field, order: asc/desc, default: `{"limit": None, "order_field": None, "order": 'asc'}` | false    |
| database   | Migration databases, you can expend as `{"name": "database name", "tables": ["table1", "table2", {"name": "table3", "rules": {...}}]}` | true     |

> database and database.tables support `shorthand` that only config a name

At last, execute `python migration.py -f migration.yaml` and confirm execution, it will migration automatic, if you don't want to confirm or you want to  migration by crontab automitic, you can use `/path/to/python /path/to/migration.py -y -f migration.yaml`