#!/usr/bin/env python3
"""
image_scraper.py

Download de imagens de uma página paginada com tags.
"""

import os
import logging
import argparse
from pathlib import Path
from typing import Optional, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from tqdm import tqdm

# --- Configuração de logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# --- Constantes / Config ---
BASE_URL = os.getenv("IMAGE_SITE_URL", "https://suaurlaqui")
DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "imagens"))
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "5"))

def create_session(retries: int = 3, backoff: float = 0.5) -> requests.Session:
    """Cria uma Session com política de retries."""
    session = requests.Session()
    adapter = HTTPAdapter(
        max_retries=Retry(
            total=retries,
            backoff_factor=backoff,
            status_forcelist=[429, 500, 502, 503, 504]
        )
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

class ImageDownloader:
    def __init__(self, session: requests.Session, download_dir: Path):
        self.session = session
        self.download_dir = download_dir
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def fetch_page(self, page: int, tags: Optional[str]) -> Optional[str]:
        """Obtém o HTML da página; retorna None em caso de erro."""
        url = f"{BASE_URL}?page={page}" + (f"&tags={tags}" if tags else "")
        try:
            resp = self.session.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
            return resp.text
        except requests.HTTPError as e:
            logger.error(f"Página {page} retornou {e.response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Erro ao conectar na página {page}: {e}")
        return None

    def parse_image_urls(self, html: str) -> List[str]:
        """Extrai URLs de todas as imagens na página."""
        soup = BeautifulSoup(html, "html.parser")
        anchors = soup.find_all("a", class_="directlink largeimg")
        return [a["href"] for a in anchors if a.has_attr("href")]

    def download_image(self, url: str) -> None:
        """Faz download de uma única imagem."""
        filename = Path(url).name
        dest = self.download_dir / filename
        if dest.exists():
            logger.debug(f"Já existe: {filename}, pulando.")
            return
        try:
            resp = self.session.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
            dest.write_bytes(resp.content)
            logger.info(f"Baixou: {filename}")
        except requests.RequestException as e:
            logger.warning(f"Falha no download {url}: {e}")

    def run(self, first: int, last: int, tags: Optional[str]) -> None:
        """Itera das páginas `first` a `last` e baixa todas as imagens."""
        for page in tqdm(range(first, last + 1), desc="Páginas"):
            html = self.fetch_page(page, tags)
            if not html:
                continue
            urls = self.parse_image_urls(html)
            for img_url in tqdm(urls, desc=f"Página {page}", leave=False):
                self.download_image(img_url)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Script para download de imagens paginadas."
    )
    parser.add_argument("first", type=int, help="Primeira página")
    parser.add_argument("last", type=int, help="Última página")
    parser.add_argument(
        "--tags", "-t", type=str, default=None,
        help="Tag(s) para filtrar (opcional)"
    )
    parser.add_argument(
        "--out", "-o", type=Path, default=DOWNLOAD_DIR,
        help="Diretório de download"
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    session = create_session()
    downloader = ImageDownloader(session, args.out)
    downloader.run(args.first, args.last, args.tags)

if __name__ == "__main__":
    main()
