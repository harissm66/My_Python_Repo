from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Path to save the JSON file
JSON_FILE_PATH = 'employees.json'

def save_to_json(data, path):
    try:
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {path}")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")

@app.route('/create_employee', methods=['POST'])
def create_employee():
    try:
        employee_name = request.json.get('employee_name')
        emp_id = request.json.get('emp_id')
        salary = request.json.get('salary')
        designation = request.json.get('designation')
        joining_date = request.json.get('joining_date')

        if not all([employee_name, emp_id, salary, designation, joining_date]):
            return jsonify({'error': 'Missing data'}), 400

        employee_data = {
            'employee_name': employee_name,
            'emp_id': emp_id,
            'salary': salary,
            'designation': designation,
            'joining_date': joining_date
        }

        # Load existing data
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as json_file:
                employees = json.load(json_file)
        else:
            employees = []

        employees.append(employee_data)
        save_to_json(employees, JSON_FILE_PATH)

        return jsonify({'message': 'Employee added successfully'}), 201
    except Exception as e:
        print(f"Error in /create_employee: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/task/create', methods=['POST'])
def create_task():
    name = request.json["name"]
    compute = request.json["compute"]
    src = request.json["src"]
    cmd1 = request.json["cmd1"]
    cmd2 = request.json["cmd2"]
    output = request.json["output"]
    report = request.json["report"]
    data = {}
    data['name'] = name
    data['compute'] = compute
    data['src'] = src
    data['cmd1'] = cmd1
    data[''] = cmd2
    data[''] = output
    data[''] = report
    with open("Tasks/config.json", "w+") as outfile:
        json.dump(data, outfile)
    return "created"



if __name__ == '__main__':
    app.run(debug=True)






















upload all .sh files
------------------------

import base64
import configparser
import os
import requests

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Extract configuration details
GITHUB_TOKEN = config.get('github', 'token')
REPO_OWNER = config.get('github', 'username')
REPO_NAME = config.get('github', 'repository')
DIRECTORY_PATH = config.get('github', 'directory_path')
COMMIT_MESSAGE = config.get('github', 'commit_message')

# Prepare the request headers
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Content-Type': 'application/json'
}

# Function to upload a file to GitHub
def upload_file(file_path, commit_message):
    # Extract the filename from the local file path
    filename = os.path.basename(file_path)
    
    # GitHub API URL
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filename}'
    
    # Read the file content and encode it to base64
    with open(file_path, 'rb') as file:
        content = file.read()
    
    # Encode the file content to base64
    content_base64 = base64.b64encode(content).decode('utf-8')
    
    # Prepare the request payload
    data = {
        'message': commit_message,
        'content': content_base64
    }
    
    # Make the PUT request to upload the file
    response = requests.put(url, headers=headers, json=data)
    
    # Check the response status
    if response.status_code == 201:
        print(f'File {filename} created successfully.')
    elif response.status_code == 200:
        print(f'File {filename} updated successfully.')
    else:
        print(f'Error uploading {filename}: {response.status_code}')
        print(response.json())

# Iterate over all .sh files in the specified directory and upload them
for root, dirs, files in os.walk(DIRECTORY_PATH):
    for file in files:
        if file.endswith('.sh'):
            file_path = os.path.join(root, file)
            upload_file(file_path, COMMIT_MESSAGE)

-------------------------
import base64
import configparser
import requests

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Extract configuration details
GITHUB_TOKEN = config.get('github', 'token')
REPO_OWNER = config.get('github', 'username')
REPO_NAME = config.get('github', 'repository')
FILE_PATH = config.get('github', 'file_path')
COMMIT_MESSAGE = config.get('github', 'commit_message')

# Extract the filename from the local file path
filename = FILE_PATH.split("\\")[-1]

# GitHub API URL
url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filename}'

# Read the file content and encode it to base64
with open(FILE_PATH, 'rb') as file:
    content = file.read()

# Encode the file content to base64
content_base64 = base64.b64encode(content).decode('utf-8')

# Prepare the request payload
data = {
    'message': COMMIT_MESSAGE,
    'content': content_base64
}

# Prepare the request headers
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Content-Type': 'application/json'
}

# Make the PUT request to upload the file
response = requests.put(url, headers=headers, json=data)

# Check the response status
if response.status_code == 201:
    print('File created successfully.')
elif response.status_code == 200:
    print('File updated successfully.')
else:
    print(f'Error: {response.status_code}')
    print(response.json())

=============================================

config.ini.
-----------
[github]
token = your_github_token
username = your_github_username
repository = your_repository_name
file_path = C:\path\to\your\script.sh
commit_message = Add script.sh
