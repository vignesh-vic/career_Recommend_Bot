from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import time
import datetime
from flask import send_file
from random import randint
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt  
import pandas as pd
import numpy as np
import mysql.connector

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error as mse

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="career_recommend"
)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####


@app.route('/',methods=['POST','GET'])
def index():
    act=""
    msg=""

    return render_template('index.html',msg=msg,act=act)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/stu_login',methods=['POST','GET'])
def stu_login():
    act=""
    msg=""
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM cr_student WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('stu_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('stu_login.html',msg=msg,act=act)



@app.route('/stu_register',methods=['POST','GET'])
def stu_register():
    msg=""
    act=""
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        email=request.form['email']
        
        uname=request.form['uname']
        pass1=request.form['pass']
        address=request.form['address']
        city=request.form['city']
        
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM cr_student where uname=%s",(uname, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM cr_student")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO cr_student(id, name, gender, dob, mobile, email, address, city, uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, gender, dob, mobile, email, address, city, uname,pass1)
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "record inserted.")
            msg='success'
            
            #if mycursor.rowcount==1:
            #    result="Registered Success"
            
        else:
            msg="fail"
    return render_template('stu_register.html',msg=msg)


@app.route('/stu_home',methods=['POST','GET'])
def stu_home():
    uname=""

    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM cr_student where uname=%s",(uname, ))
    data = cursor.fetchone()
    sid=data[0]

    cursor.execute("SELECT * FROM cr_skills where uname=%s && stype='Sports'",(uname, ))
    data2 = cursor.fetchall()

    cursor.execute("SELECT * FROM cr_skills where uname=%s && stype='Skills'",(uname, ))
    data3 = cursor.fetchall()
    
    return render_template('stu_home.html',data=data,sid=sid,data2=data2,data3=data3)

@app.route('/stu_school',methods=['POST','GET'])
def stu_school():
    uname=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cr_student where uname=%s",(uname, ))
    data = mycursor.fetchone()
    if request.method=='POST':
        school1=request.form['school1']
        mark1=request.form['mark1']
        percent1=request.form['percent1']
        c2=request.form['c2']
        
        mycursor.execute("update cr_student set school1=%s,mark1=%s,percent1=%s where uname=%s", (school1,mark1,percent1,uname))
        mydb.commit()

        if c2=="2":
            school2=request.form['school2']
            mark2=request.form['mark2']
            percent2=request.form['percent2']
            hs_group=request.form['hs_group']
            mycursor.execute("update cr_student set school2=%s,mark2=%s,percent2=%s,hs_group=%s where uname=%s", (school2,mark2,percent2,hs_group,uname))
            mydb.commit()

        
        return redirect(url_for('stu_home'))
        
    
    return render_template('stu_school.html',data=data)

@app.route('/stu_degree',methods=['POST','GET'])
def stu_degree():
    uname=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cr_student where uname=%s",(uname, ))
    data = mycursor.fetchone()
    if request.method=='POST':
        level=request.form['level']
        college=request.form['college']
        ug_degree=request.form['ug_degree']
        ug_percent=request.form['ug_percent']
        year=request.form['year']
        
        mycursor.execute("update cr_student set level=%s,college=%s,ug_degree=%s,ug_percent=%s,year=%s where uname=%s", (level,college,ug_degree,ug_percent,year,uname))
        mydb.commit()

       
        
        return redirect(url_for('stu_home'))
        
    
    return render_template('stu_degree.html',data=data)



