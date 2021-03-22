from requests import get, post, delete, put


print(get('http://localhost:5000/api/users').json())
print(get('http://localhost:5000/api/users/1').json())
print(get('http://localhost:5000/api/users/99999999').json())
print(get('http://localhost:5000/api/users/fhdskj').json())

# нет никаких данных
print(post('http://localhost:5000/api/users').json())

# не все поля
print(post('http://localhost:5000/api/users',
           json={'name': 'Oleg'}).json())

# такой индекс уже есть
print(post('http://localhost:5000/api/users',
           json={'id': 1,
                 'surname': 'Ivanov',
                 'name': 'Ivan', 
                 'age': 23,
                 'position': 'colonist', 
                 'speciality': 'driver', 
                 'address': 'module_5',
                 'email': 'ivan@mail.ru',
                 'password': 'ivan',
                 'city_from': 'Москва'}).json())

print(post('http://localhost:5000/api/users',
           json={'id': 10,
                 'surname': 'Ivanov',
                 'name': 'Ivan', 
                 'age': 23,
                 'position': 'colonist', 
                 'speciality': 'driver', 
                 'address': 'module_5',
                 'email': 'ivan@mail.ru',
                 'password': 'ivan',
                 'city_from': 'Москва'}).json())

print(get('http://localhost:5000/api/users').json())

# не существует работы
print(put('http://localhost:5000/api/users/100',
          json={'address': 'module_10',
                'age': 50}).json())

# нет данных для изменения
print(put('http://localhost:5000/api/users/10').json())

print(put('http://localhost:5000/api/users/10',
          json={'address': 'module_10',
                'age': 50}).json())

print(get('http://localhost:5000/api/users').json())

# работы не существует
print(delete('http://localhost:5000/api/users/999').json())

print(delete('http://localhost:5000/api/users/10').json())

print(get('http://localhost:5000/api/users').json())