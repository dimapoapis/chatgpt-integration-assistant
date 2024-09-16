import requests
import base64
import os  # To access environment variables

# Function to get headers with GITHUB_TOKEN from environment
def get_headers():
    # Use the GITHUB_TOKEN from the environment
    token = os.getenv('GITHUB_TOKEN')  # Fetch GITHUB_TOKEN from environment variables
    headers = {
        'Authorization': f'token {token}',  # Use GITHUB_TOKEN
        'Accept': 'application/vnd.github.v3+json'
    }
    return headers

# Function to trigger GitHub Actions workflow
def trigger_github_workflow():
    """
    Trigger the GitHub Actions workflow to pull the latest API documentation.
    """
    workflow_id = '117668209'  # The workflow ID
    url = f"https://api.github.com/repos/dimapoapis/chatgpt-integration-assistant/actions/workflows/{workflow_id}/dispatches"
    headers = get_headers()
    payload = {"ref": "main"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 204:
            return "GitHub Actions workflow triggered successfully."
        else:
            return f"Failed to trigger workflow: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error triggering workflow: {e}"

# Function to check workflow status
def check_workflow_status():
    """
    Check the status of the GitHub Actions workflow.
    """
    url = "https://api.github.com/repos/dimapoapis/chatgpt-integration-assistant/actions/runs"
    headers = get_headers()

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if data['workflow_runs']:
            latest_run = data['workflow_runs'][0]
            return f"Latest workflow run status: {latest_run['status']}, conclusion: {latest_run['conclusion']}"
        else:
            return "No workflow runs found."
    except requests.exceptions.RequestException as e:
        return f"Error checking workflow status: {e}"

# Function to fetch the latest API documentation from GitHub
def fetch_api_doc():
    """
    Fetch the latest 24SevenOffice API documentation from the GitHub repository.
    """
    url = 'https://api.github.com/repos/dimapoapis/chatgpt-integration-assistant/contents/24SevenOfficeAPI.json'
    headers = get_headers()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.json()

        # Decode the base64 content
        api_doc_content = base64.b64decode(content['content']).decode('utf-8')
        return api_doc_content
    except requests.exceptions.RequestException as e:
        return f"Error fetching the latest API documentation: {e}"

# Orchestrating all steps
def update_and_fetch_api_doc():
    # Step 1: Trigger the workflow
    trigger_response = trigger_github_workflow()
    print(trigger_response)

    # Wait for a few seconds to let the workflow start and complete
    time.sleep(20)  # Adjust this based on your workflow's runtime

    # Step 2: Check the workflow status
    status_response = check_workflow_status()
    print(status_response)

    # Step 3: If workflow completed, fetch the latest API doc
    if 'completed' in status_response:  # Adjust this condition based on actual status response
        api_doc = fetch_api_doc()
        print("Fetched API Documentation:")
        return api_doc
    else:
        return "Workflow is still in progress."

# Execute the function to trigger, monitor, and fetch the latest API documentation
result = update_and_fetch_api_doc()
print(result)

