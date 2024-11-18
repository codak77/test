# Port EOL Package Calculator

## Overview
The Port EOL Package Calculator is a Python application that interfaces with Port's API to analyze and track End-of-Life (EOL) packages across different services. It automatically calculates the number of EOL frameworks associated with each service and updates this information in Port's service entities.

## Features
- Automated fetching of service and framework data from Port's API
- Calculation of EOL package counts per service
- Bulk updating of service entities with EOL counts
- Error handling and logging
- Type hints for better code maintainability

## Prerequisites
- Python 3.7 or higher
- Access to Port's API
- Valid Port API token
- `requests` library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/port-eol-calculator.git
cd port-eol-calculator
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install requests
```

## Configuration

Before running the application, you need to set up your Port API credentials:

Create a .env file and set: 
1. `PORT_CLIENT_ID` with your actual Port client ID 
2. `PORT_CLIENT_SECRET` with your actual Port client secret 

## Usage

Run the script using Python:
```bash
python port_eol_calculator.py
```

The script will:
1. Connect to Port's API
2. Fetch all service entities
3. Fetch all framework entities
4. Calculate EOL package counts for each service
5. Update the services with their respective EOL counts
6. Display progress information and any errors that occur

## API Structure

### PortAPIClient Class

The main class handling API interactions:

#### Methods:
- `get_services()`: Fetches all service entities
- `get_frameworks()`: Fetches all framework entities
- `update_service_eol_count(service_id, eol_count)`: Updates EOL count for a specific service

### Data Structures

#### Service Entity
```json
{
    "identifier": "string",
    "title": "string",
    "relations": {
        "framework": ["string"]  // Array of framework IDs
    },
    "properties": {
        "eol_package_count": number
    }
}
```

#### Framework Entity
```json
{
    "identifier": "string",
    "title": "string",
    "properties": {
        "state": "string"  // "Active" or "EOL"
    }
}
```

## Error Handling

The application includes comprehensive error handling for:
- API communication errors
- Data structure issues
- Authentication problems
- General runtime errors

All errors are logged to the console with descriptive messages.

## Logging

The application logs:
- Service updates
- Error messages
- Processing status
- Completion confirmation

## Best Practices

When using this application:
1. Regularly verify your API token validity
2. Monitor API rate limits
3. Back up service data before running bulk updates
4. Review logs for any errors or inconsistencies

## Troubleshooting

Common issues and solutions:

1. Authentication Errors
   - Verify API token is correct
   - Check token expiration
   - Ensure proper token permissions

2. Connection Issues
   - Check internet connectivity
   - Verify API endpoint availability
   - Confirm firewall settings

3. Data Update Failures
   - Check service identifiers
   - Verify data format
   - Review API permissions


## Security Considerations
- Store API tokens securely
- Use environment variables for sensitive data
- Regularly rotate API tokens
- Monitor for suspicious activity