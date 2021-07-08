# from flask import Flask, render_template, request, redirect, url_for, session
# from datetime import date, datetime, timedelta
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
#         id = request.form['id']
#         password = request.form['password']
#         cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute(
#             'SELECT * FROM credentials WHERE id = %s AND password = %s', [id, password])
#         account = cursor.fetchone()
#         if account:
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['name'] = account['name']
#             msg = 'Logged in successfully !'
#             return render_template('index.html', msg=msg)
#         else:
#             msg = 'Incorrect id / password !'
#     return render_template('login.html', msg=msg)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == 'POST' and 'id' in request.form and 'password' in request.form and 'name' in request.form:
#         id = request.form['id']
#         password = request.form['password']
#         name = request.form['name']
#         cursor = MySQL.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM credentials WHERE id = %s', [id])
#         account = cursor.fetchone()
#         if account:
#             msg = 'Account already exists !'
#         elif not re.match(r'[A-Za-z]', name):
#             msg = 'Invalid name !'
#         elif not re.match(r'[A-Za-z0-9]+', id):
#             msg = 'Username must contain only characters and numbers !'
#         elif not id or not password or not name:
#             msg = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO credentials(id,name,password,status) VALUES (%s, %s, %s)', [
#                            id, name, password, "pending"])
#             MySQL.connection.commit()
#             msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('register.html', msg=msg)