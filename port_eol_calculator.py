import requests
import json
from typing import Dict, List
from dotenv import load_dotenv
import os

class PortAPIClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }

    def get_services(self) -> List[Dict]:
        """Fetch all service entities from Port"""
        response = requests.get(
            f'{self.base_url}/v1/blueprints/service/entities',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()['entities']

    def get_frameworks(self) -> List[Dict]:
        """Fetch all framework entities from Port"""
        response = requests.get(
            f'{self.base_url}/v1/blueprints/framework/entities',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()['entities']

    def update_service_eol_count(self, service_id: str, eol_count: int):
        """Update the EOL package count for a service"""
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
    # Replace these with your actual Port API credentials
    load_dotenv()

    PORT_API_URL = "https://api.getport.io"
    PORT_API_TOKEN = os.getenv("PORT_API_KEY")
    
    client = PortAPIClient(PORT_API_URL, PORT_API_TOKEN)

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
            service_frameworks = service.get('relations', {}).get('framework', [])
            
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