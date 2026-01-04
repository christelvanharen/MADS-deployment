import requests
from pathlib import Path
from loguru import logger
import time


def download(url, datafile: Path):
    datadir = datafile.parent
    if not datadir.exists():
        logger.info(f"Creating directory {datadir}")
        datadir.mkdir(parents=True, exist_ok=True)

    if not datafile.exists():
        logger.info(f"Downloading {url} to {datafile}")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with datafile.open("wb") as f:
                f.write(response.content)
            logger.info(f"Successfully downloaded {datafile}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download {url}: {e}")
            raise
    else:
        logger.info(f"File {datafile} already exists, skipping download")


def main():
    """Download the QAnon posts dataset"""
    logger.info("Starting data ingestion...")
    
    url = "https://raw.githubusercontent.com/jkingsman/JSON-QAnon/main/posts.json"
    datadir = Path("/app/data/raw")
    datafile = datadir / Path("posts.json")
    
    download(url, datafile)
    
    logger.info("Data ingestion complete!")


if __name__ == "__main__":
    main()
