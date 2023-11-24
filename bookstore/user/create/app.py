import ujson

from .utils import db, validator


def lambda_handler(event, context):
    try:
        # Parse the request body
        body = ujson.loads(event['body'])

        # Validate the book data
        book_schema = validator.BooksSchema()
        if book_schema.validate(body):
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Validation Error",
                    "errors": book_schema.validate(body)
                })
            }

        # Connect to the database
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection['dbmodel']
            collection = database['Books']

            # Create a new book entry
            insert_result = collection.insert_one(body)

            return {
                "statusCode": 201,
                "body": ujson.dumps({
                    "message": "Book created successfully",
                    "book_id": str(insert_result.inserted_id)
                })
            }

    except Exception as err:
        return {
            "statusCode": 400,
            "body": ujson.dumps({
                "message": "An error occurred",
                "error": str(err)
            })
        }
