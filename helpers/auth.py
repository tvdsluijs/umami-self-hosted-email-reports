import requests

def authenticate(api_url:str, username:str, password:str):

    if not api_url or not username or not password:
        print("Authentication failed: Missing required parameters.")
        exit(1)

    login_url = f"{api_url}/auth/login"
    payload = {"username": username, "password": password}
    try:
        response = requests.post(login_url, json=payload)
        response.raise_for_status()
        token = response.json().get("token")
        if not token:
            print("Authentication failed: No token received.")
            exit(1)
        return token
    except requests.exceptions.RequestException as e:
        print(f"Failed to authenticate: {e}")
        exit(1)
