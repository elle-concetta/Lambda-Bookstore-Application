from marshmallow import Schema, fields


class BooksSchema(Schema):
    book_id = fields.Int(required=True)
    isbn = fields.Str(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    publisher = fields.Str(required=True)
    year_published = fields.Int(required=True)
    genre = fields.Str(required=True)
    price = fields.Str(required=True)
    description = fields.Str(required=True)
    copies_sold = fields.Int(required=True)
    rating = fields.Str(required=True)

