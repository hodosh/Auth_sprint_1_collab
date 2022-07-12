from app import create_app
from core import config

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host=config.FLASK_HOST, port=config.FLASK_PORT)
