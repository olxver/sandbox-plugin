# Sandbox - Protected

This directory contains the protected version of the Sandbox plugin. It's designed to allow users to execute Python code on their local system within a secure, isolated environment, similar to the 'Code Interpreter' plugin OpenAI released
a few days ago.

## Description

This version of the Sandbox plugin adds extra security measures on top of the standard version, including containerization, network isolation, and code sanitization.

## Installation

1. Clone this repository
2. Navigate to the `versions/protected/` directory
3. Install [Docker on your system](https://docs.docker.com/engine/install/)
4. Build the Docker image using the provided Dockerfile: `docker build -t sandbox-img-v1 .`
5. Install Python dependencies: `pip install -r requirements.txt`
6. Run the server: `python server.py`

## Usage

1. Head over to [ChatGPT](https://chat.openai.com)
2. Press GPT-4 > Plugins, then scroll down to the Plugin Store
3. At the bottom right should be a 'Develop your own plugin' option. Press it.
4. Enter into the prompt 'localhost:8080'
5. Install it

**To start a new environment, simply say to ChatGPT: 'Start a secure environment'**.
**ChatGPT will then start a new Docker Container. If there are any issues please create a new [issue](https://github.com/olxver/sandbox-plugin/issues)**


## Contributing

Contributions are welcome. Please submit a pull request or open an issue to discuss the changes you wish to make.



