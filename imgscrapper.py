import os
import datetime
import requests
from bs4 import BeautifulSoup

def get_images(page: int, tags: str = None) -> None:
"""Faz o download de imagens de uma URL e as salva localmente."""
url = f'suaurlaqui?page={page}&tags={tags}'
response = requests.get(url)

if response.status_code != 200:
    print(f"Falha ao obter a página {page}: {response.status_code}")
    return

soup = BeautifulSoup(response.content, 'html.parser')
images = soup.find_all('a', class_='directlink largeimg')
session = requests.Session()

for image in images:
    image_url = image['href']
    image_response = session.get(image_url)

    if image_response.status_code != 200:
        print(f"Falha ao baixar a imagem {image_url}: {image_response.status_code}")
        continue

    filename = os.path.basename(image_url)
    file_path = os.path.join('imagens', filename)

    with open(file_path, 'wb') as f:
        f.write(image_response.content)
    print(f"Imagem baixada: {file_path}")
def main():
start = datetime.datetime.now()
tags = input('Tag: ')
first_page = int(input('Primeira página: '))
last_page = int(input('Última página: '))

os.makedirs('imagens', exist_ok=True)

for page in range(first_page, last_page + 1):
    get_images(page, tags)

duration = datetime.datetime.now() - start
print(f'{last_page - first_page + 1} páginas baixadas em {duration}')
if name == 'main':
main()
