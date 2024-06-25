import os
import requests
import subprocess

GITHUB_REPO = "ilove-python/Demo1"
#GITHUB_REPO = "harissm66/My_Python_Repo"
BRANCH = "master"  # Replace with the correct branch name if different
RAW_BASE_URL = "https://raw.githubusercontent.com"
API_BASE_URL = "https://api.github.com/repos"

# Optional: GitHub personal access token for authenticated requests
# TOKEN = "your_github_token"
TOKEN = None

def get_sh_files(repo, branch):
    """Get a list of .sh files in the GitHub repository using GitHub API."""
    url = f"{API_BASE_URL}/{repo}/git/trees/{branch}?recursive=1"
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    sh_files = [file['path'] for file in data['tree'] if file['path'].endswith('.sh')]
    return sh_files

def download_file(url, local_filename):
    """Downloads a file from a URL to a local file."""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def execute_shell_script(script_path):
    """Executes a shell script."""
    #result = subprocess.run(["bash", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE) #capture_output=True, text=True)
    #result=subprocess.Popen("sh "+script_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #result=os.system("sh "+script_path)
    result = subprocess.run(['bash', script_path], stdout=subprocess.PIPE)
    #print(result)
    return result

def main():
    # Get all .sh files in the repository
    sh_files = get_sh_files(GITHUB_REPO, BRANCH)

    for file_path in sh_files:
        print(file_path)
        # Construct the raw URL to download the file
        raw_url = f"{RAW_BASE_URL}/{GITHUB_REPO}/{BRANCH}/{file_path}"

        # Local path to save the downloaded file
        local_script_path = os.path.join(os.getcwd(), os.path.basename(file_path))

        # Download the file
        print(f"Downloading {file_path} from {GITHUB_REPO}...")
        downloaded_script = download_file(raw_url, local_script_path)
        print(f"Downloaded to {downloaded_script}")

        # Execute the downloaded script
        print(f"Executing {downloaded_script}...")
        execution_result = execute_shell_script(downloaded_script)
        #print(execution_result)

        # Print the execution result
        print("Execution Output:")
        print(execution_result.stdout)
        print("Execution Errors:")
        print(execution_result.stderr)

if __name__ == "__main__":
    main()

