cd ../venv/Scripts

activate.bat


cd ../..
gunicorn -w 4 -b 127.0.0.1:5002 --worker-connections 100 wsgi:app
