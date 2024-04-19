# Payroll System
This project involves creating a system to calculate the daily and weekly salaries of couriers based on various income factors such as trip earnings, income increases, and income deductions. The system will include models for income items, daily courier salaries, and weekly courier salaries. It will utilize Django Rest Framework (DRF) to implement the necessary endpoints and SQLite for database management. The architecture will be designed to ensure data consistency and rollback operations in case of calculation issues.

## Installation
 Run the following command in the root of your project directory to build and run the Docker containers:
 
```
docker-compose up
```

This command will build the images for your Django application and PostgreSQL database, create containers, and start the services. Your Django application will be accessible at 0.0.0.0:8080.



##  Software Requirements Specification Overview
- User Registration and Authentication
- Calculate Daily Income Based on Courier Rides
- Calculate Weekly Income via Daily Income
- Provide Rolbacks

### Authentication
In the platform, Authentication is developed using the Djoser library and Simple JWT utilizes Django's pre-built User model.

By integrating Djoser with Simple JWT, authentication in the web platform utilizes Djoser's built-in functionalities for user registration and login while also leveraging Simple JWT's capabilities for token-based authentication. This combination enables secure authentication mechanisms for RESTful APIs, ensuring that users can authenticate and access the platform's resources using JWTs.

### Payroll App

1. RideIncome model:
Represents income related to courier rides.
Includes fields for the courier (linked to a User model), income amount, income type (income, deficit, increment), and date.
Utilizes choices for income types in order to reduce complexity of different incomes.

3. PeriodicIncome model:
An abstract model serving as the base for DailyIncome and WeeklyIncome models.
Contains fields for the courier (linked to a User model) and income amount.

4. DailyIncome model:
Includes a unique date field for each daily income entry.

5. WeeklyIncome model:
Contains fields for start and end dates of the week.
Uses unique_together constraint to ensure only one weekly income entry per courier per week

### Daily Income Data Consistancy
To maintain data consistency for daily income, the serializers utilize an atomic transaction to update the daily income immediately after creating a ride income entry. This ensures that the daily income reflects the latest ride income transactions accurately. By integrating the daily income update within the ride income creation process, the system guarantees data integrity and alignment between the two income records. This proactive approach minimizes the risk of data discrepancies and ensures that the daily income data remains current and reliable.

### Weekly Income Automatic And Periodic Calcualation
 The Celery beat task, calculate_weekly_incomes, efficiently calculates each courier's weekly income automatically every Friday night. Here's how it optimally works:

- Efficient Querying: The task fetches the closest specific date and aggregates the weekly income for each courier within a specific date range in a single query using Django's ORM features. This approach minimizes the number of database queries required to calculate the weekly incomes.

- Bulk Creation: It creates a list of WeeklyIncomes objects based on the aggregated data and uses the bulk_create method to insert these records into the database in a single transaction. This bulk creation operation enhances performance by reducing the overhead associated with individual database inserts.

- Automated Execution: By scheduling the task to run every Friday night using Celery beat, the process of calculating weekly incomes for couriers is automated and runs at a specified time without manual intervention. This automation ensures that the weekly income calculations are consistently performed on time without the need for manual triggering.

- Data Integrity: The task is wrapped in a transaction.atomic() block to ensure that all database operations related to calculating and updating weekly incomes are atomic. This guarantees data integrity by either committing all changes in the transaction at once or rolling back the entire transaction if an error occurs, maintaining the consistency of the data.

Overall, this Celery beat task efficiently calculates each courier's weekly income by optimizing database queries, automating the process, and ensuring data integrity through atomic transactions.
