from flask import Blueprint, render_template, request, session, redirect, url_for, logging
import openai
import os

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/home', methods=['Get', 'POST'])
def home():
    # Check if the API key is set
    if not session.get('openai_api_key'):
        return redirect(url_for('api_key_bp.set_api_key'))

    # Initialize the variables
    title = instruction = examples = target_task = output_format = api_response = generated_prompt = None
    display_conversation = session.get('display_conversation', [])
    session.modified = True

    # Get the OpenAI API key from the environment variables
    openai.api_key = session.get('openai_api_key')

    # If the request method is 'POST', the form has been submitted
    if request.method == 'POST':
        # Check if the 'Submit' button was clicked
        if 'submit_prompt' in request.form:
            # Get the form data
            title = request.form.get('title')
            instruction = request.form.get('instruction')
            examples = request.form.get('examples')
            target_task = request.form.get('target_task')
            output_format = request.form.get('output_format')

            # Store the user's message in the display conversation history
            display_conversation.append({"role": "user",
                                         "content": f"Title: {title}\nInstruction: {instruction}\nExamples: {examples}\nTarget Task: {target_task}\nDesired Output Format: {output_format}"})
            session.modified = True

            # Prepare the conversation for the OpenAI API to generate a prompt
            conversation = [
                {"role": "system",
                 "content": "You are a helpful assistant helping me generate better prompts. The following is the "
                            "input I give to you and you give me a prompt out of these information."},
                {"role": "user",
                 "content": f"Title: {title}\nInstruction: {instruction}\nExamples: {examples}\nTarget Task: {target_task}\nDesired Output Format: {output_format}"}
            ]

            # Send a request to the OpenAI API to generate a prompt
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )

            # Extract the generated prompt from the API response
            generated_prompt = response.choices[0].message["content"]

            # Store the AI's message (improved prompt) in the display conversation history but not in the actual
            # conversation sent to OpenAI
            display_conversation.append({"role": "prompt", "content": generated_prompt})
            session.modified = True

            # Update conversation for response
            conversation.append({"role": "system", "content": generated_prompt})
            session.modified = True

            # Send a request to the OpenAI API to generate a response based on the generated prompt
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )

            # Extract the AI's response from the API response
            api_response = response.choices[0].message["content"]

            # Store the AI's message (response) in the conversation history
            display_conversation.append({"role": "assistant", "content": api_response})
            session.modified = True

            # Save the conversation history in the session
            session['display_conversation'] = display_conversation
            session.modified = True

    # Render the home page with the form and the conversation history
    return render_template('home.html', title=title, instruction=instruction, examples=examples,
                           target_task=target_task, output_format=output_format, api_response=api_response,
                           conversation=display_conversation)
