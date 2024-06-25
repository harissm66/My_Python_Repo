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
