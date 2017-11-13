
from flask_cors import CORS
from flask import Flask, render_template
from flask_sse import sse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(sse, url_prefix='/stream')
app.config["REDIS_URL"] = "redis://localhost"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hello')
def publish_hello():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=28888)
