import configparser
from postgres_utils import PostgresUtils

def compare_schemas(source_db, target_db):
    tables1 = source_db.get_tables()
    tables2 = target_db.get_tables()

    only_in_db1 = tables1 - tables2
    only_in_db2 = tables2 - tables1

    # Generate CREATE TABLE statements for tables only in source
    print("-- Tables to create on target database:")
    for table in only_in_db1:
        create_statement = source_db.get_create_table_statement(table)
        if create_statement:
            print(create_statement)

    # Generate DROP TABLE statements for tables only in target
    print("-- Tables to drop from target database:")
    for table in only_in_db2:
        print(f"DROP TABLE IF EXISTS {table} CASCADE;")

def read_db_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    db_config = {
        'dbname': config['database']['dbname'],
        'user': config['database']['user'],
        'host': config['database']['host'],
        'port': config['database']['port']
    }
    if 'password' in config['database']:
        db_config['password'] = config['database']['password']
    return db_config

if __name__ == "__main__":
    source_config = read_db_config('source.ini')
    target_config = read_db_config('target.ini')

    source_db = PostgresUtils(source_config)
    target_db = PostgresUtils(target_config)

    source_db.connect()
    target_db.connect()

    compare_schemas(source_db, target_db)

    source_db.close()
    target_db.close()
