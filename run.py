from app import app
from os import environ as env

app.config['SECRET_KEY'] = env.get('SECRET_KEY')
if __name__ == '__main__':
    # PORT = int(env.get('PORT', 8000))
    app.run(debug=True)