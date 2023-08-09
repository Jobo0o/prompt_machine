from flask import Flask, session
from blueprints.home import home_bp
from blueprints.chat import chat_bp
from blueprints.api_key import api_key_bp
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your secret key'

app.register_blueprint(home_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(api_key_bp)

app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem for storing session data
app.config['SESSION_PERMANENT'] = False  # Whether the session should be permanent (True means cookie will have an expiration date, False means it will expire when browser is closed)
app.config['SESSION_USE_SIGNER'] = True  # Sign the session cookie for added security
app.config['SESSION_KEY_PREFIX'] = 'your_session_prefix:'  # Prefix for storing session data (useful if using a shared storage system)
app.config['SESSION_FILE_DIR'] = 'your_directory_for_storing_sessions'  # Directory where session files will be stored (only relevant for 'filesystem' type)

Session(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)