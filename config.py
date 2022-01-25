""" 
QueryStatus Tool configuration
"""
from os import path

# QUERY URL
QUERY_URL = "http://storage.googleapis.com/revsreinterview/hosts/host{}/status"

# Number of hosts involved to generate http urls automaticlaly!
HOSTS_COUNT = 1000

# Base directory of project
BASE_DIR = path.abspath(path.dirname(__file__))

# Filepath of asynchronously generated report
REPORT_FILEPATH = f"{BASE_DIR}/QueryStatus/reports/query_status_report.json"

# Headers to be passed to async HTTP client session.
HTTP_HEADERS = {
    "content-type": "text/plain",
    "encoding" : 'utf-8-sig',
}