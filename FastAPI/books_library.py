import pyodbc

class BooksDB():

    def __init__(self) -> None:
        self.db_conn = pyodbc.connect('DSN=ms sql;')
        self.cursor = self.db_conn.cursor()
        self.cursor.execute("use books_library")

    def get_all_books_from_db(self) -> dict|str:
        """
            Description:
                Retrieves all books from the Database
            
            Return:
                returns a Dictionary
        """
        try:
            self.cursor.execute("select * from books")
            rows = self.cursor.fetchall() 
            table_row_list = {row[0]:list(row) for row in rows}
            return table_row_list
        except:
            return "Failed to execute query"
    
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
            self.cursor.execute(f"select * from books where book_title = '{title}'")
            rows = self.cursor.fetchall() 
            table_row_list = {row[0]:list(row) for row in rows}
            if len(table_row_list) == 0:
                return f"'{title}' could not be found in Library"
            return table_row_list
        except:
            return "Failed to execute query"
    
    def add_book_to_db(self, title: str, author: str, pub_date: str, qty: int) -> str:
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
            self.cursor.execute(f"insert into books values('{title}', '{author}', '{pub_date}', {qty})")
            self.db_conn.commit()
            return "Succesfully executed"
        except:
            return "Failed to execute query"
    
    def update_book_in_db(self, old_title: str,new_title: str, author: str, pub_date: str, qty: int) -> str:
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
            self.cursor.execute(f"update books set book_title = '{new_title}', author = '{author}', published_date = '{pub_date}', quantity = {qty} where book_title = '{old_title}'")
            self.db_conn.commit()
            return "Succesfully executed"
        except:
            return "Failed to execute query"
    
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
            self.db_conn.commit()
            return "Succesfully executed"
        except:
            return "Failed to execute query"