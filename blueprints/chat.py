from flask import Blueprint, render_template, request, session, flash, redirect, url_for, logging
import openai

chat_bp = Blueprint('chat_bp', __name__)


@chat_bp.route('/chat', methods=['POST'])
def chat():
    openai.api_key = session.get('openai_api_key')

    # Get the user's message from the form
    user_message = request.form.get('user_message')

    # Get the display_conversation from session or initialize if not present
    display_conversation = session.get('display_conversation', [])
    session.modified = True

    # Store the user's message in the display conversation
    display_conversation.append({"role": "user", "content": user_message})
    session.modified = True

    # Prepare the conversation for the OpenAI API to generate a response
    api_call_content = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]

    # Send a request to the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=api_call_content
    )

    # Extract the AI's response from the API response
    api_response = response.choices[0].message["content"]

    # Store the AI's message in the display conversation
    display_conversation.append({"role": "assistant", "content": api_response})

    # Save the display conversation back to the session
    session['display_conversation'] = display_conversation
    session.modified = True

    # Redirect to the home page to display the conversation
    return redirect(url_for('home_bp.home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
