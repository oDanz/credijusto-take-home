# credijusto take home challenge
## How to run it

1. Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on your local host machine.
2. In the project folder, open a terminal and type
    `docker-compose -f docker-compose.prod.yml up --build`
3. Now the web server is ready.

## Endpoints

- [http://localhost:1337/api/](http://localhost:1337/api/) Retrieve exchange rates
- [http://localhost:1337/api/account/register/](http://localhost:1337/api/account/register/) Creates a new user
- [http://localhost:1337/api/token/](http://localhost:1337/api/token/) Retrieves auth token when valid username and password fields are posted to the view
- Examples using curl:

Obtaining authentication token
```
curl -X POST http://localhost:1337/api/token/ -H 'Content-Type: application/json' -d '{"username": "test", "password": "123456"}'
```
Getting exchange rates
```
curl -X GET http://localhost:1337/api/ -H 'Authorization: Token e18dd4c87747f68b3ddcf0561c289bcc9a68480a'
```
Creating a new user
```
curl -X POST http://localhost:1337/api/account/register/ -H 'Content-Type: application/json' -d '{"username": "newuser", "password": "123456"}'
```

## Notes
- Fixer free tier only allows conversions from GPB to MXN.
- The fixer and banxico tokens are not included in the .env file.
