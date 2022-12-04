from flask import Flask, render_template, redirect, request, session, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
PASSWORD=os.getenv('password')

dbconfig = {
    "user" : "root",
    "password" : "{}".format(PASSWORD),
    "host" : "localhost",
    "database" : "week6_DB",
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "mypool",
    pool_size = 5,
    pool_reset_session = True,
    **dbconfig
    )

# app=Flask(__name__)
app=Flask(__name__,static_folder='static',static_url_path='/')
app.secret_key='12345678'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name=request.form['name']
    account=request.form['account']
    password=request.form['password']
    connection_object = connection_pool.get_connection()
    mycursor =  connection_object.cursor()
    if name=="" or account=="" or password=="":
        return redirect('/error?message=任一欄位不可有空值')
    else:
        sql='select account from member where account=%s'
        val=(account,) #這寫法比較特別要注意
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
    if result!=[]:
        mycursor.close()
        connection_object.close()
        return redirect('/error?message=帳號已有人註冊')
    else:
        sql='insert into member(name, account,password) values (%s,%s,%s)'
        val=(name, account, password)
        mycursor.execute(sql,val)
        connection_object.commit()
        mycursor.close()
        connection_object.close()
        return redirect('/')
    

@app.route('/signin', methods=['POST'] )
def signin():
    connection_object = connection_pool.get_connection()
    mycursor =  connection_object.cursor()
    account=request.form['account']
    password=request.form['password']
    sql="select * from member where account=(%s) and password=(%s)"
    val=(account,password)
    mycursor.execute(sql,val)
    result = mycursor.fetchone()
    if result!=None:
        session['user_ID']=result[0]
        session['name']=result[1]
        session['account']=result[2]
        return redirect('/member')
    else:
        # connection_object.commit()
        mycursor.close()
        connection_object.close()
        return redirect('/error?message=帳號或密碼輸入錯誤')

@app.route('/signout')
def signout():
    del session['name']
    return redirect('/')

@app.route('/member')
def member():
    connection_object = connection_pool.get_connection()
    mycursor =  connection_object.cursor()
    if 'name' in session:
            sql="select message.id, name, message from member inner join message on member.id=message.user_ID;"
            mycursor.execute(sql)
            result = mycursor.fetchall()
            result.sort(reverse = True)
            messages=''
            for i in result:
                messages+="{}:{}<br>".format(i[1],i[2])
            mycursor.close()
            connection_object.close()
            print(session['name'])
            return render_template('member.html',username=session['name'],message=messages)
    else:
        return redirect('/')

@app.route('/error')
def error():
    message=request.args.get('message',"發生錯誤")
    return render_template('error.html',msg=message)

@app.route('/message', methods=['post'] )
def message():
    if 'name' in session:
        connection_object = connection_pool.get_connection()
        mycursor =  connection_object.cursor()
        message=request.form['message']
        sql='insert into message (user_ID, message) values(%s,%s)'
        val=(session['user_ID'], message)
        mycursor.execute(sql,val)
        connection_object.commit()
        return redirect('/member')
    else:
        return redirect('/')

@app.route('/api/member', methods=['GET', 'PATCH'])
def API_member():
    if 'name' in session:
        if request.method=='GET':
            username=request.args.get('username')
            connection_object = connection_pool.get_connection()
            mycursor =  connection_object.cursor()
            sql='select * from member where account=(%s)'
            val=(username,)
            mycursor.execute(sql,val)
            result = mycursor.fetchone()
            print(result)
            mycursor.close()
            connection_object.close()
            if result!= None:
                return jsonify({
                    '"data"':{
                        '"id"':result[0],
                        '"name"':result[1],
                        '"username"':result[2]
                        }
                    }) 
            else:
                return jsonify({
                    '"data"':None}) #json會自動轉成null
        elif request.method=='PATCH':
            try:
                json=request.get_json() #取得request的json檔
                print(json)
                new_name = json['name']
                print(new_name)
                connection_object = connection_pool.get_connection()
                mycursor =  connection_object.cursor()
                sql = 'update member set name = %s where id = %s '
                val = (new_name, session['user_ID'])
                mycursor.execute(sql,val)
                connection_object.commit()
                mycursor.close()
                connection_object.close()
                return jsonify({
                    '"ok"':True
                })
            except:
                return jsonify({
                    '"error"':True
                })
        else:
            return redirect('/')
    else:
        return redirect('/')


app.run(host='0.0.0.0', port=3000, debug=True)
