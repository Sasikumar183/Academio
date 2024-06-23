from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from jinja2 import Environment
app = Flask(__name__)
app.jinja_env.globals['len'] = len
# DATABASE CONNECTIVITY
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin@123'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        regno = request.form['regno']
        dob = request.form['dob']
       
        
        con = mysql.connection.cursor()
        sql = "SELECT * FROM result WHERE registerno = %s AND dob = %s"
        con.execute(sql, [regno, dob])
        res = con.fetchone()
        
        sql = "SELECT * FROM internal1 WHERE registerno = %s"
        con.execute(sql, [regno])
        mark = con.fetchone()
        print(mark)
        
        sql = "SHOW COLUMNS FROM internal1"
        con.execute(sql)
        columns = con.fetchall()
        column_names = [column['Field'] for column in columns]  # Extract column names
        mysql.connection.commit()
        con.close()  
        return render_template('result.html', data=res, result=mark, column_names=column_names)

    return render_template('index.html')

@app.route('/admin',methods=['POST','GET'])
def adminpanel():
    if(request.method=="POST"):
        uname=request.form['uname']
        password=request.form['password']
        con=mysql.connection.cursor()
        sql='select * from adminlist where username=%s and password=%s'
        con.execute(sql,[uname,password])
        res=con.fetchone()
        return render_template('markentry.html',data=res)
    return render_template('admin.html')

@app.route('/adminregister', methods=['POST','GET'])
def adminreg():
    if request.method=='POST':
        passcode = '12345'  # Convert passcode to string for comparison
        uname = request.form['username']
        password = request.form['pass']
        cpass = request.form['cpass']
        pcode = request.form['passcode']
        
        if pcode == passcode:  # Check if passcode matches
            if password == cpass:  # Check if passwords match
                con = mysql.connection.cursor()
                sql = 'INSERT INTO adminlist(username,password) VALUES (%s ,%s)'
                con.execute(sql, [uname, password])
                mysql.connection.commit()
                con.close()
                return render_template('markentry.html')
            else:
                return render_template('adminreg.html',data='Wrong passcode')
        else:
            data={'error':'Wrong Passcode'}
            return render_template('adminreg.html',datas=data)
    return render_template('adminreg.html',datas=[])
@app.confi
def markentry()
if __name__ == '__main__':
    app.secret_key = '1234547'
    app.run(debug=True,port='8080')
