from flask import Flask, request, render_template, session
import openai
import os

app = Flask(__name__)
app.secret_key = 'your secret key'  # You should replace 'your secret key' with a random string. This is used for session security.

@app.route('/', methods=['GET', 'POST'])
def home():
    # Initialize the variables
    title = instruction = examples = target_task = output_format = api_response = generated_prompt = None
    conversation = []
    display_conversation = session.get('display_conversation', [])

    # If the request method is 'POST', the form has been submitted
    if request.method == 'POST':
        # Get the form data
        title = request.form.get('title', '')
        instruction = request.form.get('instruction', '')
        examples = request.form.get('examples', '')
        target_task = request.form.get('target_task', '')
        output_format = request.form.get('output_format', '')

        # Get the OpenAI API key from the environment variables
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Store the user's message in the conversation history
        display_conversation.append({"role": "user", "content": f"Title: {title}\nInstruction: {instruction}\nExamples: {examples}\nTarget Task: {target_task}\nDesired Output Format: {output_format}"})

        # Prepare the conversation for the OpenAI API to generate a prompt
        conversation = [
            {"role": "system", "content": "You are a helpful assistant. Use the following details to create an improved prompt."},
            {"role": "user", "content": f"Title: {title}\nInstruction: {instruction}\nExamples: {examples}\nTarget Task: {target_task}\nDesired Output Format: {output_format}"}
        ]

        # Send a request to the OpenAI API to generate a prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Extract the generated prompt from the API response
        generated_prompt = response.choices[0].message["content"]

        # Store the AI's message (improved prompt) in the conversation history
        display_conversation.append({"role": "prompt", "content": generated_prompt})

        # Prepare the conversation for the OpenAI API to generate a response based on the generated prompt
        conversation = [
            {"role": "system", "content": generated_prompt},
        ]

        # Send a request to the OpenAI API to generate a response based on the generated prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Extract the AI's response from the API response
        api_response = response.choices[0].message["content"]

        # Store the AI's message (response) in the conversation history
        display_conversation.append({"role": "assistant", "content": api_response})

        # Save the conversation history in the session
        session['display_conversation'] = display_conversation

    # Render the home page with the form and the conversation history
    return render_template('home.html', title=title, instruction=instruction, examples=examples, target_task=target_task, output_format=output_format, api_response=api_response, conversation=display_conversation)


@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the form
    user_message = request.form.get('user_message')

    # Get the conversation history from the session
    display_conversation = session.get('display_conversation', [])
    generated_prompt = session.get('generated_prompt', '')

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
    app.run(debug=True)
