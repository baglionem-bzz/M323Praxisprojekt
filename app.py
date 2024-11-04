from flask import Flask
from recipes_bp import recipes_bp
app = Flask(__name__)

app.register_blueprint(recipes_bp, url_prefix='/recipes')



if __name__ == '__main__':
    app.run(debug=True)
