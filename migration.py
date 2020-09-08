import os
import time
import yaml
import sys
import argparse
from connector.ConnectorFactory import ConnectorFactory
from operate.MigrationOperation import MigrationOperation

version = "v1.0"


def parse_config(fp):
    content = fp.read()
    return yaml.load(content, Loader=yaml.FullLoader)


def build_migration_plan(config):
    plan = []
    err = []
    # 1. check src and dst connection
    src_con = ConnectorFactory.generate(config["src"]["type"], {
        "host": config["src"]["host"],
        "port": config["src"]["port"],
        "user": config["src"]["user"],
        "passwd": config["src"]["passwd"],
    })
    dst_con = ConnectorFactory.generate(config["dst"]["type"], {
        "host": config["dst"]["host"],
        "port": config["dst"]["port"],
        "user": config["dst"]["user"],
        "passwd": config["dst"]["passwd"],
    })
    database_names = src_con.get_databases()
    for item in config['database']:
        # support dict and pure database name, default tables is all
        if isinstance(item, dict):
            if "name" not in item:
                err.append("[database] config map require name %s" % item)
                continue
            database = item["name"]
        elif isinstance(item, str):
            database = item
        else:
            err.append("[database] not support database config type %s, only map or string" % type(item))
            continue
        if database not in database_names:
            err.append("[database] %s is not found" % database)
            continue
        # 2. check database_name and get database tables
        database_tables = src_con.get_database_tables(database)
        tables = database_tables
        # special custom tables
        if isinstance(item, dict) and "tables" in item:
            tables = item["tables"]

        # 3. built plan and check table_name
        for table in tables:
            rules = {**config["rules"]}
            if isinstance(table, dict):
                if "name" not in table:
                    print("[table] config map require name")
                    continue
                table_name = table["name"]
                if "rules" in table:
                    rules = {**rules, **table["rules"]}  # merge rules
            elif isinstance(table, str):
                table_name = table
            else:
                err.append("[table] not support database config type %s" % type(item))
                continue

            if table_name not in database_tables:
                err.append("[table] %s is not found at database:%s" % (table_name, database))
                continue

            plan.append({
                "src_con": src_con,
                "dst_con": dst_con,
                "database": database,
                "table": table_name,
                "rules": rules
            })
    return plan, err


def show_migration_plan(config, plan):
    for item in plan:
        print("[migration] %s > %s %s.%s by rules: %s" % (
            config["src"]["host"], config["dst"]["host"], item["database"], item["table"], item["rules"]))


def migration_database(plan):
    print("[migration] started")
    start_micro_time = int(time.time() * 1000)
    # prepare migration database struct
    for item in plan:
        migration = MigrationOperation(item["src_con"], item['dst_con'])
        # 1. migration database strct
        migration.migration_database_struct(item["database"])
        # 2. migration table struct
        migration.migration_table_struct(item['database'], item['table'])
        # 3. migration table data
        migration.migration_table_data(item['database'], item['table'], item['rules'])
    end_micro_time = int(time.time() * 1000)
    print("[migration] ended between %.3f" % ((end_micro_time - start_micro_time) / 1000))


def run():
    default_config_path = os.path.join(os.getcwd(), 'migration.yaml')
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action="version",
                        version="Version: %s, open source by https://github.com/wangerzi" % version)
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), required=False, default=default_config_path,
                        help="migration config file, default: migration.yaml")
    parser.add_argument('-y', '--yes', action="store_true", help="without warning information")

    args = parser.parse_args()
    config = parse_config(args.file)
    plan, err = build_migration_plan(config)
    if len(err):
        print("[Error] Got following errors, please check config file first!")
        print(err)
        return
    show_migration_plan(config, plan)
    if not args.yes:
        if input("Continue (Y/N)? ").lower() != 'y':
            return
    migration_database(plan)


if __name__ == "__main__":
    sys.path.append(os.getcwd())
    run()