@app.route('/add_cat',methods=['POST','GET'])
def add_cat():
    msg=""
    act=""
    mycursor = mydb.cursor()
    if request.method=='POST':
        category=request.form['category']
        
        mycursor.execute("SELECT count(*) FROM cr_category where category=%s",(category, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM cr_category")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO cr_category(id, category) VALUES (%s, %s)"
            val = (maxid, category)
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "record inserted.")
            msg='success'

        else:
            msg="fail"

    mycursor.execute("SELECT * FROM cr_category")
    data = mycursor.fetchall()

        
    return render_template('add_cat.html',msg=msg,data=data)

@app.route('/add_course',methods=['POST','GET'])
def add_course():
    msg=""
    act=""
    catid=request.args.get("catid")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM cr_category where id=%s",(catid,))
    dat = mycursor.fetchone()
    cat=dat[1]
    
    if request.method=='POST':
        course=request.form['course']
        detail=request.form['detail']
        

        mycursor.execute("SELECT max(id)+1 FROM cr_course")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO cr_course(id, catid,course,detail) VALUES (%s, %s,%s,%s)"
        val = (maxid, catid,course,detail)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit()            
        print(mycursor.rowcount, "record inserted.")
        msg='success'

    mycursor.execute("SELECT * FROM cr_course where catid=%s",(catid,))
    data = mycursor.fetchall()

        
    return render_template('add_course.html',msg=msg,data=data,cat=cat,catid=catid)

@app.route('/add_question',methods=['POST','GET'])
def add_question():
    msg=""
    act=""
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        question=request.form['question']
        option1=request.form['option1']
        option2=request.form['option2']
        option3=request.form['option3']
        option4=request.form['option4']
        

        mycursor.execute("SELECT max(id)+1 FROM cr_question")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO cr_question(id, question, option1, option2, option3, option4) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (maxid, question, option1, option2, option3, option4)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit()            
        print(mycursor.rowcount, "record inserted.")
        msg='success'

    mycursor.execute("SELECT * FROM cr_question")
    data = mycursor.fetchall()

        
    return render_template('add_question.html',msg=msg,data=data)


@app.route('/add_recommend',methods=['POST','GET'])
def add_recommend():
    msg=""
    act=""
    catid=request.args.get("catid")
    cid=request.args.get("cid")

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cr_category where id=%s",(catid,))
    dat = mycursor.fetchone()
    cat=dat[1]

    mycursor.execute("SELECT * FROM cr_course where id=%s",(cid,))
    dat2 = mycursor.fetchone()
    course=dat2[2]
    detail=dat2[3]
    
    if request.method=='POST':
        college_type=request.form['college_type']
        college=request.form['college']
        location=request.form['location']
        district=request.form['district']
        percent=request.form['percent']
        sem_fees=request.form['sem_fees']
      
        
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()


        mycursor.execute("SELECT max(id)+1 FROM cr_college")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO cr_college(id,college_type,college,location,district,cat,course,detail,percent,sem_fees) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,college_type,college,location,district,cat,course,detail,percent,sem_fees)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit()            
        
        msg='success'
   

    mycursor.execute("SELECT * FROM cr_college")
    data = mycursor.fetchall()

    return render_template('add_recommend.html',msg=msg,data=data,cat=cat,course=course,detail=detail)


@app.route('/stu_sport',methods=['POST','GET'])
def stu_sport():
    uname=""

    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cr_student where uname=%s",(uname, ))
    data = mycursor.fetchone()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        
        detail=request.form['detail']
        file = request.files['file']

        mycursor.execute("SELECT max(id)+1 FROM cr_skills")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        fn1="S"+str(maxid)+file.filename
        file.save(os.path.join("static/upload", fn1))
        sql = "INSERT INTO cr_skills(id, uname, stype, detail, filename, rdate) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (maxid, uname, "Sports",detail,fn1,rdate)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit() 
        return redirect(url_for('stu_home'))
        
    
    return render_template('stu_sport.html',data=data)

@app.route('/stu_extra',methods=['POST','GET'])
def stu_extra():
    uname=""

    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cr_student where uname=%s",(uname, ))
    data = mycursor.fetchone()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    if request.method=='POST':
        
        detail=request.form['detail']
        file = request.files['file']

        mycursor.execute("SELECT max(id)+1 FROM cr_skills")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        fn1="S"+str(maxid)+file.filename
        file.save(os.path.join("static/upload", fn1))
        sql = "INSERT INTO cr_skills(id, uname, stype, detail, filename, rdate) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (maxid,uname,"Skills", detail,fn1,rdate)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit() 
        return redirect(url_for('stu_home'))
        
    
    return render_template('stu_extra.html',data=data)

