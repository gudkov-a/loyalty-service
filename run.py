from app import app_factory

app = app_factory()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

