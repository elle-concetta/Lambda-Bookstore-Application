import ujson
from .utils import db
import bson


def retrieve_books_by_rating(rating):
    # Initialize an empty list for the result
    result = []

    # Check if a rating is provided
    if rating is None:
        return {"error": "Rating not provided."}

    # Establish a connection to the MongoDB
    mongo = db.MongoDBConnection()

    with mongo:
        database = mongo.connection['dbmodel']
        collection = database['Books']

        try:
            # Find all books that match the given rating
            books_cursor = collection.find({"rating": rating})

            # Iterate over the cursor and append book details to the result list
            for book in books_cursor:
                result.append({
                    "title": book["title"],
                    "isbn": book.get("isbn"),
                    "rating": book.get("rating"),

                })

            # If no books are found for the given genre, return an error message
            if not result:
                return {"error": "No books found for the given rating."}

        except bson.errors.InvalidId:
            return {"error": "Invalid request format."}

    return result


def lambda_handler(event, context):
    try:
        # Extract the rating from the path parameters
        rating = event.get("pathParameters", {}).get("rating")

        if not rating:
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Rating parameter is missing"
                })
            }

        # Retrieve and return the books of the specified rating
        return {
            "statusCode": 200,
            "body": ujson.dumps({
                "message": "Success",
                "data": retrieve_books_by_rating(rating)
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
