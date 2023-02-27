from flask import Flask, render_template, request, session, jsonify, redirect
from DBConnection import Db
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

app = Flask(__name__)
app.secret_key="a"

#=====================================================Reg Form=========================================================#

@app.route('/regindex')
def regindex():
    return render_template("register_index.html")

@app.route('/form1_post', methods=['post'])
def form1_post():
    c=Db()
    fname=request.form['txt_fname']
    lname=request.form['txt_lname']
    gender = request.form['gender']
    Email = request.form['txt_email']
    Contact= request.form['txt_phone']
    password= request.form['txt_psw']
    cpassword = request.form['txt_psw1']

    qry="insert into login(username,password,usertype) values('"+fname+"','"+password+"','user')"
    lid=c.insert(qry)
    qry1="insert into user(firstname,lastname,gender,email,contact,loginid) values('"+fname+"','"+lname+"','"+gender+"','"+Email+"','"+Contact+"','"+str(lid)+"')"
    c.insert(qry1)

    # email = request.form['eml']
    # n_pwd = request.form['npwd']
    # password = str(n_pwd)
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("visualiseralgorithm@gmail.com", "PwoliprojecT")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from ALGORITHM VISUALIZER"
    msg['From'] = "visualiseralgorithm@gmail.com"
    msg['To'] = Email
    msg['Subject'] = "Registration"
    body = "You our dear user has registered successfully to our website "
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    return render_template("login_index.html")

#===================================================login section======================================================#

@app.route('/')
def loginindex():
    return  render_template("login_index.html")

@app.route('/loginpost',methods=['post'])
def loginpost():
    uname=request.form['uname']
    password=request.form['pwd']
    c=Db()
    qry="select * from login where username='"+uname+"' and password='"+password+"'"
    res=c.selectOne(qry)
    print(qry)
    if res is not None:
        type=res['usertype']
        session["lid"] = res["loginid"]
        session["kk"] = "user"
        if type=="admin":
            return render_template("admin/adminhomepage.html")
        else:
            return render_template("user/user_index.html")
    else:
        return "<Script>alert('Incorrect Password or user name');window.location='/'</script>"

#------------------------------------Forget Password----------------------------

@app.route('/fgt_pwd')
def fgt_pwd():
    return render_template("forget_pwd.html")

@app.route('/forgotpwd',methods=['post'])
def fgtpwd_post():
    email = request.form['eml']
    n_pwd=request.form['npwd']
    password = str(n_pwd)
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("visualiseralgorithm@gmail.com", "PwoliprojecT")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from ALGORITHM VISUALIZER"
    msg['From'] = "visualiseralgorithm@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Reset Your Password"
    body = "Your password has been changed . You Can Now login using your password - " + str(password)
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    qry="select * from user where email='"+email+"'"
    db=Db()
    res=db.selectOne(qry)

    qr1="update login set password='"+n_pwd+"' where loginid='"+str(res["loginid"])+"'"
    db.update(qr1)
    return '''<script>alert('Password changed successfully');window.location='/'</script>'''

#==================================================ADMIN SECTION=======================================================#

#------------------------------------Admin Home------------------

@app.route('/ah')
def ah():
    return render_template("admin/adminhomepage.html")

#------------------------------------View User-------------------

@app.route('/viewusr')
def vusr():
    c=Db()
    qry="select * from user"
    res=c.select(qry)
    return  render_template("admin/Viewuser.html",data=res)


@app.route('/viewusrBYSEARCH',methods=['post'])
def vusrsea():
    sname=request.form['Searchbar']
    c = Db()
    qry = "select * from user where firstname LIKE '%"+sname+"%'"
    res = c.select(qry)
    return render_template("admin/Viewuser.html", data=res)

#---------------------Feedback------------------------------

@app.route('/viewfdbk')
def vfdbk():
    c=Db()
    qry="select user.*,feedback.* from user,feedback where user.loginid=feedback.user_loginid"
    res=c.select(qry)
    return  render_template("admin/Viewfeedback.html",data=res)

