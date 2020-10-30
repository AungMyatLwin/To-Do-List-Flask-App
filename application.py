from flask import Flask, render_template, request, session, redirect
from flask_bs4 import Bootstrap
import sqlite3

# init: flask
app = Flask(__name__)
db = sqlite3.connect("todoapps.db", check_same_thread=False)
curr = db.cursor()
try:
    sql = "Create table username(uid integer Primary Key,urname text, password text)"
    sql_table2 = ("Create table todo(id integer Primary Key,ToDoList Text,uid Integer,FOREIGN KEY (uid) REFERENCES "
                  "username (uid))")
    curr.execute(sql)
    curr.execute(sql_table2)
    print("success")
except:
    print("sql table already exists")
Bootstrap(app)


# routing
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("login_page.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        con_password = request.form.get("retype_password")
        if password == con_password:
            db.execute("Insert into username(urname,password) values(?,?)", (username, password))
            db.commit()
            return render_template("login_page.html", username=username)
        return render_template("register.html", username=username)
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sql_password = db.execute("select password from username where urname=(?)", [username])
        for s_p in sql_password:
            # convert tuple to string use .join in for loop
            sql_password = ''.join(s_p)
    if password != str(sql_password):
        print(password, sql_password)
        return render_template("login_page.html")
    return render_template("todolist.html", username=username)



tr = []


@app.route("/todolist", methods=["GET", "POST"])
def todolist():
    if request.method == "POST":
        todolists = request.form.get("Todolist")
        db.execute('INSERT INTO todo(ToDoList) values (?)', [todolists])
        db.commit()
        todo = db.execute('SELECT ToDoList from todo')
        for str_todo in todo:
            todo=''.join(str_todo)
        return render_template("todolist.html", todolists=todo)
        # return render_template("todolist.html", username="Paysi", todolists=(list(t) for t in todo))

    # delete from marks
    # order by id desc limit 1
    return render_template("todolist.html")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        todolists = request.form.get("Delete")
        delete = "delete from todo order by id desc limit 1"
        db.execute(delete)
        db.commit()
        todo = db.execute('SELECT ToDoList from todo')
        return render_template("delete.html", username="Paysi", todolists=todo)

    return render_template("todolist.html")


if __name__ == "__main__":
    app.run(debug=True)
