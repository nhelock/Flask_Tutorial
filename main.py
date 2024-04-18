from flask import Flask, render_template, request, redirect
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)
conn_str = "mysql://root:FunnyPassword321@localhost/boatdb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


def get_int(value, min, default):
	try:
		value = int(value)
		assert(value >= min)
	except:
		value = default

	return value


def run_query(query, parameters = None):
	return conn.execute(text(query), parameters)


# render a file
@app.route('/')
def index():
    return render_template('index.html')


# remember how to take user inputs?
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# get all boats
# this is done to handle requests for two routes -
@app.route('/boats/')
@app.route('/boats/<page>')
def get_boats(page=1):
    page = int(page)  # request params always come as strings. So type conversion is necessary.
    per_page = 10  # records to show per page
    boats = conn.execute(text(f"SELECT * FROM boats LIMIT {per_page} OFFSET {(page - 1) * per_page}")).all()
    print(boats)
    return render_template('boats.html', boats=boats, page=page, per_page=per_page)


@app.route("/boats/results/<boat_id>", methods=['GET', 'POST'])
def results_boat(boat_id = 1):
	boat_id = get_int(boat_id, 1, 1)

	boat = run_query(f"select * from `boats` where `id` = {boat_id}").first()

	return render_template("results.html", boat = boat)


@app.route("/boats/alter/<boat_id>", methods=['GET'])
def alter_boat(boat_id = 1):
	boat_id = get_int(boat_id, 1, 1)

	boat = run_query(f"select * from `boats` where `id` = {boat_id}").first()

	return render_template("alter.html", boat = boat)


@app.route("/boats/", methods=['POST'])
def alter_boat_request():
    boat_id = get_int(request.form.get("id"), 1, 1)

    success = None
    error = None

    try:
        conn.execute(
            text(f"UPDATE boats SET name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price where id = {boat_id}"),
            request.form
        )

        success = "Data changed"
    except Exception as e:
        print(e)
        error = e

    # boat = conn.execute(text(f"select * from boats where id = {boat_id}")).first()

    return redirect('../boats')


@app.route('/create', methods=['GET'])
def create_get_request():
    return render_template('boats_create.html')


@app.route('/create', methods=['POST'])
def create_boat():
    # you can access the values with request.from.name
    # this name is the value of the name attribute in HTML form's input element
    # ex: print(request.form['id'])
    try:
        conn.execute(
            text("INSERT INTO boats values (:id, :name, :type, :owner_id, :rental_price)"),
            request.form
        )
        return render_template('boats_create.html', error=None, success="Data inserted successfully!")
    except Exception as e:
        print(e)
        return render_template('boats_create.html', error=error, success=None)


@app.route('/delete', methods=['GET'])
def delete_get_request():
    return render_template('boats_delete.html')


@app.route('/delete', methods=['POST'])
def delete_boat():
    try:
        conn.execute(
            text("DELETE FROM boats WHERE id = :id"),
            request.form
        )
        return render_template('boats_delete.html', error=None, success="Data deleted successfully!")
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template('boats_delete.html', error=error, success=None)


if __name__ == '__main__':
    app.run(debug=True)
