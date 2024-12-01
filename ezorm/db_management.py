from ezorm.utils import remove_escape_characters
from ezorm.utils import duck_connection
from ezorm.utils import create_directory
from ezorm import DATABASE
from typing import List, Dict, Any, Type
from ezorm import EzORM
from ezorm.validation import isinstance_ezorm
from ezorm.utils import execute

def create_tbl_query(table:Type[EzORM])->str:
    isinstance_ezorm(table)
    data_types = {
        str: "TEXT",    # or "TEXT" for unlimited length
        int: "INTEGER",
        float: "FLOAT",    # or "REAL" depending on the database
        bool: "BOOLEAN",
        # "datetime": "DATETIME"  # Use "TIMESTAMP" for PostgreSQL
    }

    query = []

    for field, detail in table.model_fields.items():
        proxy = []
        proxy.append(f"""{field} {data_types[detail.annotation]}""")
        is_required = detail.is_required()
        
        if is_required:
            proxy.append(f"""NOT NULL""")
        else:
            default = detail.default
            if (default is not None) and (default != ""):
                if isinstance(detail.default, bool):
                    proxy.append(f"""DEFAULT {str(default).upper()}""")
                elif isinstance(detail.default, str):
                    proxy.append(f"""DEFAULT '{default}'""")
                else:
                    # print("default", type(default), default)
                    proxy.append(f"""DEFAULT {default}""")
                    
        query.append(" ".join(proxy))

    query = ", ".join(query)
    query = remove_escape_characters(query).strip()

    QUERY = f"""CREATE TABLE IF NOT EXISTS {table.__table__} ( {query} );"""
    return QUERY

def delete_tbl_query(table:Type[EzORM])->str:
    isinstance_ezorm(table)
    QUERY = f"""DROP TABLE IF EXISTS {table.__table__};"""
    return QUERY

def create_tables(tables:List[EzORM]):
    create_directory(db_path=DATABASE)
    for table in tables:
        query = create_tbl_query(table)
        # print(query)
        execute(query, [])
        print(f"Model: {table.__table__} created successfully")
    print("All tables created successfully")

def delete_tables(tables:List[EzORM]):
    for table in tables:
        query = delete_tbl_query(table)
        # print(query)
        execute(query, [])
        print(f"Model: {table.__table__} deleted successfully")
    print("All tables deleted successfully")