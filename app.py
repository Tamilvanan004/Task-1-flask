from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    register_number = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


# Home page
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name")
        register_number = request.form.get("register_number")
        department = request.form.get("department")
        email = request.form.get("email")

        new_student = Student(
            name=name,
            register_number=register_number,
            department=department,
            email=email
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("students"))

    return render_template("home.html")


# Student details page
@app.route("/students")
def students():

    all_students = Student.query.all()

    return render_template(
        "student.html",
        students=all_students
    )


# Create database
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)