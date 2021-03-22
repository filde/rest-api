from requests import get, post, delete, put


print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(get('http://localhost:5000/api/v2/users/99999999').json())
print(get('http://localhost:5000/api/v2/users/fhdskj').json())

# нет никаких данных
print(post('http://localhost:5000/api/v2/users').json())

# не все поля
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Oleg'}).json())

print(post('http://localhost:5000/api/v2/users',
           json={'surname': 'Ivanov',
                 'name': 'Ivan', 
                 'age': 23,
                 'position': 'colonist', 
                 'speciality': 'driver', 
                 'address': 'module_5',
                 'email': 'ivan@mail.ru',
                 'password': 'ivan',
                 'city_from': 'Москва'}).json())

print(get('http://localhost:5000/api/v2/users').json())

# не существует пользователя
print(put('http://localhost:5000/api/v2/users/100',
        json={'surname': 'Ivanov',
                'name': 'Ivan', 
                'age': 50,
                'position': 'colonist', 
                'speciality': 'driver', 
                'address': 'module_10',
                'email': 'ivan@mail.ru',
                'password': 'ivan',
                'city_from': 'Москва'}).json())

# нет данных для изменения
print(put('http://localhost:5000/api/v2/users/7').json())

print(put('http://localhost:5000/api/v2/users/7',
          json={'surname': 'Ivanov',
                 'name': 'Ivan', 
                 'age': 50,
                 'position': 'colonist', 
                 'speciality': 'driver', 
                 'address': 'module_10',
                 'email': 'ivan@mail.ru',
                 'password': 'ivan',
                 'city_from': 'Москва'}).json())

print(get('http://localhost:5000/api/v2/users').json())

# пользователя не существует
print(delete('http://localhost:5000/api/v2/users/999').json())

print(delete('http://localhost:5000/api/v2/users/7').json())

print(get('http://localhost:5000/api/v2/users').json())