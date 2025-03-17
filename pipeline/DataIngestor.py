import os
import pandas as pd
from config.logger_config import logger


#Ingests file in pandas dataframe
class DataIngestor:
    @staticmethod
    def ingest(file_path: str) -> pd.DataFrame:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        logger.info(f"Ingesting data from file: {file_path}")
        return pd.read_csv(file_path)
