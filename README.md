# Instructions to Run the Pipeline

1. Ensure the `churn_data.csv` file is placed in the `resources/` folder.
2. Build and run Docker containers:

   ```bash
   docker-compose up --build
   ```
3. Execute Pipeline Job:

   ```bash
   docker exec -it hgi_pipeline bash
   crontab -l
   poetry run python /app/pipeline/main.py
   ```
4. Access PostgreSQL database:

   ```bash
   docker exec -it hgi_db psql -U hgi_user -d hgi_db
   ```
5. Verify data in the database:

   ```sql
   select * from churn_data_l1 limit 5;
   select * from churn_data_l2 limit 5;
   ```
