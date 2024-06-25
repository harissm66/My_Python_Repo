import requests
import subprocess
import os
import shutil
from git import Repo

def call_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        print("API call successful")
        return response.json()
    else:
        print(f"API call failed with status code {response.status_code}")
        return None

def download_from_git(git_url, clone_dir):
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    Repo.clone_from(git_url, clone_dir)
    print(f"Repository cloned to {clone_dir}")

def execute_shell_script(script_path):
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print("Shell script executed successfully")
    else:
        print(f"Shell script execution failed with return code {result.returncode}")
        print(result.stdout)
        print(result.stderr)

if __name__ == "__main__":
    # Sample API URL and Git repository
    api_url = "https://api.example.com/data"
    git_url = "https://github.com/your-repo/example.git"
    clone_dir = "/path/to/clone/dir"
    script_path = "/path/to/your/script.sh"

    # Step 1: Call an API
    api_data = call_api(api_url)
    print(api_data)

    # Step 2: Download from Git
    download_from_git(git_url, clone_dir)

    # Step 3: Execute a shell script
    execute_shell_script(script_path)
