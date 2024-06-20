from multiprocessing import cpu_count
from os import environ

def max_workers():    
    return cpu_count()*2 + 1
port = environ.get('PORT', '8000')
bind = '0.0.0.0:' + port
max_requests = 1000
worker_class = 'gthread'
workers = max_workers()
threads = workers * 2

wsgi_app = 'mysite.wsgi:application'
