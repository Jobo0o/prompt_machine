from flask import Blueprint, render_template, request, session
import openai

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the form
    user_message = request.form.get('user_message')

    # Check if the session variables exist before trying to access them
    display_conversation = session.get('display_conversation', [])
    generated_prompt = session.get('generated_prompt', '')
    
    # The rest of your route code goes here...


    # Store the user's message in the conversation history
    display_conversation.append({"role": "user", "content": user_message})

    # Prepare the conversation for the OpenAI API to generate a response
    conversation = [
        {"role": "system", "content": generated_prompt},
        {"role": "user", "content": user_message}
    ]

    # Send a request to the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # Extract the AI's response from the API response
    api_response = response.choices[0].message["content"]

    # Store the AI's message in the conversation history
    display_conversation.append({"role": "assistant", "content": api_response})

    # Save the conversation history in the session
    session['display_conversation'] = display_conversation

    # Render the home page with the conversation history
    return render_template('home.html', conversation=display_conversation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

