# Python Package

```
cd kyonkat
virtualenv kyonkat_env
source kyonkat_env/bin/activate

pip install -r requirements.txt
pip install gunicorn
```

# Python Deploy

```
python manage.py makemigrations entity
python manage.py migrate
python manage.py collectstatic
gunicorn --bind 0.0.0.0:8000 kyonkat.wsgi

```

# Create Gunicorn Service

```
sudo nano /etc/systemd/system/kyonkat.service

------------------------------------------

[Unit]
    Description=kyonkat service
    After=network.target

[Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/kyonkat
    ExecStart=/home/ubuntu/kyonkat/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/kyonkat/kyonkat.sock kyonkat.wsgi:application

[Install]
    WantedBy=multi-user.target

------------------------------------------
```

# Create Nginx Server

```

sudo nano /etc/nginx/sites-available/kyonkat

------------------------------------------

server {
    listen 80;
    server_name kyonkat.in www.kyonkat.in;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/kyonkat;
    }
    location /media/ {
        root /home/ubuntu/kyonkat;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/kyonkat/kyonkat.sock;
    }
}

------------------------------------------

sudo ln -s /etc/nginx/sites-available/kyonkat /etc/nginx/sites-enabled
```
