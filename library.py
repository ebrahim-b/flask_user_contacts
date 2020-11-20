from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+pymysql://root:@localhost/mylibapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Comments(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(30))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20))


@app.route("/")
def index():
    result = Comments.query.all()
    return render_template("index.html",result = result)

@app.route("/submit")
def submit():
    return render_template("submit.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    lname = request.form["lname"]
    email = request.form["email"]
    phone = request.form["phone"]

    user_comment = Comments(name = name, lname = lname , email = email, phone = phone)
    db.session.add(user_comment)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/show_update/<id>/")
def show_update(id):
    result = Comments.query.get(id)
    return render_template("edit.html",result = result)

@app.route('/update/<id>/', methods = ['GET', 'POST'])
def update(id):
        my_data = Comments.query.get(id)

        my_data.name = request.form['name']
        my_data.lname = request.form['lname']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Comments.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)