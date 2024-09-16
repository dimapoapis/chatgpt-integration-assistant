import os
import requests
import base64
import time

def trigger_github_workflow():
    """
    Trigger the GitHub Actions workflow to update the API documentation.
    """
    workflow_id = '117668209'  # The workflow ID for the 'update_api_doc.yml' workflow
    url = f"https://api.github.com/repos/dimapoapis/chatgpt-integration-assistant/actions/workflows/{workflow_id}/dispatches"
    
    # Get GITHUB_TOKEN from environment
    github_token = os.getenv('GITHUB_TOKEN')

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    payload = {
        "ref": "main"  # The branch you want to trigger the workflow on
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 204:
            return "GitHub Actions workflow triggered successfully."
        else:
            return f"Failed to trigger workflow: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error triggering workflow: {e}"

def check_workflow_status():
    """
    Check the status of the GitHub Actions workflow.
    """
    url = "https://api.github.com/repos/dimapoapis/chatgpt-integration-assistant/actions/runs"
    
    # Get GITHUB_TOKEN from environment
    github_token = os.getenv('GITHUB_TOKEN')

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if data['workflow_runs']:
            latest_run = data['workflow_runs'][0]
            status = latest_run['status']
            conclusion = latest_run['conclusion']
            return f"Latest workflow run status: {status}, conclusion: {conclusion}"
        else:
            return "No workflow runs found."
    except requests.exceptions.RequestException as e:
        return f"Error checking workflow status: {e}"

def wait_for_workflow_completion():
    """
    Wait for the GitHub Actions workflow to complete.
    """
    while True:
        status = check_workflow_status()
        print(status)
        if "completed" in status:
            print("Workflow completed successfully.")
            break
        else:
            print("Workflow still in progress, waiting for 20 seconds...")
            time.sleep(20)

def fetch_latest_api_doc():
    """
    Fetch the latest 24SevenOffice API documentation from the GitHub repository.
    """
    url = 'https://api.github.com/repos/dimapoapis/chatgpt-integration-assistant/contents/24SevenOfficeAPI.json'
    
    # Get GITHUB_TOKEN from environment
    github_token = os.getenv('GITHUB_TOKEN')

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.json()

        # Decode the base64 content
        api_doc_content = base64.b64decode(content['content']).decode('utf-8')
        return api_doc_content
    except requests.exceptions.RequestException as e:
        return f"Error fetching the latest API documentation: {e}"

# Full flow
trigger_response = trigger_github_workflow()
print(trigger_response)

wait_for_workflow_completion()

api_doc = fetch_latest_api_doc()
print(api_doc)
