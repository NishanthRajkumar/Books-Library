from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
import uvicorn

app = FastAPI()

library_user = {
    "Nishanth": {
        "username": "Nishanth",
        "password": "qwerty1234"
    }
}


# openssl rand -hex 32
SECRET_KEY = "b06c4ea62b387382b4a5e1597ae9c92b520254fcbec19f894ac0912fa0f61d7c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username not in library_user.keys():
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


class Book(BaseModel):
    author: str
    title: str
    price: float|None  = None

class Token(BaseModel):
    access_token: str
    token_type: str

my_library: dict[str, Book] = {}

@app.post("/login", response_model=Token, tags=['Login'])
def login(formdata: OAuth2PasswordRequestForm = Depends()):
    """
        Description:
            Authenticate the username and password entered
        
        Parameter:
            username: login username as string
            password: Password as string
    """
    if formdata.username in library_user.keys():
        if library_user.get(formdata.username)["password"] == formdata.password:
            access_token = create_access_token({"sub": formdata.username})
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/", tags=['Library books'])
def retrieve_all_books(current_user: str = Depends(get_current_user)):
    """
        Description:
            Retrieves all books from the library
        
        Parameter:
            None
        
        Return:
            A dictionary containing collection of books
    """
    return f"Books in our library:\n{my_library}"

@app.get("/book/{book_title}", tags=['Library books'])
def retrieve_a_book(book_title: str, response: Response, current_user: str = Depends(get_current_user)):
    """
        Description:
            Retrieves a book from the library
        
        Parameter:
            book_title: title of the book to retrieve
            response: for the http response
        
        Return:
            A Book object
    """
    if book_title in my_library.keys():
        return my_library[book_title]
    response.status_code = status.HTTP_404_NOT_FOUND
    return f"The book '{book_title}' is not in our library"

@app.post("/add-book/", status_code=status.HTTP_201_CREATED, tags=['Library books'])
def add_book_to_library(book_to_add: Book, current_user: str = Depends(get_current_user)):
    """
        Description:
            adds a book to the library
        
        Parameter:
            book_to_add: A Book object to add to library
        
        Return:
            A string message
    """
    if book_to_add.title in my_library.keys():
        return f"Failed to add the book. Book with title '{book_to_add.title}' already exists in library"
    my_library[book_to_add.title] = book_to_add
    return f"Succesfully added the book '{book_to_add.title}' to collection"

@app.put("/update-book/", tags=['Library books'])
def update_book_info(book_title: str, new_book_info: Book, current_user: str = Depends(get_current_user)):
    """
        Description:
            Updates a book from the library
        
        Parameter:
            book_title: The title of the book to edit
            new_book_info: A Book object to add to library
        
        Return:
            A string message
    """
    if book_title in my_library.keys():
        if book_title == new_book_info.title:
            my_library[book_title] = new_book_info
            return "Succesfully updated the book"
        if new_book_info.title in my_library.keys():
            return f"Failed to update! The new book title '{new_book_info.title}' already exists in library"
        else:
            my_library[new_book_info.title] = new_book_info
            my_library.pop(book_title)
            return f"Succesfully updated the book"
    return f"Failed to update the book '{book_title}'. The book '{book_title}' is not in our library"

@app.delete("/delete-book/", tags=['Library books'])
def delete_book(book_title: str, current_user: str = Depends(get_current_user)):
    """
        Description:
            deletes a book from the library
        
        Parameter:
            book_title: The title of the book to delete
        
        Return:
            A string message
    """
    if book_title in my_library.keys():
        deleted_book = my_library.pop(book_title)
        return f"\n{deleted_book}\nThis book has been deleted succesfully"
    return f"Failed to delete the book '{book_title}'. The book '{book_title}' is not in our library"

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8500)