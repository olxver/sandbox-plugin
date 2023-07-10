import quart
import docker
import requests
import tempfile
import tarfile
import subprocess
import quart_cors
import os, time
from quart import request
import ast

def sanitize_code(code):
    unsafe_attributes = ['os', 'subprocess', 'open', 'exec', 'eval', 'input', 'raw_input', 'cryptography']
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr in unsafe_attributes:
                raise ValueError(f"Unsafe attribute {node.attr} is not allowed inside this version of Sandbox due to security reasons")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if alias.name in unsafe_attributes:
                    raise ValueError(f"Importing {alias.name} is not allowed inside this version of Sandbox due to security reasons")
    return code

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
container_id = None

@app.route('/start', methods=['POST'])
async def start():
    global container_id
    client = docker.from_env()
    container = client.containers.run('sandbox-img-v1', detach=True, network_disabled=True)
    container_id = container.id
    return quart.jsonify({'container_id': container_id})

@app.route('/execute', methods=['POST'])
async def execute():
    try:
        data = await request.json
        container_id = data['docker_id']
        code = data['code']
        if container_id is None:
            return quart.jsonify({'error': 'Provide a docker id! If you don\'t have one, start a new environment.'})
        code = (await request.json)['code']
        sanitize_code(code)
        client = docker.from_env()
        container = client.containers.get(container_id)
        with open('temp/code.py', 'w') as f:
            f.write(code)
        with tarfile.open('temp/code.tar', 'w') as tar:
            tar.add('temp/code.py', arcname='code.py')
        container.exec_run('mkdir /code')
        with open('temp/code.tar', 'rb') as f:
            client.api.put_archive(container.id, '/code', f)
        os.remove('temp/code.py')
        os.remove('temp/code.tar')
        exit_code, output = container.exec_run('python /code/code.py')
        return quart.jsonify({'result': output.decode(), 'error': exit_code, 'extra_information_to_assistant': 'make sure to include a print statement or nothing will happen!'})
    except Exception as excep:
        return quart.jsonify({'error_occurred_in_server': str(excep)})

@app.route('/close', methods=['POST'])
async def close():
    data = await request.json
    container_id = data['docker_id']
    if container_id is None:
        return quart.jsonify({'error': 'Provide a docker id! If you don\'t have one, start a new environment.'})
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    return quart.jsonify({'message': f'Container {container_id} stopped.'})

@app.get("/protected-sandbox_security_measures.txt")
async def security_measures():
    filename = "protected-sandbox_security_measures.txt"
    return await quart.send_file(filename, mimetype='text/plain')


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
