import os

page = 'CSS'
t = os.path.exists(f'./templates/encyclopedia/{page}.html')
print(t)