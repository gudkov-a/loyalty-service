python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

export FLASK_APP=run.py
export FLASK_ENV=testing
export DATABASE_URL=sqlite:///test.sqlite
pytest --disable-warnings
