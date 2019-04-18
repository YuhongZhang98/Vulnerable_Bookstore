import sqlite3, os, hashlib
from flask import Flask, jsonify, render_template, request, g

app = Flask(__name__)
app.database = "sample.db"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restock')
def restock():
    return render_template('restock.html')

#API routes

@app.route('/api/v1.0/storeAPI', methods=['GET', 'POST'])
def storeapi():
    if request.method == 'GET':
        g.db = connect_db()
        curs = g.db.execute("SELECT * FROM textbooks")
        items = [{'items':[dict(name=row[0], quantity=row[1], price=row[2]) for row in curs.fetchall()]}]
        g.db.close()
        return jsonify(items+empls)

    elif request.method == 'POST':
        g.db = connect_db()
        name,quan,price = (request.json['name'],request.json['quantity'],request.json['price'])
        curs = g.db.execute("""INSERT INTO textbooks(name, quantity, price) VALUES(?,?,?)""", (name, quan, price))
        g.db.commit()
        g.db.close()
        return jsonify({'status':'OK','name':name,'quantity':quan,'price':price})

@app.route('/api/v1.0/storeAPI/<item>', methods=['GET'])
def searchAPI(item):
    g.db = connect_db()
    #curs = g.db.execute("SELECT * FROM shop_items WHERE name=?", item) #The safe way to actually get data from db
    curs = g.db.execute("SELECT * FROM textbooks WHERE name = '%s'" %item)
    results = [dict(name=row[0], quantity=row[1], price=row[2]) for row in curs.fetchall()]
    print(results)
    g.db.close()
    return jsonify(results)

def connect_db():
    return sqlite3.connect(app.database)

if __name__ == "__main__":

    #create database if it doesn't exist yet
    if not os.path.exists(app.database):
        with sqlite3.connect(app.database) as connection:
            c = connection.cursor()
            c.execute("""CREATE TABLE textbooks(name TEXT, quantity TEXT, price TEXT)""")
            c.execute('INSERT INTO textbooks VALUES("CS4753", "20", "30")')
            c.execute('INSERT INTO textbooks VALUES("CS3393", "60", "100")')
            c.execute('INSERT INTO textbooks VALUES("EXPOS1", "200", "40")')
            connection.commit()

    app.run()