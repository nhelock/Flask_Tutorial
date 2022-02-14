from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!!</h1>'


# adding more routes
@app.route('/hello')
def hello():  # defining index() again would have given an error
    return 'Hey there!'


# variable input in route
# try localhost:5000/john, or localhost:5000/mary
@app.route('/hello/<name>')  # name is the input var
def greet(name):  # name is passed down as parameter
    return 'Hey there, ' + name + '!'


# specifying data type
@app.route('/hello_str/<string:name>')  # don't put any spaces in url
def greet_string(name):
    return 'Hey there!' + name


# int data type. Try -
# localhost:5000/hello_num/1
# localhost:5000/hello_num/one
@app.route('/hello_num/<int:num>')
def next_number(num):
    return 'Next number is ' + str(num + 1)


if __name__ == '__main__':
    app.run(debug=True)