@app.route('/viewfdbk1',methods=['post'])
def vfdbk1():
    from_date=request.form['dateFrom']
    to_date=request.form['dateTo']
    c=Db()
    qry="select user.*,feedback.* from user,feedback where user.loginid=feedback.user_loginid and feedback.date BETWEEN '"+from_date+"'and'"+to_date+"'"
    res=c.select(qry)
    print(qry)
    return  render_template("admin/Viewfeedback.html",data=res)


@app.route('/fdbkrpy/<kk>')
def fdbr(kk):
    session["fid"]=kk
    return  render_template("admin/Feedbackreply.html")


@app.route('/fdbkrpypost', methods=['post'])
def fdbr1():
    feedback_reply=request.form['Reply']
    c=Db()
    qry="update feedback set reply='"+feedback_reply+"',feedback_status='replied',reply_date=curdate() where  fid='"+session["fid"]+"'"
    c.update(qry)
    return render_template("admin/Feedbackreply.html")

#---------------------------------admin home------------------------

@app.route('/adminhome')
def adminhome():
    return render_template("admin/adminhomepage.html")

@app.route('/adminhome1')
def adminhom():
    return render_template("admin/admin_index.html")

#---------------------------------Doubt Clearing---------------------

@app.route('/doubtclr1')
def doubtclr1():
    # print("=============================")
    c=Db()
    qry="select doubt.*,user.* from user,doubt where doubt.user_loginid=user.loginid and doubt.answer='pending'"
    print(qry)
    res=c.select(qry)
    print(res)
    return render_template("admin/View_Doubt.html", data=res)

@app.route('/dbtclrply/<m>')
def doubtclrr(m):
    session['dbtid']=m
    return  render_template("admin/Doubtclearencereply.html")

@app.route('/dbtclrpo',methods=['post'])
def dbtclrpo1():
    ans=request.form['Reply']
    c=Db()
    qry="update doubt set answer='"+ans+"' where Did='"+str(session['dbtid'])+"'"
    c.update(qry)
    return render_template("admin/Doubtclearencereply.html")

#------------------------------------Change Password---------------------------

@app.route('/changepd')
def chpd():
    return render_template("changepwd.html")

@app.route('/changepwd')
def chpwd():
    return render_template("admin/changepwd.html")

@app.route('/changepwdpost',methods=['post'])
def changepwdpost():
    lid=session["lid"]
    opass=request.form['o']
    npass=request.form['n']
    cpass=request.form['c']
    if npass==cpass:
        qry="select * from login where loginid='"+str(lid)+"' and password='"+opass+"'"
        c=Db()
        res=c.selectOne(qry)
        if res is not None:
            qry="update login set password='"+cpass+"' where loginid='"+str(lid)+"'"
            c.update(qry)
            return render_template("login_index.html")
        else:
            return 'invalid information'
    else:
        return 'invalid information'

    return render_template("admin/changepwd.html")

#==================================================User Section========================================================#

#----------------------------------User Home---------------------

@app.route('/userhome')
def userhome():

    if session["kk"]=="public":
        return redirect("/public")


    return render_template('user/user_index.html')

#---------------------------------Send Feedback------------------

@app.route('/userindex')
def userindex():
    return render_template('userfeedback.html')

@app.route('/userindexpost',methods=['post'])
def userindexpost():
    c=Db()
    x=session["lid"]
    feedback=request.form['feed']
    qry="insert into feedback(feedback,date,user_loginid) values('"+feedback+"',curdate(),'"+str(x)+"')"
    res=c.insert(qry)
    print(qry)
    text1="thanks"
    return render_template("user/feedback.html")

#---------------------------------View Feedback Replies------------------