def unique(list1):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

@app.route('/stu_recommend',methods=['POST','GET'])
def stu_recommend():
    msg=""
    uname=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']

    
    qdata=[]
    act1=0
    act2=0
    st=""

    level1=""
    level2=""
    level=""
    recommend=""
    ug=""
    ug_degree=""
    sports_st=""
    st=""
    s1=""
    ug_st=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cr_student where uname=%s",(uname, ))
    data = mycursor.fetchone()


    mycursor.execute("SELECT * FROM cr_category")
    cat = mycursor.fetchall()

    mycursor.execute("SELECT distinct(district) FROM cr_college")
    drt = mycursor.fetchall()
    

    mycursor.execute("SELECT count(*) FROM cr_skills where stype='Sports' && uname=%s",(uname, ))
    spcnt = mycursor.fetchone()[0]
    if spcnt>0:
        sports_st="1"
    else:
        sports_st="2"

    mark1=float(data[12])
    mark2=float(data[15])
    hs_group=data[16]

    mark=(mark1+mark2)/2

    if mark>=80:
        level="1"
    else:
        level="2"

    subject="Mathematics"
    if subject in hs_group:
        level2="1"
    else:
        level2="2"

    if level1=="1" and level2=="1":
        level="Engineering"
    else:
        level="Arts"



    if act=="" or act is None:
        s=1
        st="1"
        mycursor.execute("update cr_question set answer=''")
        mydb.commit()
    else:
        act1=int(act)-1
        st="2"


    mycursor.execute("SELECT count(*) FROM cr_question")
    cnt = mycursor.fetchone()[0]

    tot=cnt-1
    if act1<=tot:
        mycursor.execute("SELECT * FROM cr_question limit %s,1",(act1,))
        qdata = mycursor.fetchall()

    else:
        return redirect(url_for('stu_recommend2'))
    
    if request.method=='POST':        
        value=request.form['value']

        print(act)
        mycursor.execute("update cr_question set answer=%s where id=%s",(value,act))
        mydb.commit()

        act2=int(act)+1
        act=str(act2)
        msg="ok"
            
        '''if act=="15":
            s1="1"
            mycursor.execute("update cr_recommend set extra_curricular=%s where uname=%s",(value,uname))
            mydb.commit()
            return redirect(url_for('stu_recommend',act='16'))

        mycursor.execute("SELECT * FROM cr_recommend where uname=%s",(uname, ))
        data2 = mycursor.fetchone()
            
            
        if act=="16":
            
            s=1            
            s1="2"
            filename = 'static/dataset/datafile.csv'
            data1 = pd.read_csv(filename, encoding='cp1252')
            for dat1 in data1.values:
                if ug_st=="1":
                    if dat1[14]==ug_degree and ug_percent>=65:
                        recommend=dat1[16]
                    elif dat1[14]==ug_degree and sports_st=="1":
                        recommend=dat1[16]
                    else:
                        recommend="1"
                else:
                    if int(dat1[4])>=90 and int(dat1[5])>=80 and int(dat1[6])>=80:
                        recommend=dat1[16]
                    else:
                        if dat1[3]==data2[5]:
                            if int(dat1[4])>=60 and int(dat1[5])>=50 and int(dat1[6])>=50:
                                recommend=dat1[16]
                            elif int(dat1[4])>=50 and sports_st=="1":
                                recommend=dat1[16]
                            else:
                                recommend="2"
                        else:
                            recommend="2"

        #Low average in UG
        #You have low average marks'''
                        

    return render_template('stu_recommend.html',msg=msg,act=act,data=data,level=level,recommend=recommend,s1=s1,cat=cat,qdata=qdata,st=st)

