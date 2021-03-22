from requests import get, post, delete, put


print(get('http://localhost:5000/api/jobs').json())
print(get('http://localhost:5000/api/jobs/1').json())
print(get('http://localhost:5000/api/jobs/99999999').json())
print(get('http://localhost:5000/api/jobs/fhdskj').json())

# нет никаких данных
print(post('http://localhost:5000/api/jobs').json())

# не все поля
print(post('http://localhost:5000/api/jobs',
           json={'title': 'Заголовок'}).json())

# такой индекс уже есть
print(post('http://localhost:5000/api/jobs',
           json={'id': 1,
                 'job': 'drfgjhk',
                 'team_leader': 1,
                 'work_size': 20,
                 'collaborators': '2, 3',
                 'is_finished': False}).json())

print(post('http://localhost:5000/api/jobs',
           json={'id': 10,
                 'job': 'drfgjhk',
                 'team_leader': 1,
                 'work_size': 20,
                 'collaborators': '2, 3',
                 'is_finished': False}).json())

print(get('http://localhost:5000/api/jobs').json())

# не существует работы
print(put('http://localhost:5000/api/jobs/100',
          json={'job': 'worker',
                'work_size': 500}).json())

# нет данных для изменения
print(put('http://localhost:5000/api/jobs/10').json())

print(put('http://localhost:5000/api/jobs/10',
          json={'job': 'work',
                'work_size': 50}).json())

print(get('http://localhost:5000/api/jobs').json())

# работы не существует
print(delete('http://localhost:5000/api/jobs/999').json())

print(delete('http://localhost:5000/api/jobs/10').json())

print(get('http://localhost:5000/api/jobs').json())