from abc import ABC, abstractmethod

class DBUtils(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_tables(self):
        pass

    @abstractmethod
    def get_create_table_statement(self, table_name):
        pass

    @abstractmethod
    def close(self):
        pass
