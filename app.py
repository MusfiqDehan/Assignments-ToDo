from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    serial_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    # def __init__(self, title, status, priority, due_date):
    #     self.title = title
    #     self.status = status
    #     self.priority = priority
    #     self.due_date = due_date

    def __repr__(self):
        return f"Todo('{self.title}', '{self.desc}', '{self.status}', '{self.priority}', '{self.due_date}')"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")
        status = request.form.get("status")

        todo = Todo(
            title=title, desc=desc, due_date=due_date, priority=priority, status=status
        )
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)


@app.route("/edit/<int:serial_no>", methods=["GET", "POST"])
def edit(serial_no):
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")
        status = request.form.get("status")

        todo = Todo.query.filter_by(serial_no=serial_no).first()

        todo.title = title
        todo.desc = desc
        todo.due_date = due_date
        todo.priority = priority
        todo.status = status

        db.session.commit()
        return redirect(url_for("index"))

    todo = Todo.query.filter_by(serial_no=serial_no).first()
    return render_template("edit.html", todo=todo)


@app.route("/delete/<int:serial_no>", methods=["GET", "POST"])
def delete(serial_no):
    todo = Todo.query.filter_by(serial_no=serial_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")  # here query will be the search inputs name
    alltodos = Todo.query.filter(Todo.title.like("%" + query + "%")).all()
    return render_template("search.html", query=query, alltodos=alltodos)


@app.route("/api/v1/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    todos_json = []
    for todo in todos:
        todo_json = {
            "title": todo.title,
            "desc": todo.desc,
            "due_date": todo.due_date,
            "priority": todo.priority,
            "status": todo.status,
        }
        todos_json.append(todo_json)
    return jsonify(todos_json)


if __name__ == "__main__":
    app.run(debug=True)
