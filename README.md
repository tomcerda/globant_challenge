# Globant Challenge

This project is a FastAPI-based application designed to ingest, validate, and store employee records coming from two different sources:

- CSV ingestion
- Batch JSON ingestion via REST API

The system applies data normalization, business validations, and rejected-record logging before inserting valid entries into a PostgreSQL database.  
The application is fully containerized using Docker and can run locally or inside an AWS EC2 instance.

---

## Features

### Batch Processing  
Supports up to 1000 employee records per request.  
Each record is validated independently, allowing partial success.

### Data Normalization  
The API normalizes fields such as:

- `datetime` (converted to Python datetime or rejected)
- `department_id` and `job_id` (converted to integers)
- `name` (validated for non-empty values)

### Validation Layer  
Custom validation ensures:

- Referential integrity (department and job must exist)
- Valid datetime format
- Required fields present
- Business rules enforced

Invalid records are logged with detailed error messages.

### PostgreSQL Integration  
Valid records are stored in a PostgreSQL database.  
Rejected records are logged for auditing and troubleshooting.

### Dockerized Deployment  
The API runs inside a Docker container and can be deployed to:

- Local development environments  
- AWS EC2 instances  
- Any Docker-compatible infrastructure  

---

## Tech Stack

- Python 3.11  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Docker & Docker Compose  
- Pydantic  

---

## Project Structure

app/
├── crud/
├── routers/
├── services/
├── config.py
├── database.py
├── main.py
├── models.py
├── schemas.py
Dockerfile
docker-compose.yml
requirements.txt
.env