# Instructions to Run the Pipeline

1. Ensure the `churn_data.csv` file is placed in the `resources/` folder.
2. Build and run Docker containers:

   ```bash
   docker-compose up --build
   ```
3. Access PostgreSQL database:

   ```bash
   docker exec -it hgi_db psql -U hgi_user -d hgi_db
   ```
4. Verify data in the database:

   ```sql
   SELECT * FROM churn_data LIMIT 5;
   ```
