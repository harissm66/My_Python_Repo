import os
from github import Github
from pathlib import Path

# Replace with your GitHub personal access token
access_token = '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'
# Replace with your GitHub username
username = 'ilove-python'
# Replace with your repository name
repository_name = 'ilove-python/Demo1'
# Replace with the path to your directory containing .sh files
directory_path = '/home/Soumya/python/shellscripts'
# Replace with the commit message
commit_message = 'Add .sh files'

# Authenticate to GitHub
g = Github(access_token)

# Get the repository
repo = g.get_user(username).get_repo(repository_name)

# Iterate over all .sh files in the directory
for root, _, files in os.walk(directory_path):
    for file_name in files:
        if file_name.endswith('.sh'):
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                content = file.read()

            # Create or update the file in the repository
            try:
                contents = repo.get_contents(file_name)
                # If the file exists, update it
                repo.update_file(contents.path, commit_message, content, contents.sha)
                print(f'{file_name} updated successfully.')
            except:
                # If the file does not exist, create it
                repo.create_file(file_name, commit_message, content)
                print(f'{file_name} created successfully.')

