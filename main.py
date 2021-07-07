from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date, datetime, timedelta
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# get - backend to front end
# post - frontend to backed

# aid = ''

app = Flask(__name__)

app.secret_key = 'Team-F'

# MySQL Credentials
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'premraj123!'
app.config['MYSQL_DB'] = 'timesheet'

mysql = MySQL(app)


@app.route('/')
@app.route('/MainScreen')
def MainScreen():
    return render_template("MainScreen.html")


@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    msg = ''
    if request.method == "GET":
        return render_template("employee_login.html", msg=msg)
    else:
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM employee WHERE eid = %s AND password = %s AND username =%s', [id, password, username])
        account = cursor.fetchone()
        if account:
            session['employeeside_eid'] = account['eid']
            print("Employee logged in successfully")
            session['employeeloggedin'] = True
            return redirect(url_for('employee_history'))
        else:
            msg = "Incorrect ID/Username/Password"
        return render_template('employee_login.html', msg=msg)


@app.route('/employee_history')
def employee_history():
    # setting up cursor for MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Querying the database for getting the employee_history
    cursor.execute(
        "select * from employee_history where eid =%s and active_flag =%s order by end_date desc", [session['employeeside_eid'],"Y"])
    # Fetching all the rows
    empTimesheetDetails = cursor.fetchall()
    # Initializing the list
    empTimesheetHistoryList = []
    # Checking if the list is empty
    if empTimesheetDetails:
        # Algorithm for calculating the current week's end (friday)
        friday = (datetime.now() + timedelta(days=(4 -
                                                   datetime.now().weekday()) % 7)).date()
        # Algorithm for calculating the current week's start (saturday)
        saturday = (
            datetime.now() - timedelta(days=((datetime.now().isoweekday() + 1) % 7))).date()
        # Iterating through each value in empTimesheetDetails
        for val in empTimesheetDetails:
            if empTimesheetDetails.index(val) == 0 and str(friday) != str(val['end_date']):
                empTimesheetHistoryList.append([{'eid': val['eid'], 'status': 'pending', 'saturday':0, 'sunday': 0, 'monday': 0, 'tuesday': 0, 'wednesday':0, 'thursday': 0, 'friday': 0, 'start_date':saturday, 'end_date':friday}
                                                ])
            empTimesheetHistoryList.append([{'eid': val['eid'], 'status': val['status'], 'saturday': val['sat'], 'sunday': val['sun'], 'monday': val['mon'], 'tuesday': val['tue'], 'wednesday': val['wed'], 'thursday': val['thu'], 'friday': val['fri'], 'start_date':val['start_date'], 'end_date':val['end_date']}
                                            ])
    # This is triggered when output query tuple-  empTimesheetDetails is empty
    else:
        friday = (datetime.now() + timedelta(days=(4 -
                                                   datetime.now().weekday()) % 7)).date()
        empTimesheetHistoryList.append([{'eid': session['employeeside_eid'], 'status': 'pending', 'saturday':0, 'sunday': 0, 'monday': 0, 'tuesday': 0, 'wednesday':0, 'thursday': 0, 'friday': 0, 'start_date':saturday, 'end_date':friday}
                                        ])
    # Returning employee_history.html with empTimesheetHistoryList as argument
    return render_template('employee_history.html', history=empTimesheetHistoryList)


