import bcrypt
from flask import Blueprint, request, jsonify
from models import db, User, Post
from schemas import UserSchema, PostSchema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)
api = Blueprint('api', __name__)

user_schema = UserSchema()
post_schema = PostSchema()
jwt = JWTManager()

# Register
@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

# Login
@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad credentials"}), 401

# Get All Posts (JWT protected)
@api.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.all()
    return jsonify(post_schema.dump(posts, many=True))

# Create Post (JWT protected)
@api.route('/post', methods=['POST'])
@jwt_required()
def create_post():
    title = request.json.get('title')
    content = request.json.get('content')
    user_id = get_jwt_identity()
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return post_schema.jsonify(post)

# Update Post (JWT protected)
@api.route('/post/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    post = Post.query.get(id)
    if post:
        post.title = request.json.get('title')
        post.content = request.json.get('content')
        db.session.commit()
        return post_schema.jsonify(post)
    return jsonify({"msg": "Post not found"}), 404

# Delete Post (JWT protected)
@api.route('/post/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg": "Post deleted"}), 200
    return jsonify({"msg": "Post not found"}), 404