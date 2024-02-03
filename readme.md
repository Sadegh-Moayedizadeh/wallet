# Wallet Service

This is a basic project in which some simple features of a web-based wallet is implemented.
The homepage offers links to the API documentations. It is recommended to try those to
work around with the project.

To start the project follow these steps:

* Run the docker image for redis:
```bash
$ docker run -d --rm -p 6379:6379 redis
```

* Export the PYTHONPATH environment variable:
```bash
$ export PYTHONPATH=wallet
```

* Create the virtual environment:
```bash
$ python -m venv venv
```

* Upgrade pip:
```bash
$ pip install -U pip
```

* Install requirements:
```bash
$ pip install -r requirements.txt
```

* Run the Django project:
```bash
$ python wallet/manage.py runserver
```

* Run the celery application:
```bash
$ celery -A wallet worker -l INFO
```

Now the project should be up and running. To test if it works you can examine the API documentation.
This project, however, needs a bank API to make withdrawal requests to. For the testing purposes, a
simple fixture for that is provided which can be run with the following command:
```bash
$ python tests/fixtures/bank_api.py
```