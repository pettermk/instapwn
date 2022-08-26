# InstaPWN
A hackable instagram "clone"

# Getting PWNed

Launch a terminal in the root of this folder, then:

Setup virtualenv and install requirements
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create a local sqlite database, apply migrations and run server
```
cd instapwn/
python manage.py migrate
python manage.py runserver
```

Now visit `localhost:8000` and start hacking

To create a superuser do
```
python manage.py createsuperuser
```
and follow the instructions
