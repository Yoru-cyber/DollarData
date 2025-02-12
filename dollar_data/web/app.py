from flask import Flask, render_template
import sqlite3
import os

cwd = os.getcwd()
# con = sqlite3.connect(cwd + "/database.db")
# cur = con.cursor()
app = Flask(__name__)


@app.route("/")
def hello_world():
    with sqlite3.connect(cwd + "/database.db") as con:
        cur = con.cursor()
        res = cur.execute("SELECT * FROM HistoricalDollar LIMIT 50 OFFSET 0")
        data = res.fetchall()
        return render_template(template_name_or_list="index.html", data=data)
