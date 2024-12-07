This is a site where you can share pictures and drive a car)

# Dev

```bash
git clone https://github.com/darksquare1/vcars.git
cd vcars
```
Create .env file which looks like:
```
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings
SECRET_KEY='change me'
DJANGO_ALLOWED_HOSTS=127.0.0.1
CSRF_TRUSTED_ORIGINS=http://127.0.0.1
CACHES_BACKEND=django.core.cache.backends.memcached.PyMemcacheCache
CACHES_LOCATION=memcached:11211
INTERNAL_IPS=127.0.0.1

EMAIL_HOST_PASSWORD=change me
DEFAULT_FROM_EMAIL=change me
EMAIL_HOST=change me
EMAIL_HOST_USER=change me

REDIS_CONFIG_HOSTS=redis://127.0.0.1:6379

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=change me
SQL_USER=change me
SQL_PASSWORD=change me
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```
Run following commands:
```bash
docker compose -f docker-compose.yml build  
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml exec web python manage.py migrate
```
You can run tests by running the following command:
```bash
docker compose -f docker-compose.yml exec web pytest
```
The site is available at http://127.0.0.1:8000/
# Prod

```bash
git clone https://github.com/darksquare1/vcars.git
cd vcars
```
Create .env.prod file which looks like:
```
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings
SECRET_KEY='changeme'
DJANGO_ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=http://127.0.0.1
CACHES_BACKEND=django.core.cache.backends.memcached.PyMemcacheCache
CACHES_LOCATION=memcached:11211
INTERNAL_IPS=127.0.0.1

EMAIL_HOST_PASSWORD=changeme
DEFAULT_FROM_EMAIL=changeme
EMAIL_HOST=changeme
EMAIL_HOST_USER=changeme

REDIS_CONFIG_HOSTS =redis://redis:6379

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=changeme
SQL_USER=changeme
SQL_PASSWORD=changeme
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```
Run following commands:
```bash
docker compose -f docker-compose.prod.yml build  
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```
You can run tests by running the following command:
```bash
docker compose -f docker-compose.prod.yml exec web pytest
```
The site is available at http://127.0.0.1:80/
