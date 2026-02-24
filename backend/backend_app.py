from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
            {"id": 1, "title": "First post", "content": "This is the first post."},
            {"id": 2, "title": "Second post", "content": "This is the second post."},
            {"id": 3, "title": "Flask", "content": "This is the Flask Post."},
            {"id": 4, "title": "Python", "content": "This is the Python post."},
            {"id": 5, "title": "Flask API", "content": "This is the Flask API post."},
        ]


SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)



@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Returns all posts if Query parameters
    sor and direction are not provided. Otherwise returns posts
    based on sort and direction"""

    posts = POSTS.copy()
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    if not sort and not direction:
        return jsonify(posts), 200

    if not sort or not direction:
        return jsonify({
            "error": "Both 'sort' and 'direction' must be provided together"}), 400

    posts = sorted(
        posts,
        key=lambda x: x[sort].lower(),
        reverse=(direction == 'desc')
    )

    return jsonify(posts)



@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """This function takes query parameters title
    and content and returns posts where the title or
    content contain the given search items"""

    title = request.args.get('title')
    content = request.args.get('content')

    if not title and not content:
        return jsonify({"error": "No data provided"}), 400

    posts = POSTS.copy()

    posts_searched = [post for post in posts if (title and title.lower() in post["title"].lower()) or
                       (content and content.lower() in post["content"].lower())]

    return jsonify(posts_searched)




def validate_post(post):
    if "title" not in post or "content" not in post:
        return False
    return True


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Create a new post"""

    new_post = request.get_json()

    if not validate_post(new_post):
        return jsonify({"error": "Invalid post"}), 400

    new_id = len(POSTS) + 1
    new_post["id"] = new_id
    POSTS.append(new_post)

    return jsonify({"post": new_post}), 201


def find_post_by_id(id):
    #post = next((p for p in POSTS if p["id"] == id), None)
    for post in POSTS:
        if post["id"] == id:
            return post
    return None


@app.route('/api/posts/<int:post_id>', methods = ['DELETE'])
def delete_post(post_id):
    """Deletes a post by id"""

    post_to_be_deleted = find_post_by_id(post_id)
    if not post_to_be_deleted:
        return jsonify({"message": f"Post with id {post_id} does not exist."}), 400

    POSTS.remove(find_post_by_id(post_id))

    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200



@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Updates a post by id"""

    post = find_post_by_id(post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    updated_post = request.get_json()

    if updated_post is None:
        return jsonify({"error": "No data provided"}), 400

    if "title" in  updated_post and updated_post["title"] is not None:
        post["title"] = updated_post["title"]

    if "content" in  updated_post and updated_post["content"] is not None:
        post["content"] = updated_post["content"]

    return jsonify(post),200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
