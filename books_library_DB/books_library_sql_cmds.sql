-- Create a database to manage library of books
create database books_library

-- Select database
use books_library

--Create table called books to maintain collection of books in library
create table books
(
book_title varchar(50) not null primary key,
author varchar(20) not null,
published_date date,
quantity int not null
)

-- alter table to add default constraint to quantity column
alter table books
add constraint DF_books_qty
default 0 for quantity

-- Insert values into table
insert into books values('Learning Python', 'Mark Lutz', '2013-06-13', 10)
insert into books values('Head first Python', 'Paul Barry', '2016-12-16', 24)
insert into books values('Introduction to Machine Learning', 'Sarah Guido', '2013-06-13', 8)
insert into books values('Artificial Intelligence in Practice', 'Bernard Marr', '2018-07-13', 12)
insert into books values('Deep Learning', 'Ian Goodfellow', '2013-06-13', 6)
insert into books (book_title, author) values('I, Robot', 'Isaac Asimov')

-- Update a row in table
update books
set quantity = 15
where book_title = 'Deep Learning'

-- Delete a row in table
delete from books
where author = 'Paul Barry'

-- Display Table
select * from books

-- Stored proceedure to get all books
create procedure sp_get_books
as
begin
    select * from books
end

-- Stored proceedure to get one book by title
create procedure sp_get_book
@book_title varchar(50)
as
begin
    select * from books where book_title = @book_title
end

-- Stored proceedure to add new book to library
create procedure sp_add_book
@book_title varchar(50),
@author varchar(20),
@published_date date = null,
@quantity int = 0 
as
begin
    insert into books values(@book_title, @author, @published_date, @quantity)
end

-- Stored proceedure to update a book in library
create procedure sp_update_book
@old_title varchar(50),
@book_title varchar(50),
@author varchar(20),
@published_date date = null,
@quantity int = 0 
as
begin
    update books set book_title = @book_title, author = @author, published_date = @published_date, quantity = @quantity where book_title = @old_title
end