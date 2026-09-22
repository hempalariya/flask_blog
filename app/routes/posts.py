from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Post, User

posts_bp = Blueprint("posts", __name__, url_prefix="/api/posts")

# 1. get all posts: get /api/posts
@posts_bp.route("", methods=["GET"])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all() # Post.query.all() generates: SELECT *  FROM posts ORDER BY created_at DESC
    return jsonify([post.to_dict() for post in posts]), 200

# 2. get single post: get /api/posts/<id>
@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get(post_id) #returns None if no record matches 
    if not post:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404
    return jsonify(post.to_dict()), 200

# 3. create post: POST /api/posts
@posts_bp.route("", methods=['POST'])
def create_post():
    data = request.get_json()

    #basic payload validation
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Fields 'title' and 'content' are required." })

    author_id = data.get("author_id", 1)

    #Ensure author exists in DB
    user = User.query.get(author_id)

    if not user:
        return jsonify({"error": f"User with id {author_id} does not exist"})


    new_post = Post(
        title=data["title"],
        content=data["content"],
        user_id=author_id
    )

    try:
        db.session.add(new_post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create post", "details": str(e)}), 500
    return jsonify(new_post.to_dict()), 201

# 4. update post: PUT /api/posts/<id>
@posts_bp.route("<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update post", "details": str(e)}), 500

    return jsonify(post.to_dict()), 200

# 5. DELETE post: DELETE /api/posts/<id>
@posts_bp.route("<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": f"Post with id {post_id} not found"}), 400

    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete post", "details": str(e)}), 500
    return jsonify({"message": f"Post {post_id} has been deleted successfully"}), 200