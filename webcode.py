import os
import random
import time


import cv2
from flask import *
from werkzeug.utils import secure_filename
import pymysql


fn=''
app=Flask(__name__)
con = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='attendance_face')
cmd = con.cursor()
app.secret_key="qwe23"


import functools
def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return index()
        return func()
    return secure_function



@app.route('/logout')
def logout():
    print("lllllllllllllllllllll")
    session.pop('lid', None)

    return redirect(url_for('user'))
def get_user_role(user_id):
    cmd.execute("SELECT usertype FROM login WHERE id = %s", (user_id,))
    result = cmd.fetchone()
    if result:
        return result[0]
    else:
        return None


@app.route('/')
def index():
    if 'lid' in session:
        role = get_user_role(session['lid'])
        if role == "admin":
            return redirect('/adminhome')
        elif role == "teacher":
            return redirect('/teacherhome')
        elif role == "student":
            return redirect('/studenthome')
    else:
        return redirect(url_for('user'))

@app.route('/login', methods=["GET", "POST"])
def user():
    if 'lid' in session:
        return redirect(url_for('index'))
    if request.method == "POST":
        user = request.form['textfield']
        passw = request.form['textfield2']
        cmd.execute("select*from login where username='"+user+"' and password='"+passw+"'")
        result = cmd.fetchone()
        if result is None:
            return '''<script>alert("invalid username and password");window.location='/login'</script>'''
        else:
            session['lid'] = result[0]
        if 'lid' in session:
            role = get_user_role(session['lid'])
            if role == "admin":
                return redirect('/adminhome')
            elif role == "teacher":
                return redirect('/teacherhome')
            elif role == "student":
                return redirect('/studenthome')
        else:
            return redirect(url_for('user'))

    response = make_response(render_template('LOGIN.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


# @app.route('/logincode',methods=['post','get'])
# def logincode():
#     if 'lid' in session:
#         return redirect(url_for('main'))
#     if request.method == "POST":
#
#         uname=request.form['textfield']
#         pswd=request.form['textfield2']
#         cmd.execute("select*from login where username='"+uname+"' and password='"+pswd+"'")
#         res=cmd.fetchone()
#         if res is None:
#             return '''<script>alert("Invalid user name or password");window.location='/'</script>'''
#         else:
#             session['lid']=res[0]
#             if res[3]=="admin":
#                 return '''<script>window.location='/adminhome'</script>'''
#             elif res[3]=="teacher":
#                 return '''<script>alert("Welcome");window.location='/teacherhome'</script>'''
#             elif res[3]=="student":
#                 return '''<script>alert("Welcome");window.location='/studenthome'</script>'''
#
#     response = make_response(render_template('login.html'))
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response.headers['Expires'] = 0
#     response.headers['Pragma'] = 'no-cache'
#     return response


@app.route('/adminhome',methods=['post','get'])
@login_required
def adminhome():
    get_user_role(session['lid'])

    return render_template('admin/base.html')


@app.route('/teacherhome',methods=['post','get'])
@login_required

def teacherhome():
    get_user_role(session['lid'])

    try:
        ab=0
        cmd.execute("SELECT `department` FROM `teacher` WHERE `lid`='"+str(session['lid'])+"'")
        res=cmd.fetchone()
        dept=res[0]
        session['deptnm']=dept
        cmd.execute("SELECT studentlid, SUM(distinct_attendance_count) AS total_distinct_attendance_count FROM (SELECT studentlid, DATE, COUNT(DISTINCT attendance) AS distinct_attendance_count FROM attendence  WHERE `attendance`=0 and `attendence`.`department`='"+str(dept)+"' and `attendence`.`status`='notify' GROUP BY studentlid, DATE HAVING COUNT(attendance) = 7) AS subquery GROUP BY studentlid HAVING SUM(distinct_attendance_count) >=2")
        res=cmd.fetchall()
        print(res)
        j=0
        stid=[]
        for i in res:
            stid.append(i[0])
            j=j+1

        return render_template("staff/base.html",j=j)
    except Exception as e:
        return redirect('/')


@app.route('/studenthome',methods=['post','get'])
@login_required
def studenthome():
    get_user_role(session['lid'])

    return render_template("student/student-home.html")


#admin

@app.route('/viewstaff',methods=['post','get'])
@login_required
def viewstaff():
    cmd.execute("select * from teacher")
    res=cmd.fetchall()
    print(res)
    return render_template("admin/stafflist.html",val=res)

@app.route('/deletestaff',methods=['post','get'])
@login_required
def deletestaff():
    tlid=request.args.get('lid')
    cmd.execute("delete from teacher where lid='"+tlid+"' ")
    con.commit()
    return '''<script>alert("Successfully Deleted");window.location='/viewstaff'</script>'''

@app.route('/dellv',methods=['post','get'])
@login_required
def dellv():
    id=request.args.get('id')
    cmd.execute("delete from `leave` where lvid='"+id+"' ")
    con.commit()
    return '''<script>alert("Successfully Deleted");window.location='/leavereq'</script>'''

@app.route('/editstaff',methods=['post','get'])
@login_required
def editstaff():
    tlid=request.args.get('lid')
    session['tlid']=tlid
    cmd.execute("select * from teacher where lid='"+tlid+"'")
    res=cmd.fetchone()
    return render_template("admin/staff_editform.html",i=res)



@app.route('/editlv',methods=['post','get'])
@login_required
def editlv():
    id=request.args.get('id')
    session['lvid']=id
    cmd.execute("select * from `leave` where lvid='"+id+"'")
    res=cmd.fetchone()
    return render_template("student/student-leaveedit.html",i=res)

@app.route('/updatestaff',methods=['post','get'])
@login_required
def updatestaff():
    try:
        print("try")
        fname=request.form['text1']
        code=request.form['text2']
        address=request.form['text3']
        phone=request.form['text4']
        email=request.form['text5']
        qualification=request.form['text6']
        dept=request.form['select']
        img = request.files['files']
        name = secure_filename(img.filename)

        import time
        req = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        img.save(os.path.join('./static/staffphoto', req))
        cmd.execute("update teacher set name='"+fname+"',teacher_code='"+code+"',address='"+address+"',phone='"+phone+"',email='"+email+"',qualification='"+qualification+"',department='"+dept+"',photo='"+req+"' where lid='"+str(session['tlid'])+"'")
        con.commit()
        return '''<script>alert("Successfully Updated");window.location='/viewstaff'</script>'''
    except Exception as e:
        print(e)
        name = request.form['text1']
        code = request.form['text2']
        address = request.form['text3']
        phone = request.form['text4']
        email = request.form['text5']
        qualification = request.form['text6']
        dept = request.form['select']
        cmd.execute(
            "update teacher set name='" + name + "',teacher_code='" + code + "',address='" + address + "',phone='" + phone + "',email='" + email + "',qualification='" + qualification + "',department='" + dept + "'where lid='" + str(
                session['tlid']) + "'")
        con.commit()
        return '''<script>alert("Successfully Updated");window.location='/viewstaff'</script>'''







@app.route('/addstaff',methods=['post','get'])
@login_required
def addstaff():
    return render_template("admin/staff_form.html")
@app.route('/staffreg',methods=['post','get'])
@login_required
def staffreg():
    try:
        fname=request.form['text1']
        code=request.form['text2']
        address=request.form['text3']
        phone=request.form['text4']
        email=request.form['text5']
        qualification=request.form['text6']
        dept=request.form['select']

        img = request.files['files']
        name = secure_filename(img.filename)

        import time
        req = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        img.save(os.path.join('./static/staffphoto', req))
        uname=request.form['uname']
        password=request.form['password']
        cnfpassword=request.form['cnfpassword']
        if password==cnfpassword:
            cmd.execute("insert into login values(null,'"+uname+"','"+password+"','teacher')")
            id=con.insert_id()
            cmd.execute("insert into teacher values(null,'"+str(id)+"','"+fname+"','"+code+"','"+address+"','"+phone+"','"+email+"','"+qualification+"','"+dept+"','"+req+"' )")
            con.commit()
            return '''<script>alert("Successfully Added");window.location='/viewstaff'</script>'''
        else:
            return '''<script>alert("Password Mismatch.......!");window.location='/addstaff'</script>'''
    except Exception as e:
        print(e)
        return '''<script>alert("Error.......!");window.location='/addstaff'</script>'''


@app.route('/deptsearch',methods=['post','get'])
@login_required
def deptsearch():
    dept=request.form['select']
    print("select * from teacher where department='"+dept+"'")
    cmd.execute("select * from teacher where department='"+dept+"'")
    res=cmd.fetchall()
    print(res)
    return render_template("admin/stafflist.html",val=res,dept=dept)


@app.route('/viewstudent',methods=['post','get'])
@login_required
def viewstudent():
    cmd.execute("select * from student")
    res=cmd.fetchall()
    print(res)
    return render_template("admin/studentlist.html",val=res)

@app.route('/deptsearch1',methods=['post','get'])
@login_required
def deptsearch1():
    dept=request.form['selects']
    sem=request.form['select1']

    cmd.execute("select * from student where department='"+dept+"' and semester='"+sem+"'")
    res=cmd.fetchall()
    print(res)
    return render_template("admin/studentlist.html",val=res,dept=dept,sem=sem)






#tutor
@app.route('/viewtutor',methods=['post','get'])
@login_required
def viewtutor():
    return render_template("admin/tutor.html")

@app.route('/addtutor',methods=['post','get'])
@login_required
def addtutor():
    return render_template("admin/addtutor.html")


@app.route('/tutor',methods=['post','get'])
@login_required
def tutor():
    dept=request.form['select']
    cmd.execute("SELECT `teacher`.`name`,`teacher`.`teacher_code`,`teacher`.`photo`,`tutor`.*FROM `tutor` JOIN `teacher` ON `teacher`.`lid`=`tutor`.`staff_lid` WHERE `tutor`.`department`='"+dept+"'")
    s=cmd.fetchall()
    print(s)
    return render_template("admin/tutor.html",val=s,dept=dept)

@app.route('/deletetutor',methods=['post','get'])
@login_required
def deletetutor():
    id=request.args.get('lid')
    cmd.execute("delete from tutor where tid='"+id+"' ")
    con.commit()
    return '''<script>alert("Successfully Deleted");window.location='/viewtutor'</script>'''



@app.route('/getstaff',methods=['get','post'])
def getstaff():

    dept = request.form['dept']
    print(dept)
    cmd.execute("SELECT `lid`,`name`,`teacher_code` FROM `teacher` WHERE `department`='"+dept+"'")
    s=cmd.fetchall()
    print(s)

    lis=[0,'select']
    for r in s:
        lis.append(r[0])
        lis.append(r[1]+"(CODE:"+str(r[2])+")")
    print(lis)
    resp = make_response(jsonify(lis))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp



@app.route('/tutors',methods=['post','get'])
@login_required
def tutors():
    dept=request.form['selects']
    stafid=request.form['select']
    sem=request.form['select1']
    divi=request.form['select3']
    cmd.execute("insert into tutor values(null,'"+str(stafid)+"','"+dept+"','"+sem+"','"+divi+"')")
    con.commit()
    return '''<script>alert("Successfully Added");window.location='/viewtutor'</script>'''

#subject

@app.route('/viewsubject',methods=['post','get'])
@login_required
def viewsubject():

    return render_template("admin/subjectView.html")



@app.route('/viewsubjects',methods=['post','get'])
@login_required
def viewsubjects():
    dept=request.form['select']
    sem=request.form['select1']
    cmd.execute("SELECT `subject`.*,`teacher`.`name`,`teacher`.`teacher_code` FROM `teacher` JOIN `subject` ON `subject`.`staff_lid`=`teacher`.`lid` WHERE `subject`.`department`='"+dept+"' AND `subject`.`semester`='"+sem+"'")
    s=cmd.fetchall()
    print(s)
    return render_template("admin/subjectView.html",val=s,dept=dept,sem=sem)

@app.route('/deletesubject',methods=['post','get'])
@login_required
def deletesubject():
    id=request.args.get('lid')
    cmd.execute("delete from subject where sid='"+id+"' ")
    con.commit()
    return '''<script>alert("Successfully Deleted");window.location='/viewsubject'</script>'''



# @app.route('/editsubject',methods=['post','get'])
# @login_required
# def editsubject():
#     id=request.args.get('lid')
#     session['subid']=id
#     cmd.execute("select * from subject where sid='"+id+"'")
#     res=cmd.fetchone()
#     return render_template("admin/editsubject.html",i=res)
#
#
# @app.route('/updatesubject',methods=['post','get'])
# @login_required
# def updatesubject():
#     subject=request.form['subject']
#     code=request.form['code']
#     dept=request.form['dept']
#     sem=request.form['sem']
#     staffid=request.form['staffid']
#     cmd.execute("update subject set subject='"+subject+"',code='"+code+"',department='"+dept+"',semester='"+sem+"',staff_lid='"+staffid+"' where sid='"+str(session['subid'])+"'")
#     con.commit()
#     return '''<script>alert("Successfully updated");window.location='/viewsubject'</script>'''

@app.route('/addubject',methods=['post','get'])
@login_required
def addubject():
    return render_template("admin/SubjectRegister.html")

@app.route('/subjectreg',methods=['post','get'])
@login_required
def subjectreg():
    subject=request.form['text2']
    code=request.form['text1']
    dept=request.form['department']
    sem=request.form['Semester']
    staffid=request.form['Staff']
    cmd.execute("insert into subject values(null,'"+subject+"','"+code+"','"+dept+"','"+sem+"','"+staffid+"') ")
    con.commit()
    return '''<script>alert("Successfully Registred");window.location='/viewsubject'</script>'''

@app.route('/deletetimetable',methods=['post','get'])
@login_required
def deletetimetable():
    tlid=request.args.get('lid')
    cmd.execute("delete from timetable where tid='"+tlid+"' ")
    con.commit()
    return '''<script>alert("Successfully Deleted");window.location='/viewtimtable'</script>'''


# @app.route('/viewattendances',methods=['post','get'])
# @login_required
# def viewattendances():
#     type=request.form['submit']
#     if type=="view":
#         sem=request.form['sem']
#         session['sem']=sem
#         Division=request.form['divi']
#         session['division']=Division
#         date=request.form['date']
#         session['date']=date
#         hour=request.form['hour']
#         session['hour']=hour
#         dept=request.form['dept']
#         session['dept']=dept
#         # cmd.execute("select department from teacher where tlid='"+str(session['lid'])+"'")
#         # req=cmd.fetchone()
#         # dept=req[0]
#         # print(dept)
#         cmd.execute("SELECT `attendence`.`attendance`,`attendence`.`hour`,`student`.`regno`,`student`.`lid` FROM `attendence`  JOIN `student` ON `student`.`lid`=`attendence`.`studentlid` WHERE attendence.`date`='"+date+"' AND attendence.`hour`='"+hour+"' AND attendence.`division`='"+Division+"' AND attendence.`sem`='"+sem+"' AND attendence.`department`='"+str(dept)+"'")
#         res=cmd.fetchall()
#         print(res)
#         if len(res)==0:
#             return '''<script>alert("No Data");window.location='/viewattendance'</script>'''
#         else:
#
#             return render_template("admin/attendance.html",val=res,len=len(res))
#     else:
#         print("okkkkkkkkkkkkkk")
#         cmd.execute("SELECT `attendence`.`attendance`,`attendence`.`hour`,`student`.`regno`,`student`.`lid` FROM `attendence`  JOIN `student` ON `student`.`lid`=`attendence`.`studentlid` WHERE attendence.`date`='" + str(session['date']) + "' AND attendence.`hour`='" + str(session['hour']) + "' AND attendence.`division`='" + str(session['division']) + "' AND attendence.`sem`='" + str(session['sem']) + "' AND attendence.`department`='" + str(session['dept']) + "'")
#         res = cmd.fetchall()
#         print(res)
#         return render_template("admin/attendance1.html",val=res)
@app.route('/deletestudent',methods=['post','get'])
@login_required
def deletestudent():
    tlid=request.args.get('lid')
    cmd.execute("delete from student where lid='"+tlid+"' ")
    con.commit()
    return '''<script>alert("Successfully Deleted");window.location='/viewstudent'</script>'''


@app.route('/editstudent',methods=['post','get'])
@login_required
def editstudent():
    tlid=request.args.get('lid')
    session['slid']=tlid
    cmd.execute("select * from student where lid='"+tlid+"'")
    res=cmd.fetchone()
    return render_template("admin/student_editform.html",i=res)


@app.route('/updatestudent',methods=['post','get'])
@login_required
def updatestudent():
    try:
        fname=request.form['text1']
        regno=request.form['text2']
        address=request.form['text3']
        phone=request.form['text4']
        email=request.form['text5']

        dob=request.form['text6']
        dept=request.form['select']
        Semester=request.form['select1']
        division=request.form['select3']
        img = request.files['files']
        name = secure_filename(img.filename)

        import time
        req = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        img.save(os.path.join('static/images', req))
        print("update student set name='"+fname+"',regno='"+regno+"',address='"+address+"',phone='"+phone+"',email='"+email+"',dob='"+dob+"',department='"+dept+"', semester='"+Semester+"',division='"+division+"',photo='"+req+"' where lid='"+str(session['slid'])+"'")
        cmd.execute("update student set name='"+fname+"',regno='"+regno+"',address='"+address+"',phone='"+phone+"',email='"+email+"',dob='"+dob+"',department='"+dept+"', semester='"+Semester+"',division='"+division+"',photo='"+req+"' where lid='"+str(session['slid'])+"'")
        con.commit()
        return '''<script>alert("Successfully Updated");window.location='/viewstudent'</script>'''
    except Exception as e:
        print(e)
        fname = request.form['text1']
        regno = request.form['text2']
        address = request.form['text3']
        phone = request.form['text4']
        email = request.form['text5']

        dob = request.form['text6']
        dept = request.form['select']
        Semester = request.form['select1']
        division = request.form['select3']
        cmd.execute(
            "update student set name='" + fname + "',regno='" + regno + "',address='" + address + "',phone='" + phone + "',email='" + email + "',dob='" + dob + "',department='" + dept + "', semester='" + Semester + "',division='" + division + "' where lid='" + str(
                session['slid']) + "'")
        con.commit()

        return '''<script>alert("Successfully Updated");window.location='/viewstudent'</script>'''

@app.route('/staffupdateattendances', methods=['post', 'get'])
@login_required
def staffupdateattendances():
        student = request.form.getlist('sid')
        att = request.form.getlist('att')
        lngth = len(att)
        for i in range(lngth):
            print("update attendence set attendance='" + str(att[i]) + "' where studentlid='" + str(
                student[i]) + "' and hour='" + str(session['hour']) + "' and date='" + str(session['date']) + "'")
            cmd.execute("update attendence set attendance='" + str(att[i]) + "' where studentlid='" + str(
                student[i]) + "' and hour='" + str(session['hour']) + "' and date='" + str(session['date']) + "'")
            con.commit()

        return '''<script>alert("Attendance Changed");window.location='/staffviewattendancess'</script>'''


#staff

@app.route('/changeattendances',methods=['post','get'])
@login_required
def changeattendances():
    student=request.form.getlist('sid')
    att=request.form.getlist('att')
    lngth=len(att)
    for i in range(lngth):
        print("update attendence set attendance='"+str(att[i])+"' where studentlid='"+str(student[i])+"' and hour='"+str(session['hour'])+"' and date='"+str(session['date'])+"'")
        cmd.execute("update attendence set attendance='"+str(att[i])+"' where studentlid='"+str(student[i])+"' and hour='"+str(session['hour'])+"' and date='"+str(session['date'])+"'")
        con.commit()

    return '''<script>alert("Attendance Changed");window.location='/viewattendance'</script>'''


@app.route('/staffviewattendancess',methods=['post','get'])
@login_required
def staffviewattendancess():
    return render_template("staff/attendance.html",len=0)

@app.route('/staffviewattendances',methods=['post','get'])
@login_required
def staffviewattendances():
    type=request.form['submit']
    if type=="view":
        sem=request.form['sem']
        session['sem']=sem
        Division=request.form['divi']
        session['division']=Division
        date=request.form['date']
        session['date']=date
        hour=request.form['hour']
        session['hour']=hour
        print("SELECT `department` FROM `teacher` WHERE `lid`='"+str(session['lid'])+"'")
        cmd.execute("SELECT `department` FROM `teacher` WHERE `lid`='"+str(session['lid'])+"'")
        rr=cmd.fetchone()
        dept=rr[0]
        session['dept']=dept
        print(dept)
        print("SELECT `attendence`.`attendance`,`attendence`.`hour`,`student`.`regno` FROM `attendence` JOIN `student` ON `student`.`lid`=`attendence`.`studentlid` WHERE `attendence`.`date`='"+date+"' AND `attendence`.`hour`='"+hour+"' AND `attendence`.`division`='"+Division+"' AND `attendence`.`sem`='"+sem+"' AND `attendence`.`department`='"+dept+"'")
        cmd.execute("SELECT `attendence`.`attendance`,`attendence`.`hour`,`student`.`regno` FROM `attendence` JOIN `student` ON `student`.`lid`=`attendence`.`studentlid` WHERE `attendence`.`date`='"+date+"' AND `attendence`.`hour`='"+hour+"' AND `attendence`.`division`='"+Division+"' AND `attendence`.`sem`='"+sem+"' AND `attendence`.`department`='"+dept+"'")
        res=cmd.fetchall()
        print(res)
        if len(res)==0:
            return '''<script>alert("No data");window.location='/staffviewattendancess'</script>'''
        else:

            return render_template("staff/attendance.html",val=res,sem=sem,divi=Division,date=date,hour=hour)
    elif type=="update":
        cmd.execute("SELECT `attendence`.`attendance`,`attendence`.`hour`,`student`.`regno`,`student`.`lid` FROM `attendence` JOIN `student` ON `student`.`lid`=`attendence`.`studentlid` WHERE `attendence`.`date`='" + str(session['date']) + "' AND `attendence`.`hour`='" + str(session['hour']) + "' AND `attendence`.`division`='" + str(session['division']) + "' AND `attendence`.`sem`='" + str(session['sem']) + "' AND `attendence`.`department`='" + str(session['dept']) + "'")
        res = cmd.fetchall()
        print(res)
        return render_template("staff/attendance1.html",val=res)

@app.route('/staffprofile',methods=['post','get'])
@login_required
def staffprofile():
    cmd.execute("select * from teacher where lid='" + str(session['lid']) + "'")
    res = cmd.fetchone()
    return render_template("staff/staff_profile.html",i=res)
@app.route('/changeimg',methods=['post','get'])
@login_required
def changeimg():
    id=request.args.get('id')
    session['photo']=id
    return render_template("staff/image.html",i=id)

@app.route('/changeimgs',methods=['post','get'])
@login_required
def changeimgs():
    id=request.args.get('id')
    session['photo']=id
    return render_template("admin/staff_editimg.html",i=id)

@app.route('/studentchangeimgs',methods=['post','get'])
@login_required
def studentchangeimgs():
    id=request.args.get('id')
    session['photo']=id
    return render_template("admin/student_editimg.html",i=id)


@app.route('/updatestaffprofiles',methods=['post','get'])
@login_required
def updatestaffprofiles():
    img = request.files['files']
    import time
    req = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
    img.save(os.path.join('./static/staffphoto', req))
    cmd.execute("update teacher set photo='"+req+"' where photo='"+str(session['photo'])+"'")
    con.commit()
    return '''<script>alert("Successfully Updated");window.location='/staffprofile'</script>'''

@app.route('/updatestaffprofiless',methods=['post','get'])
@login_required
def updatestaffprofiless():
    img = request.files['files']
    import time
    req = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
    img.save(os.path.join('./static/staffphoto', req))
    cmd.execute("update teacher set photo='"+req+"' where photo='"+str(session['photo'])+"'")
    con.commit()
    return '''<script>alert("Successfully Updated");window.location='/viewstaff'</script>'''


@app.route('/updatestudentimg',methods=['post','get'])
@login_required
def updatestudentimg():
    img = request.files['files']
    import time
    req = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
    img.save(os.path.join('./static/studentphoto', req))
    cmd.execute("update student set photo='"+req+"' where photo='"+str(session['photo'])+"'")
    con.commit()
    return '''<script>alert("Successfully Updated");window.location='/viewstudent'</script>'''



@app.route('/updatestaffprofile',methods=['post','get'])
@login_required
def updatestaffprofile():

    fname=request.form['text1']
    code=request.form['text2']
    address=request.form['text3']
    phone=request.form['text4']
    email=request.form['text5']
    qualification=request.form['text6']
    dept=request.form['select']
    cmd.execute("update teacher set name='" + fname + "',teacher_code='" + code + "',address='" + address + "',phone='" + phone + "',email='" + email + "',qualification='" + qualification + "',department='" + dept + "' where lid='" + str(session['lid']) + "'")
    con.commit()

    return '''<script>alert("Successfully Updated");window.location='/staffprofile'</script>'''


@app.route('/staffviewstudent',methods=['post','get'])
@login_required
def staffviewstudent():
    cmd.execute("select * from student")
    res=cmd.fetchall()
    print(res)
    return render_template("staff/studentlist.html",val=res,i=0)

@app.route('/staffdeptsearch',methods=['post','get'])
@login_required
def staffdeptsearch():
    dept=request.form['selects']
    divi=request.form['divi']
    sem=request.form['select1']
    print("select * from student where department='"+dept+"'")
    cmd.execute("select * from student where department='"+dept+"' and division='"+divi+"' and semester='"+sem+"'")
    res=cmd.fetchall()
    print(res)
    if len(res)==0:
        return '''<script>alert("No data");window.location='/staffviewstudent'</script>'''
    else:
        return render_template("staff/studentlist.html",val=res,dept=dept,divi=divi,i=sem)

@app.route('/staffviewrequest',methods=['post','get'])
@login_required
def staffviewrequest():
    cmd.execute("SELECT `department` FROM `teacher` WHERE `lid`='" + str(session['lid']) + "'")
    rr = cmd.fetchone()
    dept = rr[0]
    print(dept)
    cmd.execute("SELECT `student`.`regno`,`student`.`name`,`student`.`department`,`student`.`semester`,`student`.`division`,`leave`.* from `student` JOIN `leave` ON `leave`.`studlid`=`student`.`lid` WHERE `student`.`department`='"+str(dept)+"'")
    res=cmd.fetchall()
    print(res)
    return render_template("staff/leaveRequestView.html",val=res)

@app.route('/leaveaccepted',methods=['post','get'])
@login_required
def leaveaccepted():
    id=request.args.get('id')
    cmd.execute("UPDATE   `leave` SET `status`='accepted' WHERE lvid='"+str(id)+"'")
    con.commit()
    return '''<script>alert("Leave granted");window.location='/staffviewrequest'</script>'''

@app.route('/leaverejected',methods=['post','get'])
@login_required
def leaverejected():
    id=request.args.get('id')
    cmd.execute("UPDATE   `leave` SET `status`='rejected' WHERE lvid='"+str(id)+"'")
    con.commit()
    return '''<script>alert("Leave rejected");window.location='/staffviewrequest'</script>'''

#student
@app.route('/studentviewprofile',methods=['post','get'])
@login_required
def studentviewprofile():
    id=session['lid']
    print(id)
    cmd.execute("select * from student where lid='"+str(id)+"'")
    res=cmd.fetchone()
    print(res)
    return render_template("student/student-profile.html",i=res)
@app.route('/studentupdate',methods=['post','get'])
@login_required
def studentupdate():
    try:
        fname=request.form['text1']
        regno=request.form['text2']
        address=request.form['text3']
        phone=request.form['text4']
        email=request.form['text5']

        dob=request.form['text6']


        img = request.files['files']
        name = secure_filename(img.filename)
        import time
        req = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        img.save(os.path.join('static/images', req))


        cmd.execute("update student set name='"+fname+"',regno='"+regno+"',address='"+address+"',phone='"+phone+"',email='"+email+"',dob='"+dob+"',photo='"+req+"' where lid='"+str(session['lid'])+"'")
        con.commit()
        return '''<script>alert("Successfully Updated");window.location='/studentviewprofile'</script>'''
    except Exception as e:
        print(e)
        fname = request.form['text1']
        regno = request.form['text2']
        address = request.form['text3']
        phone = request.form['text4']
        email = request.form['text5']
        dob = request.form['text6']


        cmd.execute(
            "update student set name='" + fname + "',regno='" + regno + "',address='" + address + "',phone='" + phone + "',email='" + email + "',dob='" + dob + "' where lid='" + str(
                session['lid']) + "'")
        con.commit()

        return '''<script>alert("Successfully Updated");window.location='/studentviewprofile'</script>'''

@app.route('/leavereq',methods=['post','get'])
@login_required
def leavereq():
    cmd.execute("select * from `leave` where studlid='"+str(session['lid'])+"'")
    res=cmd.fetchall()
    return render_template("student/leavestatus.html",val=res)
@app.route('/stleavereq',methods=['post','get'])
@login_required
def stleavereq():
    return render_template("student/student-leave.html")

@app.route('/staffviewsubject',methods=['post','get'])
@login_required
def staffviewsubject():

    return render_template("staff/subjectView.html")


@app.route('/sviewsubjects',methods=['post','get'])
@login_required
def sviewsubjects():

    sem=request.form['select1']
    cmd.execute("SELECT `department`   FROM`teacher` WHERE `lid`='"+str(session['lid'])+"'")
    res=cmd.fetchone()
    dept=res[0]
    cmd.execute("SELECT `subject`.*,`teacher`.`name`,`teacher`.`teacher_code` FROM `teacher` JOIN `subject` ON `subject`.`staff_lid`=`teacher`.`lid` WHERE `subject`.`department`='"+dept+"' AND `subject`.`semester`='"+sem+"'")
    s=cmd.fetchall()
    print(s)
    return render_template("staff/subjectView.html",val=s,sem=sem)



@app.route('/asviewsubjects',methods=['post','get'])
@login_required
def asviewsubjects():
    cmd.execute("SELECT * FROM `subject` WHERE `staff_lid`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    return render_template("staff/staffsubject.html",val=s)
@app.route('/leavereqsupdate',methods=['post','get'])
@login_required
def leavereqsupdate():
    req=request.form['text']
    date=request.form['date']
    day=request.form['day']
    cmd.execute("update `leave` set req_date=curdate(),studlid='"+str(session['lid'])+"',`leave`='"+req+"',days='"+day+"',leave_date='"+date+"' where lvid='"+str(session['lvid'])+"'")

    con.commit()
    return '''<script>alert("Leave updated....");window.location='/leavereq'</script>'''


@app.route('/leavereqs',methods=['post','get'])
@login_required
def leavereqs():
    req=request.form['text']
    date=request.form['date']
    day=request.form['day']
    cmd.execute("insert into `leave` values(null,curdate(),'"+str(session['lid'])+"','"+req+"','"+day+"','"+date+"','pending')")
    con.commit()
    return '''<script>alert("Leave Requested....");window.location='/leavereq'</script>'''

@app.route('/studentsignup',methods=['post','get'])
def studentsignup():
    return render_template("student.html")

@app.route('/addstudent',methods=['post','get'])
def addstudent():
    try:
        fname=request.form['text1']
        regno=request.form['text2']
        address=request.form['text3']
        phone=request.form['text4']
        email=request.form['text5']

        dob=request.form['text6']
        dept=request.form['select']
        Semester=request.form['select1']
        division=request.form['select3']
        Semester=request.form['select1']
        quardian=request.form['quardian']
        phonen=request.form['phone']

        img = request.files['files']
        name = secure_filename(img.filename)


        import time
        req = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        img.save(os.path.join('./static/studentphoto', req))

        uname = request.form['uname']
        password = request.form['password']
        cnfpassword = request.form['cnfpassword']
        if password == cnfpassword:
            cmd.execute("insert into login values(null,'" + uname + "','" + password + "','student')")
            id = con.insert_id()
            cmd.execute("insert into student values(null,'"+str(id)+"' ,'" + fname + "','" + regno + "','" + address + "','" + phone + "','" + email + "','" + dob + "','" + dept + "','" + Semester + "','" + division + "','" + req + "','"+quardian+"','"+phonen+"')")
            con.commit()
            return '''<script>alert("Successfully Registered");window.location='/'</script>'''
        else:
            return '''<script>alert("Password Mismatch.......!");window.location='/studentsignup'</script>'''
    except Exception as e:
        print(e)

        return '''<script>alert("Error");window.location='/'</script>'''

@app.route('/studentviewattendance',methods=['post','get'])
def studentviewattendance():
    return render_template("student/attendance.html")
@app.route('/studentviewattendances',methods=['post','get'])
def studentviewattendances():
    date=request.form['date']
    # hour=request.form['hour']
    print("SELECT `attendence`.`hour`,`attendence`.`attendance` FROM `attendence` JOIN `student` ON `student`.`lid`=`attendence`.`studentlid` WHERE `student`.`lid`='"+str(session['lid'])+"' and`attendence`.date='"+date+"' ")
    cmd.execute("SELECT `attendence`.`hour`,`attendence`.`attendance` FROM `attendence` JOIN `student` ON `student`.`lid`=`attendence`.`studentlid` WHERE `student`.`lid`='"+str(session['lid'])+"' and`attendence`.date='"+date+"' ")
    res=cmd.fetchall()
    print(res)
    return render_template("student/attendance.html",val=res)


# timetable
@app.route('/viewtimtable',methods=['post','get'])
def viewtimtable():
    return render_template("admin/timetableview.html")

@app.route('/addimg',methods=['post','get'])
def addimg():
    return render_template("student/addimg.html")


@app.route('/addimgs',methods=['post'])
def addimgs():
    import cv2

    # Initialize the camera
    camera = cv2.VideoCapture(0)

    # Number of images to capture
    num_images_to_capture = 10
    images_captured = 1

    while images_captured <= num_images_to_capture:
        # Capture frame
        ret, frame = camera.read()
        ret, img = camera.read()


        if not ret:
            print("Failed to capture frame")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print("length" + str(len(faces)))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # draw rectangle to main image

        emolist = []

        # Display the frame (optional)
        cv2.imshow('Frame', frame)

        # Save the frame as an image (optional)
        # cv2.imwrite(f'image_{images_captured}.png', frame)

        # Increment the count of captured images
        images_captured += 1
        nm = "s" + str(session['lid'])

        static_folder = os.path.join(app.root_path, 'static/training-data')
        directory_path = os.path.join(static_folder, nm)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        pth = 'static/training-data/' + nm + '/'
        fn = time.strftime("%Y%m%d_%H%M%S")+str(images_captured)+".jpg"
        print("fnnnnnnnnnnnnn", fn)
        cv2.imwrite(pth + fn, img)
        cmd.execute("insert into images values(null,'" + str(session['lid']) + "','" + fn + "')")
        con.commit()

        # Wait for a key press for 60 milliseconds
        key = cv2.waitKey(1000) & 0xFF

        # Check if the pressed key is ESC (ASCII value 27)
        if key == 27:
            break

    # Release the camera and close any OpenCV windows
    camera.release()
    cv2.destroyAllWindows()

    return redirect('/viewimg')

    # i=0
        # while (True):
        #     try:
        #         ret, img = cap.read()
        #         # img=cv2.imread(fn)
        #         print(ret)
        #
        #         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #
        #         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #         print("length" + str(len(faces)))
        #         # for (x,y,w,h) in faces:
        #         # 	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle to main image
        #
        #
        #         emolist = []
        #         cv2.imshow("Frame", img)
        #         if len(faces) > 0:
        #
        #         # enf("static/pic/"+fn)
        #             nm = "s" + str(session['lid'])
        #             i=i+1
        #             if i<=10:
        #                 static_folder = os.path.join(app.root_path, 'static/training-data')
        #                 directory_path = os.path.join(static_folder, nm)
        #                 if not os.path.exists(directory_path):
        #                     os.makedirs(directory_path)
        #                 pth='static/training-data/'+nm+'/'
        #                 fn = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        #                 cv2.imwrite(pth + fn, img)
        #                 cmd.execute("insert into images values(null,'"+str(session['lid'])+"','"+fn+"')")
        #                 con.commit()
        #             else:
        #                 cv2.destroyAllWindows()
        #                 cv2.waitKey(1)
        #                 cv2.destroyAllWindows()
        #                 break
        #
        #         if cv2.waitKey(60) & 0xFF == 27:
        #             break
        #     except Exception as e:
        #         print(e)
        #         pass









@app.route('/viewimg',methods=['post','get'])
def viewimg():
    cmd.execute("select * from images where logid='"+str(session['lid'])+"'")
    res=cmd.fetchall()
    id=session['lid']
    return render_template("student/images.html",val=res,id=id)
@app.route('/sviewtimtable',methods=['post','get'])
def sviewtimtable():
    return render_template("staff/timetable-view.html")
@app.route('/stviewtimtable',methods=['post','get'])
def stviewtimtable():
    return render_template("student/student-timetableView.html")

@app.route('/viewtimtables',methods=['post','get'])
@login_required
def viewtimtables():
    dept=request.form['select']
    sem=request.form['Semester']
    print("SELECT `timetable`.`tid`,`timetable`.`hour`,`subject`.`subject`,`subject`.`code` FROM `subject` JOIN `timetable` ON `timetable`.`subid`=`subject`.`sid` WHERE `timetable`.`dept`='"+dept+"' AND `timetable`.`sem`='"+sem+"'")
    cmd.execute("SELECT `timetable`.`tid`,`timetable`.`hour`,`subject`.`subject`,`subject`.`code` FROM `subject` JOIN `timetable` ON `timetable`.`subid`=`subject`.`sid` WHERE `timetable`.`dept`='"+dept+"' AND `timetable`.`sem`='"+sem+"'")
    s=cmd.fetchall()
    print(s)
    return render_template("admin/timetableview.html",val=s,dept=dept,sem=sem)

@app.route('/sviewtimtables',methods=['post','get'])
@login_required
def sviewtimtables():
    dept=request.form['select']
    sem=request.form['Semester']
    print("SELECT `timetable`.`tid`,`timetable`.`hour`,`subject`.`subject`,`subject`.`code` FROM `subject` JOIN `timetable` ON `timetable`.`subid`=`subject`.`sid` WHERE `timetable`.`dept`='"+dept+"' AND `timetable`.`sem`='"+sem+"'")
    cmd.execute("SELECT `timetable`.`tid`,`timetable`.`hour`,`subject`.`subject`,`subject`.`code` FROM `subject` JOIN `timetable` ON `timetable`.`subid`=`subject`.`sid` WHERE `timetable`.`dept`='"+dept+"' AND `timetable`.`sem`='"+sem+"'")
    s=cmd.fetchall()
    print(s)
    return render_template("staff/timetable-view.html",val=s,dept=dept,sem=sem)


@app.route('/addtimtable',methods=['post','get'])
@login_required
def addtimtable():
    # staffid=session['lid']
    # print("SELECT `department` FROM `teacher` WHERE `lid`='"+str(staffid)+"'")
    # cmd.execute("SELECT `department` FROM `teacher` WHERE `lid`='"+str(staffid)+"'")
    # s=cmd.fetchone()
    # dept=s[0]
    # session['dept']=dept
    return render_template("admin/Addtimetable.html")

@app.route('/addtimetable',methods=['post','get'])
@login_required
def addtimetable():
    dept=request.form['select']
    # subj=request.form['select1']
    sem=request.form['Semester']
    # hour=request.form['select3']
    session['semess']=sem
    session['deptt']=dept
    cmd.execute("SELECT * FROM timetable WHERE `dept`='"+str(dept)+"' AND `sem`='"+str(sem)+"'")
    s=cmd.fetchone()
    if s is None:
        a1 = []
        cmd.execute("SELECT * FROM `subject` WHERE `department`='" + dept + "' AND `semester`='" + sem + "' ")
        res = cmd.fetchall()
        if res is not None:
            for i in res:
                a1.append(i[1])
            hours_per_day = 7  # Number of hours in a day
            timetable = generate_timetable(a1, hours_per_day)
            print(type(timetable))
            ll = []
            for i in timetable:
                print(i)
                # ll.append(i[1])

            print(timetable)
            result_list = [timetable[key] for key in sorted(timetable.keys())]

            # Flatten the list
            flattened_list = [item for sublist in result_list for item in sublist]

            print(flattened_list)
            cmd.execute("insert into timetable values(null,'"+dept+"','"+sem+"','Monday','"+flattened_list[0]+"','"+flattened_list[1]+"','"+flattened_list[2]+"','break','"+flattened_list[4]+"','"+flattened_list[5]+"','"+flattened_list[6]+"')")
            con.commit()

            cmd.execute("insert into timetable values(null,'"+dept+"','"+sem+"','Tuesday','"+flattened_list[7]+"','"+flattened_list[8]+"','"+flattened_list[9]+"','break','"+flattened_list[11]+"','"+flattened_list[12]+"','"+flattened_list[13]+"')")
            con.commit()

            cmd.execute("insert into timetable values(null,'"+dept+"','"+sem+"','Wednesday','"+flattened_list[14]+"','"+flattened_list[15]+"','"+flattened_list[16]+"','break','"+flattened_list[18]+"','"+flattened_list[19]+"','"+flattened_list[20]+"')")
            con.commit()

            cmd.execute("insert into timetable values(null,'"+dept+"','"+sem+"','Thursday','"+flattened_list[21]+"','"+flattened_list[22]+"','"+flattened_list[23]+"','break','"+flattened_list[25]+"','"+flattened_list[26]+"','"+flattened_list[27]+"')")
            con.commit()

            cmd.execute("insert into timetable values(null,'"+dept+"','"+sem+"','Friday','"+flattened_list[28]+"','"+flattened_list[29]+"','"+flattened_list[30]+"','break','"+flattened_list[32]+"','"+flattened_list[33]+"','"+flattened_list[34]+"')")
            con.commit()
            cmd.execute("SELECT `day`,`h1`,`h2`,`h3`,`h4`,`h5`,`h6`,`h7` FROM `timetable` WHERE `dept`='"+dept+"' AND `sem`='"+sem+"'")
            res=cmd.fetchall()

            return render_template("admin/timetable.html",res=res)
        else:
            return '''<script>alert("Already Added");window.location='/viewtimetable'</script>'''




    else:
        # return '''<script>alert("Already Added");window.location='/viewtimetable'</script>'''
        return redirect('/viewtimetable')




@app.route('/viewtimetable',methods=['post','get'])
@login_required
def viewtimetable():
    cmd.execute(
        "SELECT `day`,`h1`,`h2`,`h3`,`h4`,`h5`,`h6`,`h7`,`tid` FROM `timetable` WHERE `dept`='" + str(session['deptt']) + "' AND `sem`='" +str(session['semess'])+ "'")
    res = cmd.fetchall()
    return render_template("admin/timetable.html",res=res)

@app.route('/saddtimetable',methods=['post','get'])
@login_required
def saddtimetable():
    dept=request.form['select']
    # subj=request.form['select1']
    sem=request.form['Semester']
    # hour=request.form['select3']
    cmd.execute(
        "SELECT `day`,`h1`,`h2`,`h3`,`h4`,`h5`,`h6`,`h7`,`tid` FROM `timetable` WHERE `dept`='" + str(
            dept) + "' AND `sem`='" + str(sem) + "'")
    res = cmd.fetchall()


    return render_template("staff/timetable.html",res=res)

@app.route('/saddtimetables',methods=['post','get'])
@login_required
def saddtimetables():
    dept=request.form['select']
    # subj=request.form['select1']
    sem=request.form['Semester']
    # hour=request.form['select3']
    cmd.execute(
        "SELECT `day`,`h1`,`h2`,`h3`,`h4`,`h5`,`h6`,`h7`,`tid` FROM `timetable` WHERE `dept`='" + str(
            dept) + "' AND `sem`='" + str(sem) + "'")
    res = cmd.fetchall()


    return render_template("student/timetable.html",res=res)




def generate_timetable(subjects, hours_per_day):
    timetable = {}
    for hour in range(1, hours_per_day + 1):
        # Randomly select subjects for the current hour
        subjects_for_hour = random.sample(subjects, min(5, len(subjects)))
        # If less than 5 subjects are available, repeat subjects
        subjects_for_hour += random.choices(subjects, k=max(0, 5 - len(subjects_for_hour)))
        timetable[hour] = subjects_for_hour
    return timetable

@app.route('/getsubject',methods=['get','post'])
def getsubject():
    print(request.form)
    sem = request.form['sem']
    dept=request.form['dept']
    print(sem)
    cmd.execute("SELECT `sid`,`subject`,`code` FROM `subject` WHERE `semester`='"+sem+"'AND `department`='"+dept+"'")
    s=cmd.fetchall()
    print(s)

    lis=[0,'select']
    for r in s:
        lis.append(r[0])
        lis.append(r[1]+"(CODE:"+str(r[2])+")")
    print(lis)
    resp = make_response(jsonify(lis))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp




@app.route('/att',methods=['post','get'])
@login_required
def att():
    id=request.args.get('id')

    cmd.execute("SELECT `studentlid`,COUNT(`attendance`) FROM `attendence`  WHERE `subid`='" + str(id) + "' AND `attendance`='0' GROUP BY `studentlid` ")
    res = cmd.fetchall()
    print("llll",type(res))
    print("kkkkkkkk",res)

    ll=[]
    kk=[]
    results_list = []

    for k in res:
        print(k[1])
        if k[1]>=3:
            cmd.execute("SELECT `student`.`department`,`student`.`semester`,`student`.`division`,`student`.`name`,`student`.`regno`,`student`.`gname`,`student`.`gnumber`, `student`.`lid` FROM `attendence` JOIN `student` ON `student`.`lid`=`attendence`.`studentlid` WHERE `attendence`.`subid`='"+str(id)+"' AND `attendence`.`studentlid`='"+str(k[0])+"' GROUP BY `student`.`lid`")
            s=cmd.fetchall()
            for i in s:
                results_list.append(i)
        else:
            return '''<script>alert("No data");window.location='/teacherhome'</script>'''






            # ll.insert(s)

        result=tuple(results_list)
        print("listtttttttttttttttt",result)

    return render_template("staff/absentnotification1.html",val=result)

@app.route('/absent',methods=['post','get'])
@login_required
def absent():
    cmd.execute("SELECT sid FROM `subject` WHERE `staff_lid`='"+str(session['lid'])+"'")
    s=cmd.fetchall()
    # print("s"+str(s))
    sub=[]
    subject=[]
    for i in s:
        # print(i[0])
        # print("SELECT `studentlid`,COUNT(`attendance`) FROM `attendence`  WHERE `subid`='" + str(i[0]) + "' AND `attendance`='0' GROUP BY `studentlid` ")
        cmd.execute("SELECT `studentlid`,COUNT(`attendance`) FROM `attendence`  WHERE `subid`='" + str(i[0]) + "' AND `attendance`='0' AND `status`='notify' GROUP BY `studentlid` ")
        res = cmd.fetchall()
        print("res"+str(len(res)))
        if len(res)>0:
            sub.append(i[0])
        # print("sub"+str(sub))

        for k in sub:
            cmd.execute("SELECT * FROM `subject` WHERE `sid`='" + str(k) + "'")
            rr = cmd.fetchall()
            subject.append(rr)
        # print("subject"+str(subject))
        # for kk in subject:
        #     print(kk[0])
    print(subject)
    for hh in subject:
        print(hh[0][3])
    # print(hh[0][3])
    # print(hh[0][4])

    #     print(hh[2][0])
    #     print(hh[3][0])
    #     print(hh[4][0])
    return render_template("staff/abscents.html",s=subject)

@app.route('/viewdates',methods=['post','get'])
@login_required
def viewdates():
    id=request.args.get('id')
    cmd.execute("SELECT date,aid FROM `attendence` WHERE `studentlid`='"+str(id)+"'")
    res=cmd.fetchall()
    # for i in res:

    return render_template("staff/absentnotification2.html",v=res)
@app.route('/datecheck',methods=['post','get'])
@login_required
def datecheck():
    aid=request.form.getlist('id')
    print("aid",aid)
    for i in aid:
        print(i)
        print("update attendence set status='viewed' where aid='"+str(i)+"'")
        cmd.execute("update attendence set status='viewed' where aid='"+str(i)+"'")
        con.commit()
    return redirect('/teacherhome')

@app.route('/sviewatt',methods=['post','get'])
@login_required
def sviewatt():
    print("SELECT `department`,`semester` FROM`student` WHERE `lid`='"+str(session['lid'])+"'")
    cmd.execute("SELECT `department`,`semester` FROM`student` WHERE `lid`='"+str(session['lid'])+"'")
    s=cmd.fetchone()
    dept=s[0]
    sem=s[1]
    lis=[]
    ll=[]
    print("SELECT `subject`.`subject`,COUNT(`attendence`.`date`) FROM `subject` JOIN `attendence` ON `attendence`.`subid`=`subject`.`sid`WHERE `attendence`.`studentlid`='"+str(session['lid'])+"' GROUP BY `attendence`.`subid`")
    cmd.execute("SELECT `subject`.`subject`,COUNT(`attendence`.`date`) FROM `subject` JOIN `attendence` ON `attendence`.`subid`=`subject`.`sid`WHERE `attendence`.`studentlid`='"+str(session['lid'])+"' GROUP BY `attendence`.`subid`")
    s2=cmd.fetchall()
    print(s2)
    for i in s2:
        lis.append(i[1])
    print("SELECT `subject`.`subject`,COUNT(`attendence`.`attendance`) FROM `subject` JOIN `attendence` ON `attendence`.`subid`=`subject`.`sid`WHERE `attendence`.`studentlid`='"+str(session['lid'])+"' AND `attendence`.`attendance`=1 GROUP BY `attendence`.`subid`")
    cmd.execute("SELECT `subject`.`subject`,COUNT(`attendence`.`attendance`) FROM `subject` JOIN `attendence` ON `attendence`.`subid`=`subject`.`sid`WHERE `attendence`.`studentlid`='"+str(session['lid'])+"' AND `attendence`.`attendance`=1 GROUP BY `attendence`.`subid`")
    s3=cmd.fetchall()
    k=len(s3)
    for j in range(k):
        print("1",s3[j][1])
        print("2",lis[j])
        dd= (s3[j][1]/lis[j])*100
        ll.append(dd)
    print(lis)
    print(s3)
    return render_template("student/student-attendace.html",v1=lis,v2=s3,l=len(s3),p=ll)

@app.route('/takeat1',methods=['post','get'])
def takeat1():
    return render_template("staff/takeattedance.html",)

@app.route('/takeat',methods=['post','get'])
@login_required
def takeat():
    sem=request.form['Semester']
    divi=request.form['divi']
    hour=request.form['hour']
    dept=request.form['select']
    sub=request.form['select1']
    session['semester']=sem
    session['divisions']=divi
    session['hours']=hour
    session['depts']=dept
    session['subj']=sub
    # cam(sem,divi,hour,dept,sub)
    import cv2

    # Initialize the camera
    camera = cv2.VideoCapture(0)

    # Number of images to capture
    num_images_to_capture = 10
    images_captured = 0

    while images_captured < num_images_to_capture:
        # Capture frame
        ret, frame = camera.read()

        if not ret:
            print("Failed to capture frame")
            break

        # Display the frame (optional)
        cv2.imshow('Frame', frame)

        # Save the frame as an image (optional)
        # cv2.imwrite(f'image_{images_captured}.png', frame)

        # Increment the count of captured images
        images_captured += 1
        pth = 'static/test/'
        fn = time.strftime("%Y%m%d_%H%M%S") + str(images_captured) + ".jpg"
        print("fnnnnnnnnnnnnn", fn)
        cv2.imwrite(pth + fn, frame)
        # Wait for a key press for 60 milliseconds
        key = cv2.waitKey(1) & 0xFF

        # Check if the pressed key is ESC (ASCII value 27)
        if key == 27:
            break

    # Release the camera and close any OpenCV windows
    camera.release()
    cv2.destroyAllWindows()


    return render_template("staff/stopclass.html")

@app.route('/stopclass',methods=['post','get'])
@login_required
def stopclass():
    sem=session['semester']
    divi= session['divisions']
    hour= session['hours']
    dept=session['depts']
    sub=session['subj']
    directory = './static/test'
    files = os.listdir(directory)
    labels=[]
    for file in files:
            # Check if the file is an image
        if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                # Read the image
                from src.facemaster import predict

                image_path = os.path.join(directory, file)
                predicted_img, label = predict(image_path)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                cv2.destroyAllWindows()
                print("Recognized faces = ", label)
                labels.append(label)
    print(labels)
    unique_values = list(set(value for sublist in labels for value in sublist))
    for i in unique_values:
        cmd.execute("SELECT * FROM `attendence` WHERE `studentlid`='" + str(
            i) + "' AND `date`=CURDATE() AND `hour`='"+hour+"' AND `sem`='" + sem + "' AND `division`='" + divi + "' AND `department`='" + dept + "' AND `subid`='" + sub + "'")
        res = cmd.fetchone()
        print(",,,,,,,,,", res)
        if res is None:
                pth = "s" + str(i)
                cmd.execute("insert into attendence values(null,'" + str(i) + "',curdate(),'1','" + str(
                    pth) + "','" + hour + "','" + sem + "','" + divi + "','" + dept + "','" + sub + "','notify')")
                con.commit()




    cmd.execute("SELECT `lid` FROM `student` WHERE `lid` NOT IN(SELECT `studentlid` FROM `attendence` WHERE `date`=CURDATE() AND `hour`='"+hour+"' AND `sem`='"+sem+"' AND `division`='"+divi+"' AND `department`='"+dept+"' AND `subid`='"+sub+"')")
    res=cmd.fetchall()
    print(res)
    for i in res:
        pth="s"+str(i[0])
        cmd.execute("insert into attendence values(null,'" + str(i[0]) + "',curdate(),'0','"+str(pth)+"','" + hour + "','" + sem + "','" + divi + "','" + dept + "','" + sub + "','notify')")
        con.commit()
    directory_to_clean = './static/test'
    delete_files_in_directory(directory_to_clean)

    return redirect('/teacherhome')



@app.route('/delimg',methods=['post','get'])
@login_required
def delimg():
    id=request.args.get('id')
    file_to_delete = "./static/training-data/s"+str(session['lid'])+"/"+id
    delete_file(file_to_delete)

    cmd.execute("delete from images where image='"+id+"' ")
    con.commit()
    return '''<script>alert("Successfully Deleted");window.location='/viewimg'</script>'''

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"No permission to delete '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/updatetime', methods=['post', 'get'])
@login_required
def updatetime():
    id=request.form.getlist("id")
    a1=request.form.getlist("a1")
    a2=request.form.getlist("a2")
    a3=request.form.getlist("a3")
    a4=request.form.getlist("a4")
    a5=request.form.getlist("a5")
    a6=request.form.getlist("a6")
    a7=request.form.getlist("a7")
    print("id",id)
    print("a1",a1)
    print("a2",a2)
    print("a3",a3)
    print("a4",a4)
    print("a5",a5)
    print("a6",a6)
    print("a7",a7)
    for i in id:

        cmd.execute("update timetable set h1='"+str(a1[0])+"',h2='"+str(a2[0])+"',h3='"+str(a3[0])+"',h4='"+str(a4[0])+"',h5='"+str(a5[0])+"',h6='"+str(a6[0])+"',h7='"+str(a7[0])+"' where tid='"+str(i[0])+"'")
        con.commit()
        cmd.execute(
            "update timetable set h1='" + str(a1[1]) + "',h2='" + str(a2[1]) + "',h3='" + str(a3[1]) + "',h4='" + str(
                a4[1]) + "',h5='" + str(a5[1]) + "',h6='" + str(a6[1]) + "',h7='" + str(a7[1]) + "' where tid='" + str(
                id[1]) + "'")
        con.commit()

        cmd.execute(
            "update timetable set h1='" + str(a1[2]) + "',h2='" + str(a2[2]) + "',h3='" + str(a3[2]) + "',h4='" + str(
                a4[2]) + "',h5='" + str(a5[2]) + "',h6='" + str(a6[2]) + "',h7='" + str(a7[2]) + "' where tid='" + str(
                id[2]) + "'")
        con.commit()

        cmd.execute(
            "update timetable set h1='" + str(a1[3]) + "',h2='" + str(a2[3]) + "',h3='" + str(a3[3]) + "',h4='" + str(
                a4[3]) + "',h5='" + str(a5[3]) + "',h6='" + str(a6[3]) + "',h7='" + str(a7[3]) + "' where tid='" + str(
                id[3]) + "'")
        con.commit()

        cmd.execute(
            "update timetable set h1='" + str(a1[4]) + "',h2='" + str(a2[4]) + "',h3='" + str(a3[4]) + "',h4='" + str(
                a4[4]) + "',h5='" + str(a5[4]) + "',h6='" + str(a6[4]) + "',h7='" + str(a7[4]) + "' where tid='" + str(
                id[4]) + "'")
        con.commit()

    return '''<script>alert("updated");window.location='/addtimtable'</script>'''





@app.route('/ssviewtimetable',methods=['post','get'])
@login_required
def ssviewtimetable():
    dept = request.form['select']
    sem = request.form['Semester']
    cmd.execute(
        "SELECT `day`,`h1`,`h2`,`h3`,`h4`,`h5`,`h6`,`h7`,`tid` FROM `timetable` WHERE `dept`='" + str(dept) + "' AND `sem`='" +str(sem)+ "'")
    res = cmd.fetchall()
    return render_template("staff/timetable.html",res=res)

def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(f"Deleted {filepath}")
            elif os.path.isdir(filepath):
                delete_files_in_directory(filepath)
        except Exception as e:
            print(f"Error deleting {filepath}: {e}")
if __name__ == "__main__":
    app.run(debug=True)

