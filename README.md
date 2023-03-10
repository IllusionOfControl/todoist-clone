# Todoist clone  

## Backend

First, run ``PostgreSQL``, set environment variables and create database. For example using ``docker``: ::

```
export POSTGRES_DB=rwdb POSTGRES_PORT=5432 POSTGRES_USER=postgresPOSTGRES_PASSWORD=postgres
docker run --name pgdb --rm -e POSTGRES_USER="$POSTGRES_USER" -ePOSTGRES_PASSWORD="$POSTGRES_PASSWORD" -e POSTGRES_DB="$POSTGRES_DB"postgres
export POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettingsNetworks}}{{.IPAddress}}{{end}}' pgdb)
createdb --host=$POSTGRES_HOST --port=$POSTGRES_PORT--username=$POSTGRES_USER $POSTGRES_DB
```

Then create ``.env`` file (or rename and modify ``.env.example``) in project root and set environment variables for application: ::

```
touch .env
echo APP_ENV=dev
echo DATABASE_URL=postgresql:/$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT$POSTGRES_DB >> .env
echo SECRET_KEY=$(openssl rand -hex 32) >> .env
```

To run the backend for web application in debug use::

```
alembic upgrade head
uvicorn app.main:app --reload
```

## Frontend

First, change directory in the frontend folder and install the dependencies:

```
cd frontend/
npm install
npm start
```
