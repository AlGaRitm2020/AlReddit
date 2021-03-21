from datetime import timedelta

from flask import Flask, request, jsonify
from flask_jwt_simple import JWTManager, jwt_required, get_jwt_identity

from posts.post import Post
from posts.repo import InMemoryPostsRepo
from tools.misc import make_resp, check_keys, create_jwt_generate_response
from users.repo import InMemoryUsersRepo

app = Flask(__name__)
app.user_repo = InMemoryUsersRepo()
app.posts_repo = InMemoryPostsRepo()
app.config["JWT_SECRET_KEY"] = 'super-secret-str'
app.config["JWT_EXPIRES"] = timedelta(hours=24)
app.config["JWT_IDENTITY_CLAIM"] = 'user'
app.config["JWT_HEADER_NAME"] = 'authorization'
app.jwt = JWTManager(app)

app.user_repo.request_create('user', '12345678')


@app.route("/")
def main():
    return app.send_static_file('index.html')


@app.route("/api/register", methods=["POST"])
def user_register():
    in_json = request.json
    if not in_json:
        return make_resp(jsonify({'message': "Empty request"}), 400)
    elif not check_keys(in_json, ('username', "password")):
        return make_resp((jsonify({'message': "Bad request"})), 400)

    created_user = app.user_repo.request_create(**in_json)

    if created_user is None:
        return make_resp(jsonify({'message': 'Duplication user'}), 400)
    return create_jwt_generate_response(created_user)


@app.route("/api/login", methods=["POST"])
def user_login():
    in_json = request.json
    if not in_json:
        return make_resp(jsonify({'message': "Empty request"}), 400)
    elif not check_keys(in_json, ('username', "password")):
        return make_resp((jsonify({'message': "Bad request"})), 400)

    user, error = app.user_repo.authorize(**in_json)

    if user is None:
        return make_resp(jsonify({'message': error}), 400)
    return create_jwt_generate_response(user)


@app.route("/api/posts", methods=["GET"])
def get_all_posts():
    return make_resp(jsonify(app.posts_repo.get_all()), 200)


@app.route('/api/posts', methods=['POST'])
@jwt_required
def add_post():
    in_json = request.json
    if not in_json:
        return make_resp(jsonify({'message': "Empty request"}), 400)
    elif not check_keys(in_json, ('category', "type", 'title')):
        return make_resp((jsonify({'message': "Bad request"})), 400)

    post = Post(**in_json)
    post.author = get_jwt_identity()
    post = app.posts_repo.request_create(post)
    return make_resp(jsonify(post), 200)


if __name__ == '__main__':
    app.run()