@app.route('/stu_recommend2',methods=['POST','GET'])
def stu_recommend2():
    uname=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cr_student where uname=%s",(uname, ))
    data = mycursor.fetchone()
    per=data[15]

    mycursor.execute("SELECT * FROM cr_category")
    cat = mycursor.fetchall()

    mycursor.execute("SELECT distinct(district) FROM cr_college")
    drt = mycursor.fetchall()


    mycursor.execute("SELECT * FROM cr_question")
    data2 = mycursor.fetchall()
    i=1
    x1=0
    x2=0
    x3=0
    x4=0
    for d2 in data2:
        #if i<=10:
        if d2[6]=="1":
            x1+=1
        if d2[6]=="2":
            x2+=1
        if d2[6]=="3":
            x3+=1
        if d2[6]=="4":
            x4+=1
                
        i+=1

    cat=''
    course=""
    detail=""
    if x1>x2 and x1>x3 and x1>x4:
        cat='1'
    elif x2>x3 and x2>x4:
        cat='2'
    elif x3>x4:
        cat='3'
    else:
        cat='3'

    mycursor.execute("SELECT * FROM cr_category where id=%s",(cat,))
    catt = mycursor.fetchone()

    mycursor.execute("SELECT * FROM cr_college where cat=%s && percent<=%s",(catt[1],per))
    dat11 = mycursor.fetchall()
    i=1
    for dat12 in dat11:
        if i==1:
            course=dat12[6]
            detail=dat12[7]
            break
        
        i+=1 
    
    
    mycursor.execute("SELECT * FROM cr_college where course=%s and detail=%s and percent<=%s",(course,detail,per))
    data1 = mycursor.fetchall()

    

    
    

    return render_template('stu_recommend2.html',act=act,data=data,data1=data1,course=course,detail=detail)
   

    
@app.route('/upload',methods=['POST','GET'])
def upload():
    msg=""
    if request.method=='POST':
        #cursor1 = mydb.cursor()
        #cursor1.execute("delete from cr_student")
        #mydb.commit()
        file = request.files['file']
        try:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                fn="datafile.csv"
                fn1 = secure_filename(fn)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn1))
                #return redirect(url_for('view_data'))
                filename2 = 'upload/datafile.csv'
                data1 = pd.read_csv(filename2, header=0)
                data2 = list(data1.values.flatten())
                data=[]
                i=0
                sd=len(data1)
                rows=len(data1.values)
                
                #print(str(sd)+" "+str(rows))
                for ss in data1.values:
                    mycursor = mydb.cursor()
                    #print(ss[1]+" "+ss[2]+" "+ss[3])
                    i+=1        
                    #print(str(i))
                    mycursor.execute("SELECT max(id)+1 FROM cr_student")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1

                    cgp=float(ss[13])/9.5
                    cgpa=round(cgp,2)
                    sql = "INSERT INTO cr_student(id, name, gender, dob, mobile, email, dept, year, uname, pass, address,  city, school1, mark1, school2, mark2, father, occu, jobtype, location, income, mother, occu2, jobtype2, location2, income2, mark, sport, extra_cur, skill, arrear, clear,cgpa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                    val = (maxid, ss[1], ss[2], ss[3], ss[4], ss[5], ss[6], ss[7], ss[8], ss[9], ss[10], ss[11], ss[12], ss[13], ss[14], ss[15], ss[16], ss[17], ss[18], ss[19], ss[20], ss[21], ss[22], ss[23], ss[24], ss[25], ss[26], ss[27], ss[28], ss[29], ss[30], ss[31],cgpa)
                    mycursor.execute(sql, val)
                    mydb.commit()
        
                msg="Uploaded Success"
        except:
            print("dd")
    return render_template('upload.html',msg=msg)

@app.route('/admin',methods=['POST','GET'])
def admin():
    uname=""

    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
   
    return render_template('admin.html')

