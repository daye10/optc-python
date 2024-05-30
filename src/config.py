import requests
from . import cryption

# API and Version Information
API_BASE_URL = "https://app.gb.onepiece-tc.jp"
VERSION = 'gb'  # Example versions: 'gb' or 'jp'
SESSION = requests.Session()

# User and Authentication Information
USER_INFO = {
    "uuid": None,
    "adid": None,
    "udid": None,
    "session_key": None,
    "bq159_key": None,
    "sakura_session": None,
    "username": None,
    "platform": "ios"  #  'android' or 'ios'
}

def update_request_headers(session_id=None):
    """Update session headers with default or session-specific authentication."""
    headers = {
        'Host': get_api_host(),
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': get_user_agent(),
        'Authorization': 'Basic c2FrdXJhOjBubHkwbmU=',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    if session_id:
        headers['X-SESSION'] = session_id
    SESSION.headers.update(headers)

def get_api_url():
    """Returns the full API URL based on the version."""
    return API_BASE_URL

def get_api_host():
    """Returns the API host based on the version."""
    return 'app.gb.onepiece-tc.jp' if VERSION == 'gb' else 'app.onepiece-tc.jp'

def get_user_agent():
    """Returns the user agent based on platform and version."""
    platform = 'android' if USER_INFO['platform'] == 'android' else 'ios'
    now_version = '14.0.0'
    return f'sakura/{now_version} ({platform}; 7.1.2; SM-G935F)' if platform == 'android' else f'sakura/{now_version} (iPhone; iOS 15.3.1; iPhone14,5)'
