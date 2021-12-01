# hipo case app

In the panel, you can create cards, add companies, add employees and give a card to the employees. The first day of each month is card top-up with a celery. Transactions can take place as "purchase" and "top-up".



## Install virtual env

`pip install virtualenv
`
<br> <br>
`virtualenv venv 
`


### Deactivate virtual env:

`deactivate
`

### Activate virtual env:

`
.\venv\Scripts\activate
`
# Install requirements:

`pip install -r requirements.txt
`
# Migrations:

`python manage.py makemigrations
` <br><br>
`python manage.py migrate
`


# Run:

`python manage.py runserver
`
# Crate superuser

`python manage.py createsuperuser`


<hr>




### Install redis:

https://redis.io/download

and run redis-server


### Run celery

`celery -A proj beat -l INFO`






