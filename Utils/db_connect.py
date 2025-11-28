import sqlalchemy
import urllib

def get_connection():
    server_name = 'KAKOSAN\SQLEXPRESS'
    database_name = 'SQLPractice'
    connection_string = (
      f"DRIVER={{ODBC Driver 17 for SQL Server}}"
      f";SERVER={server_name}"
      f";DATABASE={database_name}"
      f";Trusted_Connection=yes;"
    )
    
    params = urllib.parse.quote_plus(connection_string)
    engine = sqlalchemy.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine
  
  