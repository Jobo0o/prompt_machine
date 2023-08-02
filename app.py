import os
import openai
from flask import Flask, request, render_template_string

# Create a new Flask web application
app = Flask(__name__)

# Define a route for the URL '/'
@app.route('/', methods=['GET', 'POST'])
def home():
    # If the current request is a POST request
    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        instruction = request.form.get('instruction')
        examples = request.form.get('examples')
        target_task = request.form.get('target_task')
        output_format = request.form.get('output_format')

        # Set the OpenAI API key
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Send a request to the ChatGPT model
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": target_task},
            ]
        )
        
        # Return the response from the model
        return f'API response: {response.choices[0].message["content"]}'
    
    # HTML code for the form
    form_html = """
    <form method="POST">
        Title: <input type="text" name="title"><br>
        Instruction: <input type="text" name="instruction"><br>
        Examples:<br>
        <textarea name="examples" rows="10" cols="30"></textarea><br>
        Target Task: <input type="text" name="target_task"><br>
        Desired Output Format: <input type="text" name="output_format"><br>
        <input type="submit" value="Submit">
    </form>
    """

    # Render the form
    return render_template_string(form_html)
