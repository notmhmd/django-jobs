import requests
from celery import shared_task
from django.conf import settings
from candidate.models import Candidate


KEYCLOAK_URL = f'{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token'
KEYCLOAK_ADMIN_API = f'{settings.KEYCLOAK_SERVER_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users'



@shared_task
def register_candidate_task(candidate_data):
    token = get_keycloak_admin_token()
    if not token:
        print("Failed to get Keycloak admin token")
        return

    keycloak_user_id = create_keycloak_user(candidate_data, token)
    if keycloak_user_id:
        Candidate.objects.filter(email=candidate_data["email"]).update(auth_id=keycloak_user_id)
        print(f"Candidate {candidate_data['full_name']} linked to Keycloak ID: {keycloak_user_id}")
    else:
        print(f"Failed to create user in Keycloak: {candidate_data['full_name']}")


def get_keycloak_admin_token():
    """Retrieve an admin access token from Keycloak."""
    payload = {
        'grant_type': 'client_credentials',
        'client_id': settings.KEYCLOAK_CLIENT_ID,
        'client_secret': settings.KEYCLOAK_CLIENT_SECRET,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(KEYCLOAK_URL, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Failed to get Keycloak admin token: {response.text}")
        return None


def get_keycloak_user_id(email, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_ADMIN_API}?email={email}", headers=headers)
    if response.status_code == 200:
        users = response.json()
        if users:
            return users[0].get("id")
    return None


def create_keycloak_user(user_data, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    print('Creating keycloak user')
    keycloak_data = {
        'username': user_data['email'],
        'email': user_data.get('email', 'default_email@example.com'),
        'firstName': user_data['full_name'],
        'lastName': '',
        'enabled': True,
        'credentials': [{
            'type': 'password',
            'value': 'your_temp_password',
            'temporary': False
        }],
        'attributes': {
            'dob': str(user_data['date_of_birth']),
            'years_of_experience': user_data['years_of_experience'],
            'department': user_data['department'],
        }
    }
    response = requests.post(KEYCLOAK_ADMIN_API, headers=headers, json=keycloak_data)

    if response.status_code == 201:
        print(f"User {user_data['full_name']} created in Keycloak.")
        # Extract the Keycloak user ID
        user_id = get_keycloak_user_id(user_data["email"], token)
        return user_id
    else:
        print(f"Failed to create user {user_data['full_name']} in Keycloak: {response.text}")
