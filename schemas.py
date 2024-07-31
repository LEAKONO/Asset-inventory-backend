# schemas.py

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    role = fields.Str()

class AssetSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    category = fields.Str()
    image_url = fields.Str()
    allocated_to = fields.Nested(UserSchema, allow_none=True)  
class RequestSchema(Schema):
    id = fields.Int()
    asset_id = fields.Int()
    user_id = fields.Int()
    reason = fields.Str()
    quantity = fields.Int()
    urgency = fields.Str()
    status = fields.Str()
