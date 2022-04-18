export FLASK_APP=run.py
export FLASK_ENV=testing
export DATABASE_URL=sqlite:///test.sqlite
pytest --disable-warnings
