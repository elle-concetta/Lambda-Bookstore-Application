import ujson
from .utils import db, validator


def lambda_handler(event, context):
    try:
        # Extract publisher, discount, and price from the request body
        body = ujson.loads(event['body'])
        publisher = body.get('publisher')
        discount = body.get('discount')
        original_price = body.get('price', 0)

        # Validate input
        result = validator.BooksSchema()
        if not result.validate(body):
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Invalid input",
                    "data": None
                })
            }

        # Convert discount to a float and original_price to float
        try:
            discount = float(discount)
            original_price = float(original_price)
            if not 0 <= discount <= 100:
                raise ValueError
        except ValueError:
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Invalid numerical values"
                })
            }

        # Connect to the database
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection['dbmodel']
            collection = database['Books']

            # Update the price of all books by the specified publisher
            collection.update_many(
                {"publisher": publisher},
                {"$set": {"price": {"$multiply": ["$price", (100 - discount) / 100]}}}
            )

            # Calculate updated price based on the original price and discount
            updated_price = original_price * (100 - discount) / 100

            return {
                "statusCode": 200,
                "body": ujson.dumps({
                    "message": "Prices updated successfully",
                    "updated_price": updated_price
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": ujson.dumps({
                "message": "An error occurred",
                "error": str(e)
            })
        }

