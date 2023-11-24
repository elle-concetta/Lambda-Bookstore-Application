import ujson

from .utils import db


def lambda_handler(event, context):
    try:
        # Load data from the request body
        body = ujson.loads(event['body'])
        publisher = body.get('publisher')
        discount = body.get('discount')

        # Convert discount to a numeric type if it's a string
        if isinstance(discount, str):
            try:
                discount = float(discount)
            except ValueError:
                return {
                    "statusCode": 400,
                    "body": ujson.dumps({
                        "message": "Invalid discount value"
                    })
                }

        # Validate input
        if not publisher or not isinstance(discount, (int, float)):
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Invalid publisher or discount"
                })
            }

        if not (0 <= discount <= 100):
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Discount must be between 0 and 100"
                })
            }

        # Connect to the database
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection['dbmodel']
            collection = database['Books']

            # Find books by the publisher
            books = collection.find({"publisher": publisher})

            # Update each book's price
            for book in books:
                if 'price' in book and book['price'].isnumeric():
                    new_price = float(book['price']) * (100 - discount) / 100
                    collection.update_one(
                        {"_id": book['_id']},
                        {"$set": {"price": str(new_price)}}
                    )

            return {
                "statusCode": 200,
                "body": ujson.dumps({
                    "message": "Prices updated successfully"
                    # Additional response details if needed
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
