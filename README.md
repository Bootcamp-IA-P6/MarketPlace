
# Looping MarketPlace
#### Comprehensive step-by-step instructions for installing and running the MarketPlace application.

## Requirements.
- Python 3.12+
- pip
- Docker Desktop
- Git

## Run Locally.
## Quick Start (Docker).

Repository.
[MarketPlace](https://github.com/Bootcamp-IA-P6/MarketPlace)
```bash
git clone https://github.com/Bootcamp-IA-P6/MarketPlace.git
```
```bash
cd Backend
```
```bash
docker compose up --build
```

# Create virtual environment.

### Mac / Linux
``` bash
python3 -m venv venv
```
``` bash
source venv/bin/activate
``` 
### Windows
``` bash
python -m venv venv
```
``` bash
venv\Scripts\activate
``` 
### Install dependencies.
``` bash
pip install -r requirements.txt
``` 
### Apply migrations.
``` bash
python manage.py migrate
``` 
### Run development server.
``` bash
python manage.py runserver
``` 
### Build and start containers.
``` bash
docker compose up --build
``` 
### Run in background.
``` bash
docker compose up -d
``` 
### Stop containers.
``` bash
docker compose down
``` 
