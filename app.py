from flask import Flask, request, render_template
import os
import openai

# Initialize a Flask application
app = Flask(__name__)

# Define the route for the application's home page
@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    # Initialize the variables
    title = instruction = examples = target_task = output_format = api_response = None
 
    # Initialize the API response variable
    api_response = None

    # If the request method is 'POST', the form has been submitted
    if request.method == 'POST':
        # Get the form data
        title = request.form.get('title')
        instruction = request.form.get('instruction')
        examples = request.form.get('examples')
        target_task = request.form.get('target_task')
        output_format = request.form.get('output_format')

        # Get the OpenAI API key from the environment variables
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Prepare the conversation for the OpenAI API to generate a prompt
        conversation = [
            {"role": "system", "content": "You are a helpful assistant. Use the following details to create an improved prompt. Only give out the new prompt and nothing else."},
            {"role": "user", "content": f"Title: {title}\nInstruction: {instruction}\nExamples: {examples}\nTarget Task: {target_task}\nDesired Output Format: {output_format}"}
        ]

        # Send a request to the OpenAI API to generate a prompt
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=conversation
        )

        # Extract the generated prompt from the API response
        generated_prompt = response.choices[0].message["content"]

        # Prepare the conversation for the OpenAI API to generate a response based on the generated prompt
        conversation = [
            {"role": "system", "content": generated_prompt},
        ]

        # Send a request to the OpenAI API to generate a response based on the generated prompt
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=conversation
        )

        # Store the API response
        api_response = response.choices[0].message["content"]

    # Render the home page with the form and the API response
    return render_template('home.html', title=title, instruction=instruction, examples=examples, target_task=target_task, output_format=output_format, api_response=api_response)