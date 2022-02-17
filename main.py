from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric

app = Flask(__name__)

# initialize database
# URI is in the format mysql://user:password@server/database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:iit123@localhost/boatdb"
db = SQLAlchemy(app)


# create model
class BoatsModel(db.Model):
    __tablename__ = 'boats'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(32))
    type = Column('type', String(32))
    owner_id = Column('owner_id', Integer)
    rental_price = Column('rental_price', Numeric)


# render a file
@app.route('/')
def index():
    return render_template('index.html')


# remember how to take user inputs?
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# get all boats
@app.route('/boats')
def get_boats():
    boats = BoatsModel.query.all()  # returns all boats
    print(boats)
    return render_template('boats.html', boats=boats[:10])


if __name__ == '__main__':
    app.run(debug=True)
