import ujson
from .utils import db


def lambda_handler(event, context):
    try:
        # Load data from the request body
        body = ujson.loads(event['body'])
        publisher = body.get('publisher')
        discount = body.get('discount')

        # Validate and convert discount
        if discount is None or not discount.replace('.', '', 1).isdigit():
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Invalid discount value"
                })
            }
        discount = float(discount)
        if discount < 0 or discount > 100:
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

            # Initialize a counter for updated books
            updated_count = 0

            # Update each book's price
            for book in books:
                if 'price' in book and book['price'].replace('.', '', 1).isdigit():
                    new_price = float(book['price']) * (100 - discount) / 100
                    collection.update_one(
                        {"_id": book['_id']},
                        {"$set": {"price": f"{new_price:.2f}"}}
                    )
                    updated_count += 1

            return {
                "statusCode": 200,
                "body": ujson.dumps({
                    "message": "Prices updated successfully",
                    "updated_count": updated_count
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
