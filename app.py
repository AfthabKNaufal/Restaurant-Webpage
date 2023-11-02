from flask import Flask, render_template, request,redirect,url_for,session
from flask_mysqldb import MySQL
import mysql.connector


app=Flask(__name__)
app.secret_key = 'your_secret_key_here'
conn=mysql.connector.connect(host='localhost',user='root',password='',database='bakery')


order_list=[]

@app.route('/')
def layout():
     return render_template('layout.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        Emailid = request.form['Emailid']
        Password = request.form['Password']
        cur=conn.cursor()
        cur.execute(f"select Emailid,Password from register where Emailid='{Emailid}'")
        user=cur.fetchone()
        if Emailid and Password == user[1]:
            session[Emailid]=user[0]
            return render_template('order.html')
        else:
            return render_template('login.html',error='Invalid Username or Password')

        
    return render_template('login.html')  


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        Name=request.form['Name']
        Emailid=request.form['Emailid']
        Password=request.form['Password']
        cur=conn.cursor()
        cur.execute("INSERT INTO register (Name,Emailid,Password) VALUES(%s,%s,%s)",(Name,Emailid,Password))
        conn.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/temp')
def temp():
    return render_template('temp.html')




@app.route('/logout')
def logout():
    session.pop('Emailid',None)
    return redirect(url_for('layout'))



@app.route('/order',methods=['GET','POST'])
def order():
   if request.method=='POST':
        Item=request.form['Item']
        Qty=request.form['Qty']
        cur=conn.cursor()
        cur.execute("INSERT INTO order_list(Item,Qty) VALUES(%s,%s)",(Item,Qty))
        conn.commit()

        orderlist={
            'Item':Item,
            'Qty':Qty

        }
        order_list.append(orderlist)
        return redirect('/temp')
   return render_template('order.html')







@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        Name = request.form['Name']
        Password = request.form['Password']

       

        if Name == 'Admin' and Password == 'Password':
           
            return redirect('/admin_dash')
        else:
            
            return "Login failed. Please try again."

    return render_template('admin.html')

@app.route('/admin_dash')
def admin_dash():
    return render_template('admin_dash.html',order_list=order_list)

if __name__=='__main__':
    app.run()

       

      