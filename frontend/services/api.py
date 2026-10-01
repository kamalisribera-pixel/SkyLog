import requests

BASE_URL = "http://127.0.0.1:8000"


def login(email, password):
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    return response

def get_dashboard(token):

    response = requests.get(
        f"{BASE_URL}/api/dashboard/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response