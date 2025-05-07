import pyodbc  
from  source.core.config import Settings
class DBConnection:
    def __init__(self,server_name:Settings):
        self.server_name=server_name.SERVER_SSMS

    def Get_DB_Connection(self):
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};' ## or ODBC Driver 17 for SQL Server
            f'SERVER={self.server_name};'
            'DATABASE=Law_ChatBot_DB;'
            'Trusted_Connection=yes;'
        )

        return conn
    