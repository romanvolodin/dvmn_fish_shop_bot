import os
from urllib.parse import urlparse, unquote

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
        f'{API_BASE_URL}/pcm/products',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response.raise_for_status()
    return response.json()['data']


def fetch_product(product_id, access_token):
    response = requests.get(
        f'{API_BASE_URL}/pcm/products/{product_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response.raise_for_status()
    return response.json()['data']


def fetch_price_book_prices(price_book_id, access_token):
    response = requests.get(
        f'{API_BASE_URL}/pcm/pricebooks/{price_book_id}/prices/',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response.raise_for_status()
    return response.json()['data']


def fetch_product_price(price_book_id, product_sku, access_token):
    prices = fetch_price_book_prices(price_book_id, access_token)
    price_id = None
    for price in prices:
        if price['attributes']['sku'] == product_sku:
            price_id = price['id']

    if price_id is None:
        return

    response = requests.get(
        f'{API_BASE_URL}/pcm/pricebooks/{price_book_id}/prices/{price_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response.raise_for_status()
    return response.json()['data']


def fetch_product_stock(product_id, access_token):
    response = requests.get(
        f'{API_BASE_URL}/v2/inventories/{product_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response.raise_for_status()
    return response.json()['data']


def download_product_image(image_id, access_token):
    response = requests.get(
        f'{API_BASE_URL}/v2/files/{image_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response.raise_for_status()
    decoded_response = response.json()['data']
    image_url = decoded_response['link']['href']
    image_name = decoded_response['file_name']
    image_path = os.path.join('tmp', image_name)

    response = requests.get(image_url)
    response.raise_for_status()
    with open(image_path, 'wb') as file:
        file.write(response.content)
    return image_path


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
