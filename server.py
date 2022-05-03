from flask import Flask

app = Flask(__name__)

# Need to move this to MVC structure
@app.route('/')
def hello_world():
    return "Hello world TEST"


if __name__ == "__main__":
    app.run(debug = True, port = 5001)