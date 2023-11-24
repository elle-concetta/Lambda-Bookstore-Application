import ujson
from .utils import db
import bson


def retrieve_books_by_genre(genre):
    # Initialize an empty list for the result
    result = []

    # Check if a genre is provided
    if genre is None:
        return {"error": "Genre not provided."}

    # Establish a connection to the MongoDB
    mongo = db.MongoDBConnection()

    with mongo:
        database = mongo.connection['dbmodel']
        collection = database['Books']

        try:
            # Find all books that match the given genre
            books_cursor = collection.find({"genre": genre})

            # Iterate over the cursor and append book details to the result list
            for book in books_cursor:
                result.append({
                    'title': book["title"],
                    'isbn': book.get("isbn"),
                    'author': book.get("author"),
                    'genre': book.get("genre")
                })

            # If no books are found for the given genre, return an error message
            if not result:
                return {"error": "No books found for the given genre."}

        except bson.errors.InvalidId:
            return {"error": "Invalid request format."}

    return result


def lambda_handler(event, context):
    try:
        # Extract the genre from the path parameters
        genre = event.get("pathParameters", {}).get("genre")

        if not genre:
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Genre parameter is missing"
                })
            }

        # Retrieve and return the books of the specified genre
        return {
            "statusCode": 200,
            "body": ujson.dumps({
                "message": "Success",
                "data": retrieve_books_by_genre(genre)
            })
        }

    except Exception as err:
        return {
            "statusCode": 400,
            "body": ujson.dumps({
                "message": "Something went wrong. Unable to parse data!",
                "error": str(err)
            })
        }
