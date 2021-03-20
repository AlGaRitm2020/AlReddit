from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    return app.send_static_file('index.html')

@app.route("/api/register", methods=["POST"])
def user_register():
    pass


if __name__ == '__main__':
    app.run()
