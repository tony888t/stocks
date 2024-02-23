# How to set up and run
Clone repository and then run the following to build and run the container:

1. `docker compose build && docker compose up`.
This will run the migrations, redis, celery worker and celery beat.

2. Open another terminal and run the following command to prepopulate the database with Stocks, Users and Auth Tokens.
`docker-compose exec api poetry run python manage.py populate_db`

3. Log on the **admin** page using the following details:
   1. username - super-user
   2. password - super-secret-password123
4. Navigate to the **Table** and you can get the Token for the **admin-user** & **investor-user**. These tokens will needed when making a request.

# Sending requests
### Stock list
```curl --request GET \
  --url http://127.0.0.1:8000/stocks \
  --header 'Authorization: Token REPLACE_WITH_USER_TOKEN' \
  --header 'Content-Type: application/json'
```
###  Filter stock by name
```
curl --request GET \
  --url 'http://127.0.0.1:8000/stocks/?search=stock1' \
  --header 'Authorization: Token REPLACE_WITH_USER_TOKEN' \
  --header 'Content-Type: application/json'
```

### BUY OR SELL Stock
```
curl --request POST \
  --url http://127.0.0.1:8000/transactions/ \
  --header 'Authorization: Token REPLACE_WITH_USER_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
	"stock": 1,
	"quantity": 100,
	"transaction_type": "Sell"
}'

OR

curl --request POST \
  --url http://127.0.0.1:8000/transactions/ \
  --header 'Authorization: Token REPLACE_WITH_USER_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
	"stock": 1,
	"quantity": 100,
	"transaction_type": "Buy"
}'
```

### View Holding
```
curl --request GET \
  --url http://127.0.0.1:8000/portfolio \
  --header 'Authorization: Token REPLACE_WITH_USER_TOKEN'
```

### Add, Edit, Delete Stock
```
CREATE stock
curl --request POST \
  --url http://127.0.0.1:8000/admin-stocks/1/ \
  --header 'Authorization: Token REPLACE_WITH_USER_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "STOCK NAME",
	"price": 100,
    "currency_code": "GBP"
}'


DELETE stock
curl --request DELETE \
  --url http://127.0.0.1:8000/admin-stocks/1/ \
  --header 'Authorization: Token REPLACE_WITH_USER_TOKEN' \
  --header 'Content-Type: application/json' \

PUT stock
curl --request PUT \
  --url http://127.0.0.1:8000/admin-stocks/1/ \
  --header 'Authorization: Token REPLACE_WITH_USER_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "STOCK NAME",
	"price": 100,
    "currency_code": "GBP"
}'

PATCH stock
curl --request PATCH \
  --url http://127.0.0.1:8000/admin-stocks/1/ \
  --header 'Authorization: Token REPLACE_WITH_USER_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
	"price": 100
}'
```

## Fetch stock price
Task can be found in `stock/tasks.py`. This uses celery & celery-beat. The task is set to run every hour by default this can be changed in `settings.py` - `CELERY_BEAT_SCHEDULE`. 

## Test
To run tests run the following
`docker exec -it <container> poetry run pytest`
