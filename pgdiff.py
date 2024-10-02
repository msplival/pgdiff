import psycopg2
import configparser

def get_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    cursor.close()
    return set(table[0] for table in tables)

def compare_schemas(conn1, conn2):
    tables1 = get_tables(conn1)
    tables2 = get_tables(conn2)

    only_in_db1 = tables1 - tables2
    only_in_db2 = tables2 - tables1
    in_both = tables1 & tables2

    print("Tables only in first database:")
    for table in only_in_db1:
        print(table)

    print("\nTables only in second database:")
    for table in only_in_db2:
        print(table)

    print("\nTables in both databases:")
    for table in in_both:
        print(table)

def read_db_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        'dbname': config['database']['dbname'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'host': config['database']['host'],
        'port': config['database']['port']
    }

if __name__ == "__main__":
    source_config = read_db_config('/path/to/source_config.ini')
    target_config = read_db_config('/path/to/target_config.ini')

    conn1 = psycopg2.connect(**source_config)
    conn2 = psycopg2.connect(**target_config)

    compare_schemas(conn1, conn2)

    conn1.close()
    conn2.close()
