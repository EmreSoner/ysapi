# YS Order Service API

# Instruction
```
docker-compose build
docker-compose run web python manage.py migrate
```

###  Dummy data(Restaurant, Product, User etc.). The command creates fixture data. 
```
docker-compose run web python manage.py load_fixture
```

## Running Tests 
```
docker-compose run web python manage.py test
```

# Running API and depended services
```
docker-compose up
```

## API Doc
```
http://0.0.0.0:8000/
```
Order data can be created via interact tool in the doc.

## API URL
```
http://0.0.0.0:8000/api/v1/
```

### API Service Usage
Order can be created by using user and restaurant ids from fixture.
```
import coreapi

client = coreapi.Client()
schema = client.get("http://0.0.0.0:8000/")

action = ["orders", "create"]
params = {
    "user": 1,
    "restaurant": 1,
    "orderitem_set": [
	    {"product": 1, "quantity": 3}, 
	    {"product": 2, "quantity": 5}
	]
}

result = client.action(schema, action, params=params)
```
### To process or cancel the order manually;
```
import coreapi

client = coreapi.Client()
schema = client.get("http://0.0.0.0:8000/")

action = ["orders", "process"]
params = {
    "id": 1,
    "status": "COMPLETED|REJECTED",
}
result = client.action(schema, action, params=params)
```
This action normally running from **celery-beat** by using **order process** service per 2 minutes for waiting orders.
It can be reviewed on **ysapi/celery.py** file to configuration.


