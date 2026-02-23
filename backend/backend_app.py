from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


def validate_post(post):
    if "title" not in post or "content" not in post:
        return False
    return True


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()

    if not validate_post(new_post):
        return jsonify({"error": "Invalid post"}), 400

    new_id = len(POSTS) + 1
    new_post["id"] = new_id
    POSTS.append(new_post)

    return jsonify({"post": new_post}), 201


def find_post_by_id(id):
    for post in POSTS:
        if post["id"] == id:
            return post
        else:
            return None


@app.route('/api/posts/<post_id>', methods = ['DELETE'])
def delete_post(post_id):
    post_to_be_deleted = find_post_by_id(post_id)
    if post_to_be_deleted:
        POSTS.remove(find_post_by_id(post_id))
        return jsonify({"message": "Post with id <id> has been deleted successfully."}, 200)
    else:
        return jsonify({"message": "Post with id <id> does not exist."}, 400)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
