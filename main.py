# import flask. If you don't have flask installed,
# hover your mouse over the yellow line in import statement
from flask import Flask

# Flask uses this argument to determine the root path of
# the application so that it later can find resource files
# relative to the location of the application.
app = Flask(__name__)


# Defining routes. We are telling Flask what to do when
# a request is made at '/' route. In this case, it is
# localhost:5000/
@app.route('/')  # Decorator
def index():
    return '<h1>Hello World!!</h1>'  # Return either HTML or simple text


if __name__ == '__main__':  # When this file is run...
    # ... start the app in debug mode. In debug mode,
    # server is automatically restarted when you make changes to the code
    app.run(debug=True)
