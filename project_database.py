import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="timesheet")

mycursor=mydb.cursor()

#mycursor.execute("CREATE TABLE Employee (eid VARCHAR(30) PRIMARY KEY NOT NULL, aid VARCHAR(30) NOT NULL, username VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL, foreign key(aid) references admin(aid))")

#mycursor.execute("CREATE TABLE Admin (aid VARCHAR(30) PRIMARY KEY NOT NULL, username VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL)")

# s="INSERT INTO admin (aid,username,password) VALUES (%s,%s,%s)"
# a1=("A101","Moorthy","Moorthy")
# a2=("A102","Poornima","Poornima")
# #mycursor.execute(s,a2)
# #mydb.commit()
# #mycursor.execute("select * from employee")

# s1="INSERT INTO employee (eid,aid,username,password) VALUES (%s,%s,%s,%s)"
# e1=("E1001","A101","Kanthimathi","Kanthimathi")
# e2=("E1002","A102","Abinaya","Abinaya")
# e3=("E1003","A101","Prem","Prem")
# e4=("E1004","A102","Medha","Medha")
# e5=("E1005","A101","Santhosh","Santhosh")
# e6=("E1006","A102","Preethi","Preethi")
#mycursor.execute(s1,e6)
#mydb.commit()

#mycursor.execute("CREATE TABLE Employee_latest (eid VARCHAR(30) NOT NULL,status VARCHAR(30),sat varchar(10), sun varchar(10), mon varchar(10), tue varchar(10), wed varchar(10), thu varchar(10), fri varchar(10), start_date DATE, end_date DATE, foreign key(eid) references employee(eid))")
#mycursor.execute("CREATE TABLE Employee_history (eid VARCHAR(30) NOT NULL,status VARCHAR(30),sat varchar(10), sun varchar(10), mon varchar(10), tue varchar(10), wed varchar(10), thu varchar(10), fri varchar(10), start_date DATE, end_date DATE, active_flag varchar(10), foreign key(eid) references employee(eid))")

s2="INSERT INTO Employee_latest (eid,status,sat,sun,mon,tue,wed,thu,fri,start_date,end_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
eh1=("E1004","REJECTED","0","0","8","9","9","9","9","2021-07-03","2021-07-09")
# mycursor.execute(s2,eh1)
# mydb.commit()
eh2=("E1004","APPROVED","0","0","9","9","9","9","9","2021-07-03","2021-07-09")
# mycursor.execute(s2,eh2)
# mydb.commit()
#mycursor.execute("show tables")

s3="INSERT INTO Employee_history (eid,status,sat,sun,mon,tue,wed,thu,fri,start_date,end_date,active_flag) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
el1=("E1004","REJECTED","0","0","8","9","9","9","9","2021-07-03","2021-07-09","N")
el2=("E1003","APPROVED","0","0","9","8","9","9","9","2021-06-26","2021-07-02","Y")
el3=("E1003","APPROVED","0","0","9","9","9","9","9","2021-06-19","2021-06-25","Y")
mycursor.execute(s3,el2)
mycursor.execute(s3,el3)
mydb.commit()

#mycursor.execute("CREATE TABLE Admin_check (aid VARCHAR(30), eid VARCHAR(30) NOT NULL,sat varchar(10), sun varchar(10), mon varchar(10), tue varchar(10), wed varchar(10), thu varchar(10), fri varchar(10), start_date DATE, end_date DATE,foreign key(aid) references admin(aid), foreign key(eid) references employee(eid))")

s4="INSERT INTO Admin_check (aid,eid,sat,sun,mon,tue,wed,thu,fri,start_date,end_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
ac1=("A102","E1004","0","0","9","9","9","9","9","2021-07-03","2021-07-09")
# mycursor.execute(s4,ac1)
# mydb.commit()

for i in mycursor:
	print(i)
