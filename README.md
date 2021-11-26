# YS Order Service API

# Kurulum
```
docker-compose build
docker-compose run web python manage.py migrate
```

###  Dummy data(Restaurant, Product, User v.b) yüklemek için alttaki command kullanılabilir.
```
docker-compose run web python manage.py load_fixture
```

## Testleri çalıştırma
```
docker-compose run web python manage.py test
```

# API ve bağımlı servisleri çalıştırma
```
docker-compose up
```

## API Doc
```
http://0.0.0.0:8000/
```
Doc içerisinde bulunan interact tool'u ile de sipariş datası oluşturulabilir.

## API URL
```
http://0.0.0.0:8000/api/v1/
```

### API Service Kullanım
Fixture ile gelen data kullanılarak ürün, kullanıcı ve restoran id'leri kullanılarak sipariş oluşturulabilir. 
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
### Siparişi manuel olarak tamamlamak ya da iptal etmek icin;
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
kullanabilirsiniz. Bu işlem normal olarak **celery-beat ile pub/sub** şeklinde 2 dakikada bir bekleyen siparişler için **order process** servisi kullanılarak yapılmaktadır.
Konfigurasyon için **ysapi/celery.py** dosyasını inceleyebilirsiniz.