@app.route('/employee_timesheet_enter', methods=['GET', 'POST'])
def employee_timesheet_enter():
    if session['employeeloggedin'] == True:
        # Code for GET Request
        if request.method == "GET":
            id = request.args.get("id")
            end_date = request.args.get("ed")
            start_date = request.args.get("sd")
            status = request.args.get("status")
            print(f'id: {id}')
            print(f'Status: {status}')
            # Setting cursor
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            currentTimesheet = [id, start_date, end_date,
                                '0', '0', '0', '0', '0', '0', '0', "PENDING"]
            # Code for PENDING Status
            if status.lower() == "pending":
                print('came inside pending')
                cursor.close()
                return render_template('employee_timesheet_enter.html', ct=currentTimesheet)

            # Code for APPROVED Status
            elif status.lower() == "approved" or status.lower() == "submitted":
                print('came inside approved and submitted')
                cursor.execute(
                    "select * from employee_history where eid=%s and active_flag=%s and end_date=%s", [id, "Y", end_date])
                val = cursor.fetchone()
                print(f'val: {val}')
                cursor.close()
                if val:
                    print("Came inside val")
                    currentTimesheet = [id, val['start_date'], val['end_date'], val['sat'], val['sun'],
                                        val['mon'], val['tue'], val['wed'], val['thu'], val['fri'], val['status']]
                    return render_template('employee_timesheet_enter.html', ct=currentTimesheet)
                else:
                    return render_template('employee_timesheet_enter.html', ct=currentTimesheet)

            # Code for REJECTED Status
            elif status.lower() == 'rejected':
                print('came inside rejected')
                cursor.execute(
                    "select * from employee_latest where eid=%s", [id])
                val = cursor.fetchone()
                cursor.close()
                if val:
                    currentTimesheet = [id, val['start_date'], val['end_date'], val['sat'], val['sun'],
                                        val['mon'], val['tue'], val['wed'], val['thu'], val['fri'], val['status']]
                    return render_template('employee_timesheet_enter.html', ct=currentTimesheet)
                else:
                    return render_template('employee_timesheet_enter.html', ct=currentTimesheet)
            print('final return')
            return render_template('employee_timesheet_enter.html')

        # Code for POST Request
        elif request.method == "POST":

            # Getting all the data from front-end
            sat = request.form['sat']
            sun = request.form['sun']
            mon = request.form['mon']
            tue = request.form['tue']
            wed = request.form['wed']
            thu = request.form['thu']
            fri = request.form['fri']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            status = request.form['status']
            eid = request.form['eid']

            # Setting cursor1 to fetch aid
            cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor1.execute("select aid from employee where eid=%s", [eid])
            aid = cursor1.fetchone()
            aid = aid['aid']
            session['eid'] = eid
            # setting cursor2
            cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # deleting previous data from employee_latest
            cursor2.execute(
                "delete from employee_latest where eid=%s and end_date=%s", [eid, end_date])

            # inserrting latest timesheet data to employee_latest table
            cursor2.execute("insert into employee_latest(eid,aid,status,sat,sun,mon,tue,wed,thu,fri,start_date,end_date)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [
                            eid, aid, "SUBMITTED", sat, sun, mon, tue, wed, thu, fri, start_date, end_date])

            # updating active_flag of previous data in employee_history to N
            cursor2.execute("update employee_history set active_flag =%s where eid = %s and end_date =%s", [
                            "N", eid, end_date])

            # inserting new data with active_flag Y to employee_history table
            cursor2.execute("insert into employee_history(eid,aid,status,sat,sun,mon,tue,wed,thu,fri,start_date,end_date,active_flag)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [
                            eid, aid, "SUBMITTED", sat, sun, mon, tue, wed, thu, fri, start_date, end_date, "Y"])

            # committing changes to databsae
            mysql.connection.commit()

            # closing cursors
            cursor1.close()
            cursor2.close()

            # Setting dataIsSet Session so that data isnt added to database when refreshed
            session['dataIsSet'] = True

            # Returning custom created employee_history_post route after data is set.
            return redirect(url_for('employee_history'))
    else:
        return render_template('employee_login.html')


