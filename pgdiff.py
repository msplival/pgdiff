#!/usr/bin/env python3

import psycopg2
import configparser
import subprocess
import os

def get_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
    """)
    tables = cursor.fetchall()
    cursor.close()
    return set(table[0] for table in tables)

def get_create_table_statement(table_name, db_config):
    # Build the connection string without password
    conn_str = f"postgresql://{db_config['user']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

    # Set the PGPASSWORD environment variable
    env = os.environ.copy()
    if 'password' in db_config:
        env['PGPASSWORD'] = db_config['password']

    # Build the pg_dump command
    cmd = [
        'pg_dump',
        '--schema-only',
        '--no-owner',
        '--table', table_name,
        '--dbname', conn_str
    ]

    # Run the command
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

    if result.returncode != 0:
        print(f"Error getting table definition for {table_name}: {result.stderr}")
        return None
    else:
        return result.stdout

def compare_schemas(conn1, conn2, source_config):
    tables1 = get_tables(conn1)
    tables2 = get_tables(conn2)

    only_in_db1 = tables1 - tables2
    only_in_db2 = tables2 - tables1

    # Generate CREATE TABLE statements for tables only in source
    print("-- Tables to create on target database:")
    for table in only_in_db1:
        create_statement = get_create_table_statement(table, source_config)
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

    conn1 = psycopg2.connect(**source_config)
    conn2 = psycopg2.connect(**target_config)

    compare_schemas(conn1, conn2, source_config)

    conn1.close()
    conn2.close()