@app.route('/load_data', methods=['GET', 'POST'])
def load_data():
    msg=""
    cnt=0
    data=[]
    rows=0
    cols=0

    '''df = pd.read_csv("static/upload/datafile.csv",encoding='cp1252')
    dat=df.head()
    data=[]
    rows=len(dat.values)
    for ss in dat.values:
        cnt=len(ss)
        data.append(ss)'''

        
    filename = 'static/dataset/datafile.csv'
    data1 = pd.read_csv(filename, header=0,encoding='cp1252')
    dat=data1.head(100)
    data2 = list(data1.values.flatten())
    
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    
    for ss in dat.values:
        cnt=len(ss)
        data.append(ss)
    cols=cnt
    
    return render_template('load_data.html',data=data,rows=rows,cols=cols)


            
@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    msg=""
    mem=0
    cnt=0
    cols=0
    rows=0
    rowsn=0
    nullcount=0
    filename = 'static/dataset/datafile.csv'
    data1 = pd.read_csv(filename, encoding='cp1252')
    data2 = list(data1.values.flatten())
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data1)
    #rows=len(data1.values)
    
    #print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        i=0
        x=0
        while i<cnt:
            if pd.isnull(ss[i]):
                nullcount+=1
                x+=1
            i+=1
        if x>0:
            rowsn+=1
        

    i=0
    while i<cnt:
        j=0
        x=0
        y=0
        for rr in data1.values:
            dt=type(rr[i])
            
            j+=1
        
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    rows=rows-rowsn
    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))


    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    print(data)
    cols=cnt
    mem=float(rows)*0.75
    

    #if request.method=='POST':
    #    return redirect(url_for('feature_ext'))
    
    return render_template('preprocess.html',data=data, msg=msg, rows=rows, cols=cols,nullcount=nullcount, dtype=dtype, mem=mem)



