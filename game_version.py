import requests
import src.config as config

def check_game_version():
    """
    Checks the current game version against the server's required version.
    Updates the local configuration if a new version is required.

    Returns:
        bool: True if the current version is up-to-date, False if not.
    """
    headers = {
        'Host': config.get_api_host(),
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': config.get_user_agent(),
        'Authorization': 'Basic c2FrdXJhOjBubHkwbmU=',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close'
    }
    url = f"{config.get_api_url()}/client_requirements/need_update?locale=en"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        server_version = response.json().get('now_version')
        current_version = '13.0.0'  # This should be centrally managed if it changes frequently.
        if server_version and server_version != current_version:
            print(f"Update needed. Server version: {server_version}, Current version: {current_version}")
            return False
        else:
            print("Current game version is up-to-date.")
            return True
    else:
        print("Failed to retrieve game version information.")
        return False

# Example usage
if __name__ == "__main__":
    if check_game_version():
        print("Proceed with game operations...")
    else:
        print("Please update the game version or check your connection.")