@app.route('/employee_logout')
def logout():
    session['employeeloggedin'] = False
    return render_template('MainScreen.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    # Initializing msg variable
    msg = ''
    # Checking if the request is a GET Request
    if request.method == "GET":
        # Returning admin_login.html for get request
        return render_template("admin_login.html", msg=msg)
    # Checking if the request is a post request
    elif request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM admin WHERE aid = %s AND password = %s AND username =%s', [id, password, username])
        account = cursor.fetchone()
        if account:
            session['userloggedin'] = True
            session['adminside_aid'] = id
            return redirect(url_for("admin_select"))
        else:
            msg = "Incorrect ID/Username/Password"
    return render_template("admin_login.html", msg=msg)


@app.route('/admin_select')
def admin_select():
    return render_template('admin_select.html')


@app.route('/pending', methods=['GET', 'POST'])
def pending():
    # This checks for get request
    if request.method == "GET":
        aid = session['adminside_aid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "select * from employee_latest where aid=%s and status=%s", [aid, "SUBMITTED"])
        employeeData = cursor.fetchall()
        cursor.execute("Select * from admin_check where aid=%s", [aid])
        adminCheckData = cursor.fetchall()
        employeeAndAdminDataList = []
        print(f'employeedata: {employeeData}')
        print(f'admindata{adminCheckData}')
        if employeeData:
            for val in employeeData:
                i = employeeData.index(val)
                if adminCheckData:
                    employeeAndAdminDataList.append([[{'eid': val['eid'], 'saturday': val['sat'], 'sunday': val['sun'], 'monday': val['mon'], 'tuesday': val['tue'], 'wednesday': val['wed'], 'thursday': val['thu'], 'friday': val['fri'], 'start_date':val['start_date'], 'end_date':val['end_date'], 'aid':aid}
                                                      ], [{'saturday': adminCheckData[i]['sat'], 'sunday': adminCheckData[i]['sun'], 'monday': adminCheckData[i]['mon'],
                                                           'tuesday': adminCheckData[i]['tue'], 'wednesday': adminCheckData[i]['wed'], 'thursday': adminCheckData[i]['thu'], 'friday': adminCheckData[i]['fri']}]])
                else:
                    employeeAndAdminDataList.append([[{'eid': val['eid'], 'saturday': val['sat'], 'sunday': val['sun'], 'monday': val['mon'], 'tuesday': val['tue'], 'wednesday': val['wed'], 'thursday': val['thu'], 'friday': val['fri'], 'start_date':val['start_date'], 'end_date':val['end_date'], 'aid':aid}
                                                      ], [{'saturday': 'N/A', 'sunday': 'N/A', 'monday': 'N/A',
                                                           'tuesday': 'N/A', 'wednesday': 'N/A', 'thursday': 'N/A', 'friday': 'N/A'}]])

        return render_template('admin_pending.html', employeeAdminData=employeeAndAdminDataList)


@app.route('/status')
def status():
    eid = request.args.get('eid')
    end_date = request.args.get('ed')
    status = request.args.get('status')
    aid = request.args.get('aid')
    print(status)
    print(type(status))
    print(type(str(status)))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('update employee_latest set status=%s where eid=%s and aid=%s and end_date=%s', [
                   status, eid, aid, end_date])
    cursor.execute('update employee_history set status=%s where eid=%s and aid=%s and end_date=%s and active_flag=%s', [
                   status, eid, aid, end_date, "Y"])
    mysql.connection.commit()
    return redirect(url_for('pending'))


@app.route('/approved', methods=['GET', 'POST'])
def approved():
    if request.method == "GET":
        # Initializing cursor for MySql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Executing query to get all approved data from employee_history table
        cursor.execute('select * from employee_history where aid=%s and status=%s and active_flag =%s',
                       [session["adminside_aid"], "APPROVED", "Y"])
        # Fetching all the rows from the query
        adminApprovedData = cursor.fetchall()
        print(adminApprovedData)
        # Initializing list
        adminApprovedDataList = []
        # Checking if the returned query tuple is empty
        if adminApprovedData:
            for val in adminApprovedData:
                adminApprovedDataList.append([{'eid': val['eid'], 'saturday': val['sat'], 'sunday': val['sun'], 'monday': val['mon'], 'tuesday': val['tue'], 'wednesday': val['wed'], 'thursday': val['thu'], 'friday': val['fri'], 'start_date':val['start_date'], 'end_date':val['end_date']}
                                              ])
        return render_template('admin_approved.html', adminApprovedData=adminApprovedDataList)


@app.route('/all', methods=['GET', 'POST'])
def all():
    if request.method == "GET":
        # Initializing cursor for MySql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Executing query to get all approved data from employee_history table
        cursor.execute('select * from employee_history where aid=%s',
                       [session['adminside_aid']])
        # Fetching all the rows from the query
        adminAllData = cursor.fetchall()
        # Initaializing list
        adminAllDataList = []
        # Checking if the query returned tuple is empty
        if adminAllData:
            for val in adminAllData:
                adminAllDataList.append([{'eid': val['eid'],'status':val['status'] ,'saturday': val['sat'], 'sunday': val['sun'], 'monday': val['mon'], 'tuesday': val['tue'], 'wednesday': val['wed'], 'thursday': val['thu'], 'friday': val['fri'], 'start_date':val['start_date'], 'end_date':val['end_date'], 'active_flag':val['active_flag']}
                                         ])
        return render_template('admin_all.html', adminAllData=adminAllDataList)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
        id = request.form['id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM credentials WHERE id = %s AND password = %s', [id, password])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['name'] = account['name']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect id / password !'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form and 'name' in request.form:
        id = request.form['id']
        password = request.form['password']
        name = request.form['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM credentials WHERE id = %s', [id])
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z]', name):
            msg = 'Invalid name !'
        elif not re.match(r'[A-Za-z0-9]+', id):
            msg = 'Username must contain only characters and numbers !'
        elif not id or not password or not name:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO credentials(id,name,password,status) VALUES (%s, %s, %s)', [
                           id, name, password, "pending"])
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


