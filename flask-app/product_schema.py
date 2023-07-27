from marshmallow import Schema, fields

class ProductSchema(Schema):
    product_name = fields.Str(required=True)
    product_category = fields.Str(required=True)
    price = fields.Float(required=True)
    available_quantity = fields.Int(required=True)
    description = fields.Str(required=True)
