import json
from . import config
from . import cryption

def user_login_stamp():
    """Executes user login stamp campaign and updates user nickname."""
    url = f"{config.get_api_url()}/user_login_stamp_campaigns/execute"
    headers = build_headers(session_id=config.USER_INFO['sakura_session'])
    data = '{"_dummy": "1"}'
    
    encoded_data = cryption.encrypt(config.USER_INFO['session_key'], data)
    payload = {
        'encoded': True,
        'data': encoded_data.decode('utf-8')
    }

    response = config.SESSION.post(url, json=payload, headers=headers)
    if response.ok:
        decoded_data = cryption.decrypt(config.USER_INFO['session_key'], response.json()['data'])
        decoded_json = json.loads(decoded_data.value.decode('utf-8'))
        config.USER_INFO['username'] = decoded_json["current_user"]["nickname"]
    else:
        print('Error during user login stamp.')
        response.raise_for_status()

def user_login_bonuses():
    """Retrieves and processes user's total login bonuses."""
    url = f"{config.get_api_url()}/users/total_login_bonus"
    headers = build_headers(session_id=config.USER_INFO['sakura_session'])

    response = config.SESSION.get(url, headers=headers)
    if response.ok:
        # Process the response as needed
        pass
    else:
        print('Error retrieving login bonuses.')
        response.raise_for_status()

def build_headers(session_id=None):
    """Builds headers for the request, including session-specific authentication if provided."""
    headers = {
        'Host': config.get_api_host(),
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': config.get_user_agent(),
        'Authorization': 'Basic c2FrdXJhOjBubHkwbmU=',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    if session_id:
        headers['X-SESSION'] = session_id
    return headers
