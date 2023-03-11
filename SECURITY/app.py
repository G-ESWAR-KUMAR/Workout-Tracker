from flask import Flask,render_template,request
import mysql.connector as mysql
import plotly.express as px
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app=Flask(__name__)
db=mysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'Eswar*143/',
    database ='eswar'
)
app.secret_key='1234'

 
cur=db.cursor() 

@app.route('/')
def homer():
    return render_template('Homer.html')

@app.route('/register',methods=['get'])
def new():
    return render_template('index.html')


@app.route('/details',methods=['POST'])
def details():
    name=request.form['Name']
    email=request.form['RollNo']
    password=request.form['Password']
    phone=request.form['Phoneno']
    city=request.form['Department']
 
    cur.execute('select name from pavan')
    result=cur.fetchall()
    flag=0
    for i in result:
        if i[0]==name and name=="":
            flag=1
            return render_template('index.html',result='Existed User')
    if flag==0:
        sql='insert into pavan (name,email,password,phone,city) values(%s,%s,%s,%s,%s)'
        values=(name,email,password,phone,city)
        cur.execute(sql,values)
        db.commit()
        if(cur.rowcount==1):
            return render_template('index.html',result='Registration Successful')
        else:
            return render_template('index.html',result='Registration Failed')

@app.route('/login',methods=['get'])
def login():
    return render_template('login.html')

@app.route('/verify',methods=['post','get'])
def verify():
    userid=request.form['Email']
    password=request.form['Password']
    cur.execute('SELECT * FROM pavan')
    res=cur.fetchall()
    flag=0
    for i in res:
        if(i[1]==userid and i[2]==password):
            flag=0
            return render_template('email.html')
        else:
            return render_template('login.html',result='Enter correct details')

@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/hom')
def hom():
    return render_template('email.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/form')
def open1():
    return render_template('entry.html')

@app.route('/store',methods=['POST'])
def store():
    date=request.form['name']
    work=request.form['workout_name']
    time=request.form['time']

 
    cur.execute('select date from workout')
    result=cur.fetchall()
    flag=0
    for x in result:
        if date==x[0]:
            flag=1
            return render_template('entry.html',result=' User')
    if flag==0:
        sql='insert into workout (date,workout,time) values(%s,%s,%s)'
        values=(date,work,time)
        cur.execute(sql,values)
        db.commit()
        if(cur.rowcount==1):
            return render_template('entry.html',result='Added Successful.')
        else:
            return render_template('entry.html',result='Failed To Add.')


@app.route('/table',methods=['get'])
def cancel():
    cur.execute('select * from workout')
    result=cur.fetchall()
    for x in result:
        print(type(x))
    print(result)
    return render_template('previous.html',data=result)
 

@app.route('/graph',methods=['get'])
def tr():
    cur.execute('select * from workout')
    result=cur.fetchall()
    date=[]
    workout=[]
    time=[]
    for i in result:
        date.append(i[0])
        workout.append(i[1])
        time.append(i[2])

    trace1 = px.scatter(
    x=date,
    y=time,
    color=workout
    )
    p=px.bar(x=date,y=time,color=workout)
    y=px.pie(time,names=workout)
    y.show()
    p.show()
    trace1.show()

    return render_template('email.html')
        
@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/ver',methods=['get','post'])
def ver():
    msgg=request.args.get('Email')
    smtp_port = 587                 
    smtp_server = "smtp.gmail.com"  
    email_from = "eswarkumar1430@gmail.com"
    email_list = msgg

    pswd = "sqlqftryidydcywn"


    subject = "New email from WORKOUT TRACKER..."

    body = f"""
    Free diet-plan for a week
    """

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_list
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    filename = "test.txt"

    attachment= open(filename,"rb")  

    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(attachment_package)

    text = msg.as_string()

    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pswd)
    print("Succesfully connected to server")
    print()

    print(f"Sending email to: {email_list}...")
    TIE_server.sendmail(email_from,email_list, text)
    print(f"Email sent to: {email_list}")
    print()

    TIE_server.quit()
    return render_template('email.html',result='Email Sent Successfully.')


@app.route('/benefits')
def benefits():
    return render_template('try.html')

@app.route('/bmi1',methods=['post','get'])
def bmi():
    height=request.form['h']
    weight=request.form['w']
    if height=="" and weight=="":
        return render_template('bmi.html', result="Invalid")
    else:
        x=int(height)
        we=int(weight)
        h= float(x/100)
        bmi= float(we/(h*h))
        if bmi<=18.5:
            return render_template("bmi.html", result=bmi,res="Oops! You are underweight.")
        elif bmi<=24.9:
            return render_template("bmi.html", result=bmi,res="Awesome! You are healthy.")
        elif bmi<=29.9:
            return render_template("bmi.html", result=bmi,res="Eee! You are overweight.")
        else:
            return render_template("bmi.html", result=bmi,res="Seesh! You are obese.")
 

@app.route('/bmi')
def bmi1():
    return render_template('bmi.html') 

 

if __name__=="__main__":
    app.run(debug=True)