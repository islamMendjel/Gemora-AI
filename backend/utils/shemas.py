from marshmallow import Schema, fields, validate
# ------------------------------
# 🧩 Signup Schema
# ------------------------------
class SignupSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))


# ------------------------------
# 🧩 Login Schema
# ------------------------------
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
