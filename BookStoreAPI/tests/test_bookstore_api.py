import os
import pytest
import logging
from utils.helper import update_env_variable


logger = logging.getLogger(__name__)


def test_get_books(api_client):
    response = api_client.get("/BookStore/v1/Books")
    assert response.status_code == 200
    
    books = response.json().get("books", [])
    assert len(books) > 0, "Book list is empty!"
    
    logger.info(f"Retrieved {len(books)} books")
    logger.info(f"First Book ISBN: {books[0].get('isbn')}")

def test_get_book(api_client):
    # 1. Fetch the list first to get a valid ISBN dynamically
    books_response = api_client.get("/BookStore/v1/Books")
    first_isbn = books_response.json().get("books", [])[0].get("isbn")

    # 2. Use the 'params' dictionary for a cleaner and safer request
    response = api_client.get("/BookStore/v1/Book", params={"ISBN": first_isbn})
    
    assert response.status_code == 200
    logger.info(f"Successfully retrieved book: {response.json().get('title')}")

def test_post_book(api_client):
    # 1. Fetch a valid ISBN from the store catalog to ensure it exists
    books_response = api_client.get("/BookStore/v1/Books")
    valid_isbn = books_response.json().get("books", [])[0].get("isbn")

    # ✅ Write ISBN to .env
    update_env_variable("ISBN", valid_isbn)
    user_id = os.getenv("USER_ID")
    addBook_response = api_client.post("/BookStore/v1/Books", json={
        "userId": user_id,
        "collectionOfIsbns": [
            {
                "isbn": valid_isbn
            }
        ]
    })
    # We expect a 400 if the random ISBN isn't in the store, or 201 if it were valid
    logger.info(addBook_response.json())
    assert addBook_response.status_code == 201
    logger.info(f"Tried to add random ISBN {valid_isbn}, status: {addBook_response.status_code}")

def test_put_book(api_client):
    initial_isbn = os.getenv("ISBN")
    random_isbn = "9781492078005" #The Alchemist
    user_id = os.getenv("USER_ID")
    putBook_response = api_client.put(f"/BookStore/v1/Book/{initial_isbn}", json={
        "userId": user_id,
        "isbn": random_isbn
    })
    assert putBook_response.status_code == 200



def test_delete_book(api_client):
    initial_isbn = os.getenv("ISBN")
    user_id = os.getenv("USER_ID")
    deleteBook_response = api_client.delete(f"/BookStore/v1/Book", json={
        "userId": user_id,
        "isbn": initial_isbn
    })
    assert deleteBook_response.status_code == 204
    

def test_delete_books(api_client):
    user_id = os.getenv("USER_ID")
    deleteBooks_response = api_client.delete(f"/BookStore/v1/Books/{user_id}")
    assert deleteBooks_response.status_code == 204

    


    # 2. Use the 'params' dictionary for a cleaner and safer request
    #response = api_client.get("/BookStore/v1/Book", params={"ISBN": first_isbn})
    
    #assert response.status_code == 200
    #logger.info(f"Successfully retrieved book: {response.json().get('title')}")