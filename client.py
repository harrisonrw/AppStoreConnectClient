#!/usr/bin/python

from datetime import datetime, timedelta
import time
import jwt
import requests
import gzip
from pathlib import Path

from settings import *

TOKEN_REFRESH_INTERVAL = 15 # In minutes
TOKEN_EXPIRATION = 20 # In minutes

ALGORITHM = "ES256"
TOKEN_TYPE = "JWT"
AUDIENCE = "appstoreconnect-v1"

BASE_URL = "https://api.appstoreconnect.apple.com"

class Client:

    def __init__(self, key_id, key_file, issuer_id):
        self.key_id = key_id
        self.key_file = key_file
        self.issuer_id = issuer_id
        self.expiration_time = None
        self.token_date = None
        self._token = None
        
        # Create the first token.
        _ = self.token

    def _create_token(self):
        """
        Returns a new, signed JWT.
        """

        header = {
            "alg": ALGORITHM,
            "kid": self.key_id,
            "typ": TOKEN_TYPE
        }

        self.token_date = datetime.now()
        self.expiration_time = int(time.mktime((self.token_date + timedelta(minutes=TOKEN_EXPIRATION)).timetuple()))

        payload = {
            'iss': self.issuer_id,
            'exp': self.expiration_time,
            'aud': AUDIENCE
        }

        with open(self.key_file, 'r') as fh:
            key = fh.read()

        return jwt.encode(payload, key, algorithm=ALGORITHM, headers=header).decode('ascii')

    @property 
    def token(self):
        """
        Returns a signed JWT. Creates a new token if one does not exist or if the refresh 
        interval has past.
        """
        if not self._token or self.token_date + timedelta(minutes=TOKEN_REFRESH_INTERVAL) > datetime.now():
            self._token = self._create_token()
        
        return self._token

    def download_sales_reports(self, report_date, vendor_number, report_output_file):
        """
        Downloads sales reports.

        Some parameters are currently hard-coded. For more information about the parameters,
        please visit:
        https://developer.apple.com/documentation/appstoreconnectapi/download_sales_and_trends_reports
        """
        url = BASE_URL + '/v1/salesReports?filter[frequency]=MONTHLY&filter[reportDate]=' + report_date + '&filter[reportSubType]=SUMMARY&filter[reportType]=SALES&filter[vendorNumber]=' + vendor_number
        headers = { "Authorization": "Bearer %s" % self.token }

        request = requests.get(url, headers=headers)

        content_type = request.headers['content-type']

        if content_type == "application/a-gzip":
            data = self._get_request_data(request)
            self._write_data_to_file(data, report_output_file)
            
        else:
            print("HTTP Error %d" % request.status_code)

    def _get_request_data(self, request):
        compressed_data = b""
        for block in request.iter_content(1024 * 1024):
            if block:
                compressed_data = compressed_data + block
            
        data = gzip.decompress(compressed_data)

        return data

    def _write_data_to_file(self, data, file_name):
        text = data.decode("utf-8")
        file = Path(file_name)
        file.write_text(text, 'utf-8')


def main():
    client = Client(
        KEY_ID, 
        KEY_FILE, 
        ISSUER_ID
    )
    client.download_sales_reports(
        MONTH, 
        VENDOR_NUMBER,
        REPORT_OUTPUT_FILE
    )


if __name__ == '__main__': main()
