


# Appointment Booking App

The application is designed for making appointments with professionals for various services (haircuts, medical services, car maintenance, etc.). The application allows to create accounts for clients and organizations/professionals providing services to interact with each other.
The application is based on Onion architecture, Backend application is based on FastAPI. PostgreSQL is used as the main database, interaction with the database is realized on the Repository design pattern. Redis is used as the database for hashing.  API of the application is implemented in REST architectural style with the necessary conventions and full CRUD support, which in turn allows to call the application a RESTful web application. For monitoring and logging of the application there are two options to choose from: Prometheus + Grafana or Sentry. Celery together with Flower is integrated into the application to execute pending jobs. Pytest is used for unit testing and integration testing. Docker is used to automate application deployment. There are two docker-compose scripts options for deploying the application: using gunicorn as a load balancer or using Nginx as a load balancer.

The application implements:
- Onion application architecture;
- DTO according to the Repository pattern;
- Custom user registration, authentication, authorization system;
- Role model of data access;
- Admin panel for data management;
- CRUD operations for all application entities: user, customer, provider, appointment;
- RESTful API;
- Tagging system for services;
- Pending jobs service;
- Unit tests and ingestion tests;
- Monitoring and logging system;
- Two Docker configurations to build and deploy the application (using Gunicorn or Nginx);
- Docker configuration for local Sentry deployment;
- Docker configuration for local Prometheus + Grafana deployment with preconfigured dashboard;


# <a id="monitoring"></a> Content:
 
 - [Definitions](#definitions)
 - [Architecture](#architecture)
 - Registration, authentication, authorization
 - Configuration
 - Tests
 - [Logging and monitoring](#monitoring) 
 -  --[ Prometheus](#prometheus) 
 - --[ Sentry](#sentry)
 - [Environment files (.env)](#envfiles)
 -  [Docker containers](#docker)

# <a id="definitions"></a> Definitions
user - 
customer - 
provider - 
appointment - 

# <a id="architecture"></a> Architecture


<image src="./docs/components_schema.svg">

# <a id="monitoring"></a> Monitoring

Предусмотрено два варианта мониторинга приложения: prometheus или sentry.


## <a id="prometheus"></a> Prometheus


## <a id="sentry"></a> Sentry
To use Sentry as a monitoring service, you need to deploy this service using `docker-compose-sentry.yml`,  all parameters for Sentry configuration are set in [.env.prod](#env-prod). 
The sequence of steps to deploy the Sentry service:
#### 1. Generate secret key
```bash
docker-compose -f docker-compose-sentry.yml run --rm sentry-base config generate-secret-key
```
And then set generated key to `SENTRY_SECRET_KEY` in  [.env.prod](#env-prod).

#### 2. Initialize database

If this is a new database, you'll need to run `upgrade`.

```bash
docker-compose run --rm sentry-base upgrade
```

And **create** an initial user, if you need.


#### 3. Service Start 

```bash
docker-compose up -d
```

And open `http://localhost:9000`



# <a id="envfiles"></a>Environment files (.env)
For convenience .env files are divided into three groups:

 - [.env](#env) - env file for working in development mode.
 - [.env.prod](#env) - env file for working in application deployment mode. 
 - [.env.docker](#env-prod) - env file for configuring docker containers.

.env files that end with example (.env.example) are example files with the necessary parameters to run the application, these files should be converted to the form shown above.

## <a id="env"></a>.env | .env.prod

`MODE` defines the operating mode of the application.
```js
MODE=DEV
```
`MODE` can have the following values:
`DEV` - development mode;
`TEST` - testing mode;
`PROD` - mode for application deployment.

`LOG_LEVEL`sets the logging level in  `logger.py`.
```js
LOG_LEVEL=INFO
```
`LOG_LEVEL` can have the following values:
`DEBUG` - application debugging level;
`INFO` - all errors and warnings.

The following parameters are set to configure the connection to the database:
```js
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=postgres_db
```
`DB_HOST` - the database address;
`DB_PORT` - database access port;
`DB_USER` - database user name;
`DB_NAME` - database name.

The parameters for connecting to the test database are set in the same way:
```js
TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_USER=postgres
TEST_DB_PASS=postgres
TEST_DB_NAME=test_postgres_db
```
The secret key and encryption algorithm for user registration and authorization are set with the following values:
```js
SECRET_KEY=9aUaK88fnrO+8m7ncx2gJhYMhE6iD8umdWEs0TX0mAQ=
ALGORITHM=HS256
```
`SECRET_KEY` - randomly generated key for password encryption;
`ALGORITHM` - password hash calculation algorithm;
The following python code can be used to generate `SECRET_KEY`:
```python
from secrets import token_bytes
from base64 import b64encode
print(b64encode(token_bytes(32)).decode())
```
or in Linux /MacOS use the key generator built into bash:
```bash
openssl rand -base64 32
```

## <a id="env-prod"></a>.env.docker.sentry
The following parameters are set for configuring the database:
```
POSTGRES_DB=sentry_db
POSTGRES_USER=sentry_user
POSTGRES_PASSWORD=sentry_password
```
`POSTGRES_DB` - name of the database to be created;
`POSTGRES_USER` - user of the database to be created;
`POSTGRES_PASSWORD` - password for the database to be created;

Sentry's data encryption uses `SENTRY_SECRET_KEY`.  To generate this key, use the commands described in [sentry configuration section](#sentry).
```
SENTRY_SECRET_KEY==bogvg62jz%ah0nw1w=)cc(bg4fwd!d^6&i*15z534&8c+63n1^
```
The following parameters are used to connect to the Sentry database:
```
SENTRY_POSTGRES_HOST=sentry-postgres
SENTRY_POSTGRES_PORT=5432
SENTRY_DB_NAME=sentry_db
SENTRY_DB_USER=sentry_user
SENTRY_DB_PASSWORD=sentry_password
```
To configure Redis for Sentry, the following parameters are set:
```
SENTRY_REDIS_HOST=sentry-redis
SENTRY_REDIS_PORT=6379
```
`SENTRY_REDIS_HOST` - Redis address for Sentry (in case docker compose is used, this is the service name in the docker compose file);
`SENTRY_REDIS_PORT` - Redis port number for Sentry


# <a id="docker"></a>Docker containers
The following configuration yml files will help in deploying the application:
`docker-compose-gunicorn.yml` - for deploying application with Gunicorn;
`docker-compose-nginx.yml` - for deploying the application with Nginx;
`docker-compose-prometheus.yml` - for deploying application logging and monitoring with Prometheus and Grafana;
`docker-compose-sentry.yml` - for deploying logging and monitoring of the application using local version of Sentry.
The `Dockerfile`, which is located at the root of the project, is used to build applications, along with bash scripts and configuration files from the `docker` directory.

