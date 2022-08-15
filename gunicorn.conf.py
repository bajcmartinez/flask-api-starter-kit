import multiprocessing

bind = "127.0.0.1:11111"
workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "wsgi:app"