@app.route('/freply1')
def feedback1():
    c=Db()
    qry = "select feedback.* from feedback where feedback.user_loginid='" + str(session['lid']) + "' and feedback_status='replied'"
    # qry="select feedback.*,user.* from user,feedback where feedback.user_loginid=user.loginid and feedback.feedback_status='replied'"
    print(qry)
    res=c.select(qry)
    print(res)
    return render_template("user/userfeedbackreply.html", res=res)

#===================================================User Algorithm=====================================================#

#-------------------------------------------------------Sorting---------------------------------------------------------

@app.route('/sort')
def sort():
    return render_template("Sort/Sort_container.html")

#----------------------------Bubble----------------------------------

@app.route('/bubble')
def bubble():
    return render_template("Sort/bubble.html")

#------------------------Selection----------------------------------

@app.route('/selection')
def selection():
    return render_template("Sort/selection.html")

#------------------------Insertion----------------------------------

@app.route('/insertion')
def insertion():
    return render_template("Sort/insertion.html")

#-----------------------------Merge----------------------------------

@app.route('/merge')
def merge():
    return render_template("Sort/merge.html")

#------------------------------Quick----------------------------------

@app.route('/quick')
def quick():
    return render_template("Sort/quick.html")

#-----------------------------------------------------Searching---------------------------------------------------------

@app.route('/search')
def search():
    return render_template("Searching/Search_container.html")

#------------------------Binary----------------------------------

@app.route('/binary')
def binary():
    return render_template("Searching/binary.html")

#------------------------Linear----------------------------------

@app.route('/linear')
def linear():
    return render_template("Searching/Linear.html")

#------------------------Jump-------------------------------------

@app.route('/jump')
def jump():
    return render_template("Searching/jump.html")

#------------------------Interpolation------------------------------

@app.route('/inter')
def inter():
    return render_template("Searching/interpolation.html")

#------------------------------------------------------Graph------------------------------------------------------------

@app.route('/graph')
def graph():
    return render_template("Graph/Graph_container.html")

#------------------------BFS------------------------------

@app.route('/bfs')
def bfs():
    return render_template("Graph/bfs.html")

#------------------------DFS------------------------------

@app.route('/dfs')
def dfs():
    return render_template("Graph/dfs.html")

#---------------------------------------------------Data_Structure------------------------------------------------------

@app.route('/ds')
def ds():
    return render_template("Data_Structure/DS_container.html")

#------------------------Queue----------------------------------------

@app.route('/queue')
def queue():
    return render_template("Data_Structure/queue.html")

#------------------------Stack----------------------------------------

@app.route('/stack')
def stack():
    return render_template("Data_Structure/stack.html")

#-------------------------Linked list----------------------------------

@app.route('/linkedlist')
def linkedlist():
    return render_template("Data_Structure/linked_list.html")

#-------------------------------------------------------Doubts----------------------------------------------------------

@app.route('/dbs')
def dbs():
    c=Db()
    qry = "select doubt.* from doubt where doubt.user_loginid='"+str(session['lid'])+"'"
    print(qry)
    res = c.select(qry)

    return render_template("user/doubt.html", res=res)

@app.route('/dbspost',methods=['post'])
def dbspost():
    ds=request.form['Reply']
    c=Db()
    qry="insert into doubt(date,doubt,user_loginid,answer)VALUES (curdate(),'"+ds+"','"+str(session['lid'])+"','pending')"
    res=c.insert(qry)
    return  "<Script>alert('Doubt added Successfully');window.location='/dbs'</script>"

#--------------------------------------------------------Quiz-----------------------------------------------------------

@app.route('/quiz')
def quiz():
    return render_template("user/quiz.html")

#=========================================================Public========================================================#

@app.route('/public')
def public():
    session["kk"]="public"
    return render_template("Public/public.html")

#=========================================================Info========================================================#

@app.route('/info')
def info():
    return render_template("user/info.html")

#======================================================================================================================#
#======================================================================================================================#

if __name__ == '__main__':
    app.run(debug=True,port=5000)