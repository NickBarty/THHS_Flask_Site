from flask import Flask, render_template
from views import index

app = Flask(__name__)

app.register_blueprint(index)

if __name__ == '__main__':
    app.run()
