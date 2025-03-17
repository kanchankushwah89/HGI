import pandas as pd
import psycopg2

from config.logger_config import logger


class PostgresLoader:
    @staticmethod
    def load(df: pd.DataFrame, db_params: dict, table_name: str) -> None:
        logger.info(f"Loading data into PostgreSQL table: {table_name}")
        conn = None
        cursor = None
        try:
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()

            # Ensure the table exists
            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                customer_id TEXT PRIMARY KEY,
                age INT,
                gender TEXT,
                tenure INT,
                monthly_charges FLOAT,
                contract_type TEXT,
                internet_service TEXT,
                total_charges FLOAT,
                tech_support TEXT,
                churn TEXT
            );
            ''')
            conn.commit()

            # Insert data into the table
            insert_query = f'''
            INSERT INTO {table_name} (customer_id, age, gender, tenure, monthly_charges, contract_type, 
                                    internet_service, total_charges, tech_support, churn)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING;
            '''
            for _, row in df.iterrows():
                cursor.execute(insert_query, tuple(row))
            conn.commit()
            logger.info(f"Data successfully loaded into {table_name}.")

        except Exception as e:
            logger.error(f"Error during PostgreSQL operation for {table_name}: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