@app.route('/feature', methods=['GET', 'POST'])
def feature():
    msg=""
    cnt=0
    data=[]
    rows=0
    rowsn=0
    nullcount=0
    cols=0

    '''df = pd.read_csv("static/upload/datafile.csv",encoding='cp1252')
    dat=df.head()
    data=[]
    rows=len(dat.values)
    for ss in dat.values:
        cnt=len(ss)
        data.append(ss)'''

        
    filename = 'static/dataset/datafile.csv'
    data1 = pd.read_csv(filename, header=0,encoding='cp1252')
    dat=data1.head(100)
    data2 = list(data1.values.flatten())
    
    i=0
    sd=len(data1)
    #rows=len(data1.values)
    
    v1=0
    v2=0
    v3=0
    n=0
    int_subj=[]
    com_skill=[]
    for ss in dat.values:
        cnt=len(ss)
        i=0
        x=0
        while i<cnt:
            if pd.isnull(ss[i]):
                nullcount+=1
                x+=1
            i+=1
        if x>0:
            rowsn+=1
        else:

            v1+=int(ss[4])
            v2+=int(ss[5])
            v3+=int(ss[6])
            int_subj.append(ss[3])
            com_skill.append(ss[7])
            n+=1
            data.append(ss)
    cols=cnt

    v11=v1/n
    c1=round(v11,2)

    v22=v2/n
    c2=round(v22,2)

    v33=v3/n
    c3=round(v33,2)

    #####
    val_subj=[]
    nj2=0
    interest_subj=unique(int_subj)
    for ij in interest_subj:
        nj=0
        for ss in dat.values:
            if ss[3]==ij:
                nj+=1

        val_subj.append(nj)
        
    val_subj.sort()        
    nj2=val_subj[-1]+10
    #####
    val_skill=[]
    nj3=0
    comm_skill=unique(com_skill)
    for ij1 in comm_skill:
        ns=0
        for ss in dat.values:
            if ss[7]==ij1:
                ns+=1

        val_skill.append(ns)
        
    val_skill.sort()        
    nj3=val_skill[-1]+10
    #################
    val=[c1,c2,c3]
    doc = ['Maths','Physics','Chemistry'] #list(data.keys())
    values = val #list(data.values())
    
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    #cc=['red','green']
    plt.bar(doc, values, width = 0.6)
 

    plt.ylim((1,100))
    plt.xlabel("Subject")
    plt.ylabel("Percentage")
    plt.title("")

    rr=randint(100,999)
    fn="graph1.png"
    #plt.xticks(rotation=5,size=20)
    plt.savefig('static/'+fn)
    
    plt.close()
    #plt.clf()
    #################
    val=val_subj
    doc = interest_subj #list(data.keys())
    values = val #list(data.values())
    
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    #cc=['red','green']
    plt.bar(doc, values, width = 0.6)
 

    plt.ylim((1,nj2))
    plt.xlabel("Interested Subject")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="graph2.png"
    #plt.xticks(rotation=5,size=20)
    plt.savefig('static/'+fn)
    
    plt.close()
    #plt.clf()
    #################
    val=val_skill
    doc = comm_skill #list(data.keys())
    values = val #list(data.values())
    
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    #cc=['red','green']
    plt.bar(doc, values, width = 0.6)
 

    plt.ylim((1,nj3))
    plt.xlabel("Level of Communication Skills")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="graph3.png"
    #plt.xticks(rotation=5,size=20)
    plt.savefig('static/'+fn)
    
    plt.close()
    #plt.clf()
    ##########################
    #acc########################################
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(94,98)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(94,98)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[5,26,45,60,72]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy %")
    
    fn="graph4.png"
    #plt.savefig('static/'+fn)
    plt.close()
    #######################################################
    #graph4
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,4)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(1,4)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[5,26,45,60,72]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Model loss")
    
    fn="graph5.png"
    #plt.savefig('static/'+fn)
    plt.close()
    ############################



    
    return render_template('feature.html',data=data,rows=rows,cols=cols)

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    cnt=0
    data=[]
    rows=0
    rowsn=0
    nullcount=0
    cols=0

    '''df = pd.read_csv("static/upload/datafile.csv",encoding='cp1252')
    dat=df.head()
    data=[]
    rows=len(dat.values)
    for ss in dat.values:
        cnt=len(ss)
        data.append(ss)'''

    ##Decision Tree Algorithm
    filename = 'static/dataset/datafile.csv'
    data1 = pd.read_csv(filename, header=0,encoding='cp1252')
    dat=data1.head(100)
    data2 = list(data1.values.flatten())
    from sklearn import preprocessing
    #le_status = preprocessing.LabelEncoder()
    #le_status.fit(['status','1'])
    #X[:,1] = le_status.transform(X[:,1])
    df = pd.read_csv(filename, header=0,encoding='cp1252')
    df = df.fillna(df.mean()) # updates the df
    df.corr()

    x = df.iloc[:,0:-1].values
    y = df.iloc[:,-1:].values

    x_train, x_test, y_train, y_test = train_test_split(x, y)

    print(x_train)
    print(y_train)

    print(len(x_train),len(x_test))

    dt_regressor = DecisionTreeRegressor()
    #dt_regressor.fit(x_train, y_train)

    #y_pred_dt = dt_regressor.predict(x_test)

    #print(r2_score(y_test, y_pred_dt))
    #print(mse(y_test, y_pred_dt)**0.5)
    #
    
    i=0
    sd=len(data1)
    #rows=len(data1.values)
    
    
    for ss in dat.values:
        cnt=len(ss)
        i=0
        x=0
        while i<cnt:
            if pd.isnull(ss[i]):
                nullcount+=1
                x+=1
            i+=1
        if x>0:
            rowsn+=1
        else:
            data.append(ss)
    cols=cnt
    
    return render_template('classify.html',data=data,rows=rows,cols=cols)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
