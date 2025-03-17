import os

from config.logger_config import logger
from pipeline.DataIngestor import DataIngestor
from pipeline.DataTransformer import DataTransformer
from pipeline.PostgresLoader import PostgresLoader


def main():
    file_path = os.path.join('/app', 'resources', 'churn_data.csv')
    db_params = {
        'dbname': 'hgi_db',
        'user': 'hgi_user',
        'password': 'hgi_password',
        'host': 'db',
        'port': 5432
    }

    try:
        logger.info("Starting data pipeline...")
        df = DataIngestor.ingest(file_path)
        logger.info(f"Data ingestion completed. Rows loaded: {len(df)}")

        # Loading raw data into PostgreSQL (L1)
        PostgresLoader.load(df, db_params, 'churn_data_l1')

        # Transforming the data for L2
        transformed_df = DataTransformer.transform(df)

        # Loading transformed data into PostgreSQL (L2)
        PostgresLoader.load(transformed_df, db_params, 'churn_data_l2')

        logger.info("Data pipeline executed successfully!")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

if __name__ == '__main__':
    main()
