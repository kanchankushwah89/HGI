from typing import Dict

from pipeline.DataIngestor import DataIngestor
from pipeline.DataTransformer import DataTransformer
from pipeline.PostgresLoader import PostgresLoader


class DataPipeline:
    def __init__(self, file_path: str, db_params: Dict[str, str]):
        self.file_path = file_path
        self.db_params = db_params

    def run(self):
        try:
            #Starting data ingestion
            df = DataIngestor.ingest(self.file_path)

            # Loading raw data into PostgreSQL (L1)
            PostgresLoader.load(df, self.db_params, 'churn_data_l1')

            # Transforming the data for L2
            transformed_df = DataTransformer.transform(df)

            # Loading transformed data into PostgreSQL (L2)
            PostgresLoader.load(transformed_df, self.db_params, 'churn_data_l2')
        except Exception as e:
            print(f"Pipeline failed: {e}")