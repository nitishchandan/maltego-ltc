from maltego_trx.entities import Phrase
from maltego_trx.entities import Alias
from maltego_trx.entities import URL
from maltego_trx.entities import Image
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import subprocess

from modules.Helptransform.extensions import Helptransform_registry, Helptransform_set
import requests
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os


def get_favicon_url(soup, base_url):
    icon_link = soup.find('link', rel='icon')
    if icon_link:
        return urljoin(base_url, icon_link['href'])

    apple_icon_link = soup.find('link', rel='apple-touch-icon')
    if apple_icon_link:
        return urljoin(base_url, apple_icon_link['href'])
    return urljoin(base_url, '/favicon.ico')


def find_favicon_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    favicon_url = get_favicon_url(soup, base_url)
    return favicon_url


def calculate_md5_from_url(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        md5_hash = hashlib.md5(response.content).hexdigest()
        return md5_hash
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the image: {e}")
        return None


class getfavicon(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        person_name = request.Value
        favicon_url = find_favicon_url(person_name)
        md5_hash = calculate_md5_from_url(favicon_url)
        ent= response.addEntity("maltego.Image", favicon_url)
        ent.addProperty (fieldName="url", displayName="URL", matchingRule="strict", value=favicon_url)
        ent1 = response.addEntity("maltego.Phrase", md5_hash)

