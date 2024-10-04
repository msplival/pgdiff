import psycopg2
import os
import subprocess
from .db_utils import DBUtils

class PostgresUtils(DBUtils):
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(**self.config)

    def get_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
        """)
        tables = cursor.fetchall()
        cursor.close()
        return set(table[0] for table in tables)

    def get_create_table_statement(self, table_name):
        # Build the connection string without password
        conn_str = f"postgresql://{self.config['user']}@{self.config['host']}:{self.config['port']}/{self.config['dbname']}"

        # Set the PGPASSWORD environment variable
        env = os.environ.copy()
        if 'password' in self.config:
            env['PGPASSWORD'] = self.config['password']

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

    def close(self):
        if self.connection:
            self.connection.close()
