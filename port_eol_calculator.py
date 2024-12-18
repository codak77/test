import requests
import json
from typing import Dict, List
from dotenv import load_dotenv
import os

class PortAPIClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get_access_token(self) -> str:
        """Fetch access token using client credentials"""
        auth_url = f"{self.base_url}/v1/auth/access_token"
        payload = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }
        
        response = requests.post(auth_url, json=payload)
        response.raise_for_status()
        
        self.token = response.json()['accessToken']
        self.headers['Authorization'] = f'Bearer {self.token}'
        return self.token

    def _ensure_valid_token(self):
        """Ensure we have a valid token before making requests"""
        if not self.token:
            self.get_access_token()

    def get_services(self) -> List[Dict]:
        """Fetch all service entities from Port"""
        self._ensure_valid_token()
        response = requests.get(
            f'{self.base_url}/v1/blueprints/service/entities',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()['entities']

    def get_frameworks(self) -> List[Dict]:
        """Fetch all framework entities from Port"""
        self._ensure_valid_token()
        response = requests.get(
            f'{self.base_url}/v1/blueprints/framework/entities',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()['entities']

    def update_service_eol_count(self, service_id: str, eol_count: int):
        """Update the EOL package count for a service"""
        self._ensure_valid_token()
        payload = {
            "properties": {
                "number_of_eol_packages": eol_count
            }
        }
        response = requests.patch(
            f'{self.base_url}/v1/blueprints/service/entities/{service_id}',
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

def calculate_eol_packages():
    # Initialize Port API client
    load_dotenv()

    PORT_API_URL = "https://api.getport.io"
    PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
    PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")

    client = PortAPIClient(PORT_API_URL, PORT_CLIENT_ID, PORT_CLIENT_SECRET) 

    try:
        # Get all services and frameworks
        services = client.get_services()
        frameworks = client.get_frameworks()

        # Create a lookup dictionary for frameworks
        framework_state_map = {
            framework['identifier']: framework['properties']['state']
            for framework in frameworks
        }

        # Process each service
        for service in services:
            # Get the frameworks related to this service
            service_frameworks = service['relations']['used_frameworks']
            
            # Count EOL frameworks
            eol_count = sum(
                1 for framework_id in service_frameworks
                if framework_state_map.get(framework_id) == 'EOL'
            )

            # Update the service with the EOL count
            print(f"Updating service {service['identifier']} with EOL count: {eol_count}")
            client.update_service_eol_count(service['identifier'], eol_count)

        print("Successfully updated all services with EOL package counts")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while communicating with Port API: {str(e)}")
    except KeyError as e:
        print(f"Error accessing data structure: {str(e)}")
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    calculate_eol_packages()