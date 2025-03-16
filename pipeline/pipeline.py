import os
import pandas as pd
import hashlib
import psycopg2

def ingest_data(file_path):
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Load dataset
    df = pd.read_csv(file_path)

    # Data Cleaning
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0.0)
    df['TechSupport'].fillna("No", inplace=True)
    df.fillna({"InternetService": "None"}, inplace=True)

    # Anonymize CustomerID
    df['CustomerID'] = df['CustomerID'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())

    return df

def load_to_postgres(df, db_params):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Ensure table exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS churn_data (
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

        # Insert data
        insert_query = '''
        INSERT INTO churn_data (customer_id, age, gender, tenure, monthly_charges, contract_type, 
                               internet_service, total_charges, tech_support, churn)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (customer_id) DO NOTHING;
        '''

        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        conn.commit()

    except Exception as e:
        print(f"Error during PostgreSQL operation: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    # Docker container path
    file_path = os.path.join('/app', 'resources', 'churn_data.csv')

    db_params = {
        'dbname': 'hgi_db',
        'user': 'hgi_user',
        'password': 'hgi_password',
        'host': 'db',  # Service name in docker-compose
        'port': 5432
    }

    try:
        print("Starting data ingestion...")
        df = ingest_data(file_path)
        print("Data ingestion completed. Rows loaded:", len(df))

        print("Loading data to PostgreSQL...")
        load_to_postgres(df, db_params)

        print("Data pipeline executed successfully!")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == '__main__':
    main()