# KeySoParser
Simple python app to autommaticly parse offers from keys.so and upload them to google sheets.

# Installation
1. Install [venv](https://docs.python.org/3/library/venv.html)
2. Clone this repository
3. Create venv using ```python -m venv venv``` and activate by typing ```source venv/bin/activate```
4. After installation run ```python -m pip install -r requirements.txt``` to install all project dependencies to virtual environment
5. To config database specify your database config in FormParsing/settings.py and run ```python manage.py makemigrations``` and ```python manage.py migrate```
6. Execute ```cp .env.example .env``` and fill environmental variables.

# Usage
- Run ```python manage.py parse_keys_so --help``` to get info about parsing script args
- Run ```python manage.py run_cron_jobs``` to execute all cron jobs
- Run ```python manage.py update_parse_jobs --help``` to get info about jobs updation/creation