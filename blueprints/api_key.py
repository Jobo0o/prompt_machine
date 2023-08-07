import openai

from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from openai import OpenAIError

api_key_bp = Blueprint('api_key_bp', __name__)

@api_key_bp.route('/', methods=['GET'])
def index():
    # Check if the API key is set in the session
    if session.get('openai_api_key'):
        return redirect(url_for('home_bp.home'))
    return redirect(url_for('api_key_bp.set_api_key'))

@api_key_bp.route('/set_api_key', methods=['GET', 'POST'])
def set_api_key():
    if request.method == 'POST':
        api_key = request.form.get('api_key')
        
        # Attempt to validate API key with a simple request
        openai.api_key = api_key
        try:
            # Use the key to make a dummy call to OpenAI to validate it
            openai.Completion.create(engine="davinci", prompt="test", max_tokens=5)
        except openai.error.OpenAIError as e:
            # Print out the error message for debugging purposes
            print(str(e))
            flash("The provided API key is invalid.", "danger")
            return render_template('set_api_key.html')

        session['openai_api_key'] = api_key
        flash("API key set successfully!", "success")
        return redirect(url_for('home_bp.home'))

    return render_template('set_api_key.html')
