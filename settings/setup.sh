cd ..
mkdir venv
cd venv
python3 -m venv .
cd ..
source venv/bin/activate
pip3 install -r requirements.txt --index-url https://pypi.douban.com/simple
pip3 install gunicorn --index-url https://pypi.douban.com/simple
pip3 install eventlet --index-url https://pypi.douban.com/simple
pip3 install coverage --index-url https://pypi.douban.com/simple
deactivate
source venv/bin/activate
python3 manage.py init
deactivate
echo "Finished"

