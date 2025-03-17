import pandas as pd
from sqlalchemy import create_engine, Table, Column, String, Integer, Float, MetaData
from sqlalchemy.exc import OperationalError
from config.logger_config import logger

class PostgresLoader:
    @staticmethod
    def load(df: pd.DataFrame, db_params: dict, table_name: str) -> None:
        logger.info(f"Loading data into PostgreSQL table: {table_name}")

        # Create the PostgreSQL connection string and use sqlalchemy to ingest data
        connection_string = f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@" \
                            f"{db_params['host']}:{db_params['port']}/{db_params['dbname']}"

        engine = create_engine(connection_string)
        metadata = MetaData()

        try:
            # Establish a connection to the database
            with engine.connect() as connection:

                # Check if the table exists
                if not engine.dialect.has_table(connection, table_name):
                    logger.info(f"Table {table_name} does not exist. Creating table...")

                    # Table definition
                    table = Table(table_name, metadata,
                                  Column('customer_id', String, primary_key=True),
                                  Column('age', Integer),
                                  Column('gender', String),
                                  Column('tenure', Integer),
                                  Column('monthly_charges', Float),
                                  Column('contract_type', String),
                                  Column('internet_service', String),
                                  Column('total_charges', Float),
                                  Column('tech_support', String),
                                  Column('churn', String)
                                  )
                    # Create the table in the database
                    metadata.create_all(engine)

                #Insert dataframe at once
                df.to_sql(table_name, engine, index=False, if_exists='replace', method='multi')
                logger.info(f"Data successfully loaded into {table_name}.")

        except OperationalError as e:
            logger.error(f"Error during PostgreSQL operation for {table_name}: {e}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")

        finally:
            engine.dispose()
