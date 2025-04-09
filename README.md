DarkVision Dashboard API (MVP)

This is a minimal backend MVP built with FastAPI. It authenticates users using JWT and serves dashboard reports by retrieving JSON files from AWS S3.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Boto3 (AWS S3)
- Uvicorn (dev server)
- CORS enabled

## Core Concepts

- Users are stored in a local PostgreSQL database and linked to companies via `company_code`.
- Each company has a dedicated folder in S3 under: `mock_s3_archive/reports/{company_code}/`.
- When a user logs in, their associated `company_code` is extracted from the token.
- Two API endpoints are exposed:
  - `GET /reports` → Lists all reports (JSON filenames) from S3
  - `GET /reports/{filename}` → Returns parsed content of a specific JSON report from S3
- S3 is queried in real-time for each dashboard access (MVP only). Future versions should sync reports to DB periodically and fetch from there.

## Installation

git clone https://github.com/Luis2387/darkvision_fastapi.git

cd darkvision-api

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

Create .env file as follows or use .env_example as guide: 

AWS_ACCESS_KEY_ID=yourkey

AWS_SECRET_ACCESS_KEY=yoursecret

AWS_REGION=us-east-1

JWT_SECRET_KEY=mysecret

## Running the app

uvicorn app.main:app --reload

to see Swagger doc and test api endpoints: http://localhost:8000/docs
