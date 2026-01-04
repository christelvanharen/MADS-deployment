from pathlib import Path
from loguru import logger
from pandas import json_normalize
import json
from datetime import datetime
import pandas as pd
import re


def bin_time(time):
    """Bin time based on QAnon activity phases"""
    if time < datetime(2017, 12, 1):
        return 0
    elif time < datetime(2018, 1, 1):
        return 1
    elif time < datetime(2018, 8, 10):
        return 2
    elif time < datetime(2019, 8, 1):
        return 3
    else:
        return 4


def remove_url(text):
    """Remove URLs from text"""
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', text)


def preprocess_data():
    """Preprocess the raw QAnon posts data"""
    logger.info("Starting data preprocessing...")
    
    datadir = Path("/app/data/raw")
    datafile = datadir / "posts.json"
    
    if not datafile.exists():
        logger.error(f"Input file {datafile} does not exist. Run ingest first!")
        raise FileNotFoundError(f"Input file {datafile} not found")
    
    logger.info(f"Loading data from {datafile}")
    with datafile.open() as f:
        df = json_normalize(json.load(f)["posts"], sep="_")
    
    logger.info(f"Loaded {len(df)} posts")
    
    # Add time features
    df["time"] = df["post_metadata_time"].apply(pd.to_datetime, unit="s")
    df["bintime"] = df["time"].apply(lambda x: bin_time(x))
    
    # Clean text
    df["text"] = df["text"].apply(lambda x: str(x).replace("\n", " "))
    df["text"] = df["text"].apply(lambda x: remove_url(x))
    df["text"] = df["text"].apply(lambda x: x.lower())
    
    # Filter by text length
    df['size'] = df['text'].apply(lambda x: len(str(x)))
    df = df[df["size"] > 50]
    df.reset_index(inplace=True, drop=True)
    
    logger.info(f"After filtering: {len(df)} posts")
    
    # Save preprocessed data
    processeddir = Path("/app/data/processed")
    if not processeddir.exists():
        logger.info(f"Creating directory {processeddir}")
        processeddir.mkdir(parents=True, exist_ok=True)
    
    outputfile = processeddir / "posts.parquet"
    df.to_parquet(outputfile)
    logger.info(f"Saved preprocessed data to {outputfile}")
    
    logger.info("Data preprocessing complete!")


if __name__ == "__main__":
    preprocess_data()
