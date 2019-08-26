# AppStoreConnectClient
A client for the Apple AppStoreConnect API.

This is a work in progress. It currently downloads the Sales Reports for a specific month.

## Required Pre-Requisites
* Python 3
* [PyJWT](https://github.com/jpadilla/pyjwt)
* [requests](https://github.com/psf/requests)

## Installation
1. Install the required pre-requisites.
2. Clone this repository
3. Create `settings.py` with the following contents:
```
#!/usr/bin/python

# DO NOT INCLUDE IN VERSION CONTROL

"""
JWT Authentication

For information about the parameters, visit:
https://developer.apple.com/documentation/appstoreconnectapi/generating_tokens_for_api_requests
"""

# Your private key ID from App Store Connect
KEY_ID = 'YOU KEY ID'

# Your private key, downloaded from App Store Connect
KEY_FILE = 'YOUR KEY FILE'

# Your issuer ID from the API Keys page in App Store Connect
ISSUER_ID = 'YOUR ISSUER ID'

"""
Sales Reports

For information about the parameters, visit:
https://developer.apple.com/documentation/appstoreconnectapi/download_sales_and_trends_reports
"""
VENDOR_NUMBER = 'YOUR VENDOR NUMBER'
MONTH = '2019-05' # Change date as appropriate

"""
Output
"""
REPORT_OUTPUT_FILE = 'report.csv'
```
4. User your own identifiers and in `settings.py`

## Usage
Run:
```
python client.py
```
