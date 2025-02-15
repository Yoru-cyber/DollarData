wsgi_app = "dollar_data.wsgi:app"
bind = "0.0.0.0:8000"
workers = 2
preload_app = True