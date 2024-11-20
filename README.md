## Prerequisites

Before you begin, ensure that you have the following installed on your machine:

- Docker
- Docker Compose

## Project Setup

Follow these steps to set up the project:

### 1. Clone the repository
Run the following commands to clone the repository and navigate into the project directory:

```
git clone <repository-url>
cd <project-directory>
```

### 2. Create the `.env` file

Create a `.env` file in the root of the project directory. This file contains environment variables for configuring the PostgreSQL database connection.

Example `.env` file:

```
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

Make sure to replace the placeholders with your actual database details.

### 3. Set Up the Docker Containers

Build and start the Docker containers using Docker Compose by running:

```
docker-compose up --build
```

This command will:
- Build the images for the Django app and the PostgreSQL database.
- Start the containers and set up the necessary environment variables from the `.env` file.

### 4. Apply Database Migrations

Once the containers are up and running, open a terminal and run the following command to apply migrations and set up the database:

```
docker-compose exec web python manage.py migrate
```

### 5. Running the Application

After migrations are applied, you can start the Django development server by running:

```
docker-compose exec web python manage.py runserver 0.0.0.0:8000
```

The application should now be running at `http://localhost:8000`.

## Docker Commands

- To bring up the containers:
  
  ```
  docker-compose up
  ```

- To stop the containers:
  
  ```
  docker-compose down
  ```

- To rebuild the containers:
  
  ```
  docker-compose up --build
  ```

## File Structure

- `loan/` - Folder for the loan-related components of the app.
- `server/` - Folder for the main server-side components of the app.
- `.env` - File for storing environment variables (make sure to configure it).
- `.gitignore` - Ensures that unnecessary files are not tracked by Git (e.g., `venv/`).
- `Dockerfile` - Contains the instructions to build the Django app's Docker image.
- `docker-compose.yml` - Defines the services (web and db) required to run the app.
- `manage.py` - Django's command-line utility.
- `requirements.txt` - List of Python dependencies for the project.
- `customer_data.xlsx`, `loan_data.xlsx` - Sample data files for the project.

## Notes

- Make sure your `.env` file is not uploaded to the repository for security reasons. It is included in `.gitignore` to avoid tracking.
- Adjust the environment variables in `.env` for your database credentials.

## Troubleshooting

- If you face any issues with the database connection, ensure that the `DATABASE_HOST` in the `.env` file is set to `db` (this is the name of the service defined in `docker-compose.yml`).
- You can check the logs of the containers by running:

  ```
  docker-compose logs
  ```

---

Happy coding!
