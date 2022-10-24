import requests
from environs import Env


API_BASE_URL = 'https://api.moltin.com'

def get_access_token(client_id, client_secret):
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }
    response = requests.post(
        f'{API_BASE_URL}/oauth/access_token', data=payload
    )
    response.raise_for_status()
    return response.json()['access_token']


def fetch_products(access_token):
    response = requests.get(
        f'{API_BASE_URL}/v2/products',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response.raise_for_status()
    return response.json()['data']


def fetch_product(product_id, access_token):
    response = requests.get(
        f'{API_BASE_URL}/v2/products/{product_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response.raise_for_status()
    return response.json()['data']


def fetch_cart(access_token, cart_id):
    response = requests.get(
        f'{API_BASE_URL}/v2/carts/{cart_id}/items',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response.raise_for_status()
    return response.json()['data']


def add_product_to_cart(access_token, product_id, cart_id):
    response = requests.post(
        f'{API_BASE_URL}/v2/carts/{cart_id}/items',
        headers={
            'Authorization': f'Bearer {access_token}',
        },
        json={
            'data': {
                'type': 'cart_item',
                'sku': 'shark-123',
                'quantity': 12,
            }
        }
    )
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    access_token = get_access_token(env.str('EP_CLIENT_ID'), env.str('EP_CLIENT_SECRET'))
    print(add_product_to_cart(access_token, None, 'carttt'))
    print(fetch_cart(access_token, 'carttt'))
