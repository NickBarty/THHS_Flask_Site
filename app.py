from flask import Flask

from views import predict_page

app = Flask(__name__)
app.secret_key = "qwertyuiop"

app.register_blueprint(predict_page)

if __name__ == '__main__':
    app.run()
