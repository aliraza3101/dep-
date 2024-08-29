from flask_marshmallow import Marshmallow
from models import User, Post

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post