# Prompt Machine

Prompt Machine is a generative AI application built using Flask and the OpenAI GPT-3.5-turbo model. The app is designed to help engineers create more effective prompts for AI models.

## Features

- **Prompt Generator:** Users can input a title, instruction, examples, target task, and desired output format. The app sends this information to the OpenAI API, which generates an improved prompt. The app then sends this improved prompt back to the API to generate a response.
  
- **Chat Feature:** After generating a prompt, users can continue the conversation by sending additional messages, which are also processed by the AI model.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed [Docker](https://www.docker.com/products/docker-desktop) on your machine.
- You have an [OpenAI](https://beta.openai.com/signup/) API key.

## Running the App

To run Prompt Machine, follow these steps:

1. **Pull the Docker image from Docker Hub:**
   
   ```bash
   docker pull joschenk/prompt_machine:latest
   ```

2. **Run the Docker container:**
   
   ```bash
   docker run -p 5000:5000 -e OPENAI_API_KEY=your_openai_api_key joschenk/prompt_machine:latest
   ```
   
   Replace `your_openai_api_key` with your actual OpenAI API key.
   
3. **Access the application:**
   
   Open your web browser and go to `http://localhost:5000`.

## Contributing to Prompt Machine

To contribute to Prompt Machine, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contact

If you want to contact me, you can reach me at `<johannes.schenk2@gmx.de>`.

## License

This project uses the following license: [MIT](<link>).
  
