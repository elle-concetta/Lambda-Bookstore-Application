import bson
import ujson
from bson import ObjectId

from .utils import db


def lambda_handler(event, context):
    try:
        object_id = event["pathParameters"]["Id"]
    except TypeError:
        object_id = None

    mongo = db.MongoDBConnection()
    with mongo:
        database = mongo.connection['dbmodel']
        collection = database['Books']
        try:
            collection.delete_one({"_id": ObjectId(object_id)})
        except bson.errors.InvalidId:
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Error! Invalid book.",
                    "data": None
                })
            }

        return {
            "statusCode": 204,
            "body": ujson.dumps({
                "message": "Book data deleted!",
                "data": None
            })
        }
