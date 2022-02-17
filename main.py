from flask import Flask, render_template
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)

# initialize database
# connection string is in the format mysql://user:password@server/database
conn_str = "mysql://root:iit123@localhost/boatdb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


# create model
class BoatsModel:
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
    # local_session = Session(bind=engine)
    # boats = local_session.query(BoatsModel).all()  # returns all boats
    boats = conn.execute(text("select * from boats")).all()
    print(boats)
    return render_template('boats.html', boats=boats[:10])


if __name__ == '__main__':
    app.run(debug=True)
