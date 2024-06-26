import json
import subprocess

# Define the JSON data
json_data = '''
{
  "id": "Daily Builds",
  "description": "Workflow that runs to build Apple A application",
  "owner": "A",
  "Tasks":[
      {
        "id": "1",
        "type": "input",
        "data": { "name": "Nightly Build", "source":"http://github.com/repo", "compute":"AWS","cmd":["echo 'test'","echo 'script 2'"], "output":"http://github.com/repo1","report":"email" },
        "Position": { "x": 0, "y": 50 }        
      },
      {
        "id": "2",
        "type": "middle", 
        "data": { "name": "Run Unit Test", "source":"http://github.com/repo", "compute":"AWS","cmd":["echo 'test'","echo 'script 2'"], "output":"http://github.com/repo1","report":"email" },       
        "position": { "x": 300, "y": 50 }
      },
      {
        "id": "3",
        "type": "output",
        "data": { "name": "CoRelation" ,"source":"http://github.com/repo", "compute":"AWS","cmd":["echo 'test'","echo 'script 2'"], "output":"http://github.com/repo1","report":"email" },
        "position": { "x": 650, "y": 25 }        
      },
      {
        "id": "4",
        "type": "output",
        "data": { "name": "Performace" ,"source":"http://github.com/repo", "compute":"AWS","cmd":["echo 'test'","echo 'script 2'"], "output":"http://github.com/repo1","report":"email" },
        "position": { "x": 650, "y": 100 }
        
      }
  ],
  "Edges":[
      {
        "id": "e1-2",
        "source": "1",
        "target": "2",  
        "Pre-condition": ["success"]      
      },
      {
        "id": "e2a-3",
        "source": "2",
        "target": "3",       
        "Pre-condition": ["success","Fail"] 
      },
      {
        "id": "e2b-4",
        "source": "2",
        "target": "4",
        "Pre-condition": ["Fail"] 
      }
  ]
}
'''

# Parse the JSON data
workflow = json.loads(json_data)

# Function to execute a list of commands
def execute_commands(commands):
    for cmd in commands:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            return False
    return True

# Dictionary to store the status of each task
task_status = {}

# Execute tasks based on their dependencies
for task in workflow["Tasks"]:
    task_id = task["id"]
    commands = task["data"]["cmd"]

    if task_id == "1":
        success = execute_commands(commands)
        task_status[task_id] = "success" if success else "fail"
    
    elif task_id == "2":
        if task_status["1"] == "success":
            success = execute_commands(commands)
            task_status[task_id] = "success" if success else "fail"
    
    elif task_id in ["3", "4"]:
        if task_status["2"] in ["success", "fail"]:
            success = execute_commands(commands)
            task_status[task_id] = "success" if success else "fail"

print("Task Execution Status:")
print(task_status)


--------------------------------------------------------------------

{
    "db_name": "your_db_name",
    "db_user": "your_db_user",
    "db_password": "your_db_password",
    "db_host": "your_db_host",
    "db_port": "your_db_port"
}


import json
import psycopg2
from flask import Flask, request

app = Flask(__name__)

# Function to read the database configuration from a file
def get_db_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

# Function to store task data in the database
def store_task_in_db(db_config, data):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_config['db_name'],
            user=db_config['db_user'],
            password=db_config['db_password'],
            host=db_config['db_host'],
            port=db_config['db_port']
        )
        cursor = conn.cursor()

        # Insert data into the task_details table
        cursor.execute(
            """
            INSERT INTO task_details (name, compute, src, cmd1, cmd2, output, report)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (data['name'], data['compute'], data['src'], data['cmd1'], data['cmd2'], data['output'], data['report'])
        )

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return "Task created successfully"
    except Exception as e:
        return f"An error occurred: {e}"

# Read database connection details from config file
db_config = get_db_config('/path/to/config.json')

@app.route('/task/create', methods=['POST'])
def create_task():
    # Parse JSON request data
    request_data = request.get_json()
    name = request_data.get("name")
    compute = request_data.get("compute")
    src = request_data.get("src")
    cmd1 = request_data.get("cmd1")
    cmd2 = request_data.get("cmd2")
    output = request_data.get("output")
    report = request_data.get("report")

    # Create data dictionary
    data = {
        'name': name,
        'compute': compute,
        'src': src,
        'cmd1': cmd1,
        'cmd2': cmd2,
        'output': output,
        'report': report
    }

    # Store task in the database
    result = store_task_in_db(db_config, data)

    return result

if __name__ == "__main__":
    app.run(debug=True)


-_------------------------------

CREATE TABLE task_details (
    id SERIAL PRIMARY KEY,
    task_details JSONB
);


-------------------------------

@app.route('/task/create', methods=['GET', 'POST'])
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
    with open("/home/nexgencld02/Hari/My_Python_Repo-main/config.json", "w+") as outfile:
        json.dump(data, outfile)
    return "created"


{"name":"",
"compute":"",
"src":"github",
"cmd1": 1,
"cmd2": 2,
"output":"",
"report":"" 
}


code to rite the data to db 
-----------------------------

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    compute = db.Column(db.String(50), nullable=False)
    src = db.Column(db.String(200), nullable=False)
    cmd1 = db.Column(db.String(200), nullable=False)
    cmd2 = db.Column(db.String(200), nullable=False)
    output = db.Column(db.String(200), nullable=False)
    report = db.Column(db.String(200), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/task/create', methods=['POST'])
def create_task():
    # Extract the data from the request
    name = request.json["name"]
    compute = request.json["compute"]
    src = request.json["src"]
    cmd1 = request.json["cmd1"]
    cmd2 = request.json["cmd2"]
    output = request.json["output"]
    report = request.json["report"]
    
    # Create a new Task instance
    task = Task(
        name=name,
        compute=compute,
        src=src,
        cmd1=cmd1,
        cmd2=cmd2,
        output=output,
        report=report
    )
    
    # Add the Task instance to the session and commit it to the database
    db.session.add(task)
    db.session.commit()
    
    return jsonify({"message": "Task created successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)




--------------------------------------
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
