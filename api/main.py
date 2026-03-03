from fastapi import FastAPI
import os
from pymongo import MongoClient

# Load environment variables (reuse same pattern)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "books")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "books")

app = FastAPI(title="Books API")

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/books")
def get_books(limit: int = 50):
    books = list(collection.find().limit(limit))
    for book in books:
        book["_id"] = str(book["_id"])
    return books


@app.get("/books/{book_id}")
def get_book(book_id: str):
    book = collection.find_one({"_id": book_id})
    if not book:
        return {"error": "Book not found"}
    book["_id"] = str(book["_id"])
    return book