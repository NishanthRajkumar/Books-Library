import pyodbc
import pandas as pd

class BooksDB():

    def __init__(self) -> None:
        self.db_conn = pyodbc.connect('DSN=ms sql;')
        self.cursor = self.db_conn.cursor()
        self.cursor.execute("use books_library")

    def get_all_books_from_db(self):
        """
            Description:
                Retrieves all books from the Database
            
            Return:
                returns a Dictionary
        """
        self.cursor.execute("select * from books")
        rows = self.cursor.fetchall() 
        table_row_list = {row[0]:list(row) for row in rows}
        return table_row_list
    
    def get_book_from_db(self, title: str):
        """
            Description:
                Retrieves a book from the Database that matches title
            
            Parameter:
                title: Title of the book
            
            Return:
                returns a Dictionary
        """
        self.cursor.execute(f"select * from books where book_title = '{title}'")
        rows = self.cursor.fetchall() 
        table_row_list = {row[0]:list(row) for row in rows}
        return table_row_list
    
    def add_book_to_db(self, title: str, author: str, pub_date: str, qty: int):
        """
            Description:
                Adds a book to the Database
            
            Parameter:
                title: Title of the book
                author: Author of the book
                pub_date: Published date
                qty: quantity
            
            Return:
                returns a Dictionary
        """
        self.cursor.execute(f"insert into books values('{title}', '{author}', '{pub_date}', {qty})")