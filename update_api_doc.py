import requests
import json
import logging
from datetime import datetime

# Configure logging to store errors in 'error_log.txt'
logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_latest_api_doc():
    url = "https://rest-api.developer.24sevenoffice.com/doc/v1.json"
    try:
        # Fetch the API documentation
        response = requests.get(url)
        response.raise_for_status()
        api_doc = response.json()

        # Save the API documentation to a JSON file
        with open('24SevenOfficeAPI.json', 'w') as f:
            json.dump(api_doc, f, indent=2)

        print('API documentation updated and saved to 24SevenOfficeAPI.json')
        return api_doc

    except requests.exceptions.RequestException as e:
        # Log the error with details
        logging.error(f"Error fetching API documentation: {e}")
        print(f"Error fetching API documentation: {e}")

if __name__ == "__main__":
    fetch_latest_api_doc()
