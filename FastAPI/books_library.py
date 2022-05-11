import pymssql
import os
from datetime import date

class DBException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class BooksDB():

    def __init__(self) -> None:
        SQL_SERVER = os.environ['CFP_ASQL_server']
        USER = os.environ['CFP_ASQL_user']
        PWD = os.environ['CFP_ASQL_password']
        DB = os.environ['CFP_ASQL_DB']
        self.db_conn = pymssql.connect(server=SQL_SERVER, user=USER, password=PWD, database=DB)
        self.cursor = self.db_conn.cursor()
        #self.cursor.execute("use books_library")

    def get_all_books_from_db(self) -> dict|str:
        """
            Description:
                Retrieves all books from the Database
            
            Return:
                returns a Dictionary
        """
        try:
            self.cursor.execute("exec sp_get_books")
            rows = self.cursor.fetchall() 
            table_row_list = {row[0]:list(row) for row in rows}
            return table_row_list
        except Exception as e:
            return f"Failed to execute query: {e}"
    
    def get_book_from_db(self, title: str) -> dict|str:
        """
            Description:
                Retrieves a book from the Database that matches title
            
            Parameter:
                title: Title of the book
            
            Return:
                returns a Dictionary
        """
        try:
            self.cursor.execute(f"exec sp_get_book '{title}'")
            rows = self.cursor.fetchall() 
            table_row_list = {row[0]:list(row) for row in rows}
            if len(table_row_list) == 0:
                raise DBException(f"'{title}' could not be found in Library")
            return table_row_list
        except Exception as e:
            return f"Failed to execute query: {e}"
    
    def add_book_to_db(self, title: str, author: str, pub_date: date, qty: int) -> str:
        """
            Description:
                Adds a book to the Database
            
            Parameter:
                title: Title of the book
                author: Author of the book
                pub_date: Published date
                qty: quantity
            
            Return:
                returns a string
        """
        try:
            self.cursor.execute(f"exec sp_add_book '{title}', '{author}', '{pub_date}', {qty}")
            return "Succesfully executed"
        except Exception as e:
            self.db_conn.rollback()
            return f"Failed to execute query: {e}"
        finally:
            self.db_conn.commit()
    
    def update_book_in_db(self, old_title: str,new_title: str, author: str, pub_date: date, qty: int) -> str:
        """
            Description:
                Updates a book in the Database
            
            Parameter:
                old_title: Title of the book to edit
                new_title: Updated title of the book
                author: Updated Author of the book
                pub_date: Updated Published date
                qty: quantity
            
            Return:
                returns a string
        """
        try:
            self.cursor.execute(f"exec sp_update_book '{old_title}', '{new_title}', '{author}', '{pub_date}', {qty}")
            return "Succesfully executed"
        except Exception as e:
            self.db_conn.rollback()
            return f"Failed to execute query: {e}"
        finally:
            self.db_conn.commit()
    
    def delete_book_from_db(self, title: str) -> str:
        """
            Description:
                Deletes a book from the Database that matches title
            
            Parameter:
                title: Title of the book
            
            Return:
                returns a string
        """
        try:
            self.cursor.execute(f"delete from books where book_title = '{title}'")
            return "Succesfully executed"
        except Exception as e:
            self.db_conn.rollback()
            return f"Failed to execute query: {e}"
        finally:
            self.db_conn.commit()