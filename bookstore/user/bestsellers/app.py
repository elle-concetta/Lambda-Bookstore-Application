import ujson
from .utils import db


def retrieve_top_books():
    # Retrieve top 10 books from database
    result = list()
    mongo = db.MongoDBConnection()

    with mongo:
        database = mongo.connection['dbmodel']
        collection = database['Books']

        # Retrieve top 10 books based on copies sold
        for book in collection.find().sort("copies_sold", -1).limit(10):
            result.append({
                "title": book["title"],
                "copies_sold": book["copies_sold"]
            })

    return result


def lambda_handler(event, context):
    try:
        return {
            "statusCode": 200,
            "body": ujson.dumps({
                "message": "Success",
                "data": retrieve_top_books()
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
