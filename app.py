from flask import Flask, session
from blueprints.home import home_bp
from blueprints.chat import chat_bp
from blueprints.api_key import api_key_bp

app = Flask(__name__)
app.secret_key = 'your secret key'

app.register_blueprint(home_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(api_key_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)