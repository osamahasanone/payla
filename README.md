# Newsletter

 A django application for managing a newsletter subscriptions.

## Built With

The below languages, libraries and tools have been used:
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Djoser](https://djoser.readthedocs.io/en/latest/getting_started.html)
* [PostgreSQL](https://www.mysql.com/)
* [Pytest](https://docs.pytest.org/en/6.2.x/)
* [Docker](https://www.docker.com/)
* [Swagger](https://swagger.io/)

## Prerequisites

Please make sure that you have Git and Docker installed on you machine.

## Installation

1.  Clone the repo

```sh
git clone https://github.com/osamahasanone/payla
```

2. Build Docker images and start containers in one command:

```sh
docker-compose up -d
```

3. Run tests:

```sh
docker-compose exec web pytest
```

## QA

Make sure to have the containers running in foreground to be able to see the messages in the terminal (emails):

```sh
docker-compose up
```

Please follow the steps below:

1.  Create 4 different users: http://0.0.0.0:8000/auth/users/
2.  Log in using one of these users: http://0.0.0.0:8000/auth/jwt/create
3.  Copy the access token from the response (It will be valid for 24 hours, so no need for the refresh token)
4.  If you want to do the next steps in browser, please add the extension **ModHeader** to Chrome.
5.  Add the header: ```JWT your_access_token```
6.  To start a subscription: http://0.0.0.0:8000/newsletter/subscription/start

    You will see an email containing the confirmation link in the terminal.

    You can also get this link from the response.
7. Click the confirmation link, and you are now a subscriber (check [here](http://0.0.0.0:8000/admin/newsletter/client/)).

8.  To start an unsubscription: http://0.0.0.0:8000/newsletter/unsubscription/start

    You will see an email containing the confirmation link in the terminal.

    You can also get this link from the response.
9. Click the confirmation link, and you are now a normal client.
10. For now we have 4 users. All of them are unsubscribed. Please make ONLY 3 of them subscribers (from the admin site)
11. ```docker-compose down```
12. ```docker-compose up -d```
13. ```docker-compose exec web bash```
14. To test sending the newsletter to subscribers ```python manage.py sendnewsletter```

    Please check the terminal, you will see that the emails were sent only to subscribers.
    You can also see that the emails were sent in two batches: a batch of two emails, another batch of one email (in settings the batch size is 2)
15. You can also specify the batch size: ```python manage.py sendnewsletter -b 1```

    Emails will be sent in 3 batches, each batch contains 1 email.
16. To cleanup subscription and unsubscription outdated attempts: ```python manage.py cleanup```

