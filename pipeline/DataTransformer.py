import hashlib
import pandas as pd
from config.logger_config import logger


class DataTransformer:
    @staticmethod
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Transforming data for L2")
        #Data Cleaning
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0.0)
        df['TechSupport'].fillna("No", inplace=True)
        df.fillna({"InternetService": "None"}, inplace=True)

        #Anonymize CustomerID(Assuming customer id as PII)
        df['CustomerID'] = df['CustomerID'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
        logger.info("Data transformation completed for L2.")
        return df