if __name__ == "__main__":
    app.run(debug=True)


# @app.route('/employee_history_post')
# def employee_history_post():
#     # setting session
#     eid = session.get('eid')

#     # Checking if dataIsSet
#     if session['dataIsSet']:
#         # Setting dataIsSet to False, to prevent data reloading to database when page is refreshed
#         session['dataIsSet'] = False
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

#         # getting data here for navigating to employee history
#         cursor.execute(
#             "select * from employee_history where eid =%s order by end_date desc", [eid])

#         # fetching all the matched rows from the tables
#         empTimesheetDetails = cursor.fetchall()

#         # declaring an empty list for passing history data to employee_history.html file
#         empTimesheetHistoryList = []

#         # Checkinf if the returned query tuple is empty
#         if empTimesheetDetails:
#             # Algorithm for getting current week's friday
#             friday = (datetime.now() + timedelta(days=(4 -
#                                                        datetime.now().weekday()) % 7)).date()
#             # Algorithm for getting current week's saturday
#             saturday = (
#                 datetime.now() - timedelta(days=((datetime.now().isoweekday() + 1) % 7))).date()
#             for val in empTimesheetDetails:
#                 # Condion to get the top/first element in the returned query tuple and checking if
#                 # the top/first element isn't already set in the table
#                 if empTimesheetDetails.index(val) == 0 and str(friday) != str(val['end_date']):
#                     # With this algorithm by default every week, that weeks pending timesheet will apprear
#                     empTimesheetHistoryList.append([{'eid': val['eid'], 'status': 'pending', 'saturday':0, 'sunday': 0, 'monday': 0, 'tuesday': 0, 'wednesday':0, 'thursday': 0, 'friday': 0, 'start_date':saturday, 'end_date':friday}
#                                                     ])
#                 # This line adds, rest of the elements to the list
#                 empTimesheetHistoryList.append([{'eid': val['eid'], 'status': val['status'], 'saturday': val['sat'], 'sunday': val['sun'], 'monday': val['mon'], 'tuesday': val['tue'], 'wednesday': val['wed'], 'thursday': val['thu'], 'friday': val['fri'], 'start_date':val['start_date'], 'end_date':val['end_date']}
#                                                 ])
#         # This condition executes when the returned query tuple is empty
#         else:
#             # Here if the returned tuple is empty, we are returning the current weeks timesheet with PENDING status
#             friday = (datetime.now() + timedelta(days=(4 -
#                                                        datetime.now().weekday()) % 7)).date()
#             empTimesheetHistoryList.append([{'eid': eid, 'status': 'pending', 'saturday': 0, 'sunday': 0, 'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0, 'start_date': saturday, 'end_date': friday}
#                                             ])
#         # Returning employee_history.html file with an argument whose value is empTImesheetHistoryList
#         return render_template('employee_history.html', history=empTimesheetHistoryList)
#     else:
#         return render_template('employee_history.html', history=[])
