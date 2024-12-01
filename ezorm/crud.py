from ezorm import EzORM
from typing import List
from ezorm.utils import remove_escape_characters

class Read:
    def __init__(self, table:EzORM, select:List[str]=None, where:List[str]=None):
        self.select = select
        self.table = table
        self.where = where
    
    @staticmethod
    def select_query(select:List[str]):
        if select is None or len(select) == 0:
            return "SELECT *"
        query = f"SELECT {", ".join([field for field in select])}"
        return query

    @staticmethod
    def table_query(table:EzORM):
        query = f"FROM {table.__table__}"
        return query

    @staticmethod
    def where_query(where:List[str]):
        if where is None:
            return ""
        query = f"WHERE "
        return query

    def query(self, ):
        select = self.select_query(self.select)
        table = self.table_query(self.table)
        where = self.where_query(self.where)
        query = " ".join([select, table, where]).strip()
        query = remove_escape_characters(query)
        query = f"{query};"
        return query