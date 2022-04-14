import pyodbc
import pandas as pd

db_conn = pyodbc.connect('DSN=mssqldsn;')

cursor = db_conn.cursor()

cursor.execute("use books_library") 
cursor.execute("select * from books") 
rows = cursor.fetchall() 
table_row_list = [list(row) for row in rows]

df = pd.DataFrame(table_row_list, columns=['book_title', 'author', 'published_date', 'quantity'])

print(df)