from requests import get, post, delete, put


print(get('http://localhost:5000/api/v2/jobs').json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs/99999999').json())
print(get('http://localhost:5000/api/v2/jobs/fhdskj').json())

# нет никаких данных
print(post('http://localhost:5000/api/v2/jobs').json())

# не все поля
print(post('http://localhost:5000/api/v2/jobs',
           json={'name': 'Oleg'}).json())

print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'drfgjhk',
                 'team_leader': 1,
                 'work_size': 20,
                 'collaborators': '2, 3',
                 'is_finished': False}).json())

print(get('http://localhost:5000/api/v2/jobs').json())

# не существует работы
print(put('http://localhost:5000/api/v2/jobs/100',
          json={'job': 'drfgjhk',
                'team_leader': 1,
                'work_size': 70,
                'collaborators': '1, 3',
                'is_finished': False}).json())

# нет данных для изменения
print(put('http://localhost:5000/api/v2/users/4').json())

print(put('http://localhost:5000/api/v2/jobs/4',
          json={'job': 'drfgjhk',
                'team_leader': 1,
                'work_size': 70,
                'collaborators': '1, 3',
                'is_finished': False}).json())

print(get('http://localhost:5000/api/v2/jobs').json())

# работы не существует
print(delete('http://localhost:5000/api/v2/jobs/999').json())

print(delete('http://localhost:5000/api/v2/jobs/4').json())

print(get('http://localhost:5000/api/v2/jobs').json())