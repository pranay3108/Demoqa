from utils.api_client import APIClient

def test_get_books(base_url, headers):
    client = APIClient(base_url, headers)

    response = client.get("/BookStore/v1/Books")

    assert response.status_code == 200
    print(response)

def test_get_book(base_url, headers):
    client = APIClient(base_url, headers)

    response = client.get("/BookStore/v1/Book")

    assert response.status_code == 200
    print(response)