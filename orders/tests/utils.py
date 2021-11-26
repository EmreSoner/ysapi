from django.contrib.auth.models import User

from products.models import Category, Restaurant, Product


def load_fixture():
    restaurants = [
        {'name': 'Süper Dönerci', 'category': 'Döner/Kebap', 'products': [
            {'name': 'Döner', 'price': '10.00'},
            {'name': 'İskender', 'price': '20.00'},
            {'name': 'Etibol İskender', 'price': '25.95'},
        ]},
        {'name': 'Harika Ev Yemekleri', 'category': 'Ev Yemekleri', 'products': [
            {'name': 'Kuru Fasülye', 'price': '20.10'},
            {'name': 'Pilav', 'price': '18.90'},
            {'name': 'Mercimek Çorbası', 'price': '12.30'},
        ]},
        {'name': 'Bizim Büfe', 'category': 'Fast-Food', 'products': [
            {'name': 'Goralı', 'price': '9.50'},
            {'name': 'Dilli Kaşarlı', 'price': '12.00'},
            {'name': 'Yengen', 'price': '15.00'},
        ]}]


    users = [
        {'first_name': 'Uğur', 'last_name': 'Özi', 'email': 'uozy@yspt.com', 'username': 'uozy@yspt.com'},
        {'first_name': 'Cenk', 'last_name': 'Yaldız', 'email': 'cyaldiz@yspt.com', 'username': 'cyaldiz@yspt.com'},
        {'first_name': 'Selin', 'last_name': 'Simge', 'email': 'ssimge@yspt.com', 'username': 'ssimge@yspt.com'}
    ]

    for restaurant in restaurants:
        category, _ = Category.objects.get_or_create(name=restaurant['category'])
        restaurant_obj, _ = Restaurant.objects.get_or_create(name=restaurant['name'], category=category)

        for product in restaurant['products']:
            Product.objects.get_or_create(name=product['name'], price=product['price'], restaurant=restaurant_obj)

    for user in users:
        User.objects.get_or_create(**user)
