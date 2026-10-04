import requests

BASE_URL = "http://127.0.0.1:8000"


def login(email, password):
    response = requests.post(
        f"{BASE_URL}/api/auth/login", json={"email": email, "password": password}
    )

    return response


def get_dashboard(token):

    response = requests.get(
        f"{BASE_URL}/api/dashboard/", headers={"Authorization": f"Bearer {token}"}
    )

    return response


def get_aircraft(token):

    response = requests.get(
        f"{BASE_URL}/api/aircraft/", headers={"Authorization": f"Bearer {token}"}
    )

    return response


def create_aircraft(token, aircraft):

    response = requests.post(
        f"{BASE_URL}/api/aircraft/",
        headers={"Authorization": f"Bearer {token}"},
        json=aircraft,
    )

    return response


def delete_aircraft(token, aircraft_id):

    response = requests.delete(
        f"{BASE_URL}/api/aircraft/{aircraft_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    return response


def get_flights(token):

    response = requests.get(
        f"{BASE_URL}/api/flights/", headers={"Authorization": f"Bearer {token}"}
    )

    return response


def create_flight(token, flight):

    response = requests.post(
        f"{BASE_URL}/api/flights/",
        headers={"Authorization": f"Bearer {token}"},
        json=flight,
    )

    return response


def delete_flight(token, flight_id):

    response = requests.delete(
        f"{BASE_URL}/api/flights/{flight_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    return response


def export_csv(token):

    response = requests.get(
        f"{BASE_URL}/api/reports/export/csv",
        headers={"Authorization": f"Bearer {token}"},
    )

    return response


def get_statistics(token):

    response = requests.get(
        f"{BASE_URL}/api/reports/statistics",
        headers={"Authorization": f"Bearer {token}"},
    )

    return response


def register(name, email, password):

    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={"name": name, "email": email, "password": password},
    )

    return response


def update_aircraft(token, aircraft_id, aircraft):

    response = requests.put(
        f"{BASE_URL}/api/aircraft/{aircraft_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=aircraft,
    )

    return response
