from flask import Flask, render_template, request, redirect, session,url_for
from blockchain import Block, Blockchain
import datetime

global current_faculty
global current_student
app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"

blockchain = Blockchain()


@app.route('/')
def home():
    return render_template("index.html")

    
@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/admin_login', methods=["GET", "POST"])
def admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            error1 = "Please fill out All fields!"
            return render_template('admin_login.html', error1=error1)

        chain = blockchain.getAdminData()
        for i in chain:
            if i.data.get("username") == username:
                if i.data.get("password") == password:
                    std_count = len(blockchain.getStudentData())
                    fcl_count = len(blockchain.getFacultyData())

                    return render_template("admin_dashboard.html", student_count = std_count, faculty_count = fcl_count)
        return render_template("admin_login.html")
    return render_template("admin_login.html")


@app.route('/admin_dashboard')
def admin_dashboard():
    std_count = len(blockchain.getStudentData())
    fcl_count = len(blockchain.getFacultyData())

    return render_template("admin_dashboard.html", student_count=std_count, faculty_count=fcl_count)


@app.route("/add_student", methods=['POST', 'GET'])
def add_student():
    if request.method == "POST":
        name = request.form.get('name')
        std_id = request.form.get('id')
        password = request.form.get('password')
        conf_password = request.form.get('con_password')
        program = request.form.get('program')
        semester = request.form.get('semester')

        if not name or not std_id or not password or not conf_password:
            error1 = "Please fill out All fields!"
            return render_template('add_student.html', error1=error1)

        # checking if email exist or not
        student_exist = False
        students = blockchain.getStudentData()
        for i in students:
            if i.data.get("id") == std_id:
                student_exist = True

        if student_exist:
            error3 = "Student with this ID, already Registered!"
            return render_template('add_student.html', error3=error3)

        # rules of adding password
        length = False
        if len(password) >= 3:
            length = True
        numeric = False
        for p in password:
            if p.isdigit():
                numeric = True
        if (numeric != True or length != True):
            error4 = "Password rules not fulfilled!"
            return render_template('add_student.html', error4=error4)

        if password != conf_password:
            error2 = "Password confirmation not match!"
            return render_template('add_student.html', error2=error2)

        # adding student data on blockchain...
        data = {"name": name, "id": std_id, "password": password, "program": program, "semester": semester,
                "Student": True}
        new_blocks = Block((len(blockchain.get_chain()) + 1), datetime.datetime.now().date(), data, "", "")
        blockchain.add_block(new_blocks)

        confirm = "Student Registered Successfully!"
        return render_template('add_student.html', comfirm=confirm)

    return render_template("add_student.html")


@app.route("/add_faculty", methods=['POST', 'GET'])
def add_faculty():
    if request.method == "POST":
        name = request.form.get('name')
        faculty_id = request.form.get('id')
        password = request.form.get('password')
        conf_password = request.form.get('con_password')
        subject = request.form.get('subject')

        if not name or not faculty_id or not password or not conf_password:
            error1 = "Please fill out All fields!"
            return render_template('add_faculty.html', error1=error1)

        # checking if id exist or not
        student_exist = False
        faculty = blockchain.getFacultyData()
        for i in faculty:
            if i.data.get("id") == faculty_id:
                student_exist = True

        if student_exist:
            error3 = "Teacher with this ID, already Registered!"
            return render_template('add_faculty.html', error3=error3)

        # rules of adding password
        length = False
        if len(password) >= 3:
            length = True
        numeric = False
        for p in password:
            if p.isdigit():
                numeric = True
        if (numeric != True or length != True):
            error4 = "Password rules not fulfilled!"
            return render_template('add_faculty.html', error4=error4)

        if password != conf_password:
            error2 = "Password confirmation not match!"
            return render_template('add_faculty.html', error2=error2)

        # adding faculty data on blockchain...
        data = {"name": name, "id": faculty_id, "password": password, "subject": subject, "Faculty": True}
        new_blocks = Block((len(blockchain.get_chain()) + 1), datetime.datetime.now().date(), data, "", "")
        blockchain.add_block(new_blocks)

        confirm = "Teacher Registered Successfully!"
        return render_template('add_faculty.html', comfirm=confirm)

    return render_template("add_faculty.html")


@app.route('/student_login', methods=["GET", "POST"])
def student():
    if request.method == 'POST':
        std_id = request.form.get("id")
        password = request.form.get("password")

        if not std_id or not password:
            error1 = "Please fill out All fields!"
            return render_template('student_login.html', error1=error1)

        # confirming that, student id exist or not
        student_exist = False
        for i in blockchain.getStudentData():
            if i.data.get("id") == std_id:
                student_exist = True
        if not student_exist:
            error3 = "Student-ID doesn't exist!"
            return render_template('student_login.html', error3=error3)

        # confirming password of above id
        check = {}
        for i in blockchain.getStudentData():
            if i.data.get("id") == std_id:
                check = i
                break
        if (check.data.get("id") != std_id or check.data.get("password") != password):
            error2 = "Wrong Password!"
            return render_template('student_login.html', error2=error2)
        global current_student
        current_student=check.data
        return render_template("student_dashboard.html", currentuser = (current_student.get("name")))

    return render_template("student_login.html")

@app.route('/faculty_login', methods=["GET", "POST"])
def faculty():
    if request.method == 'POST':
        faculty_id = request.form.get("id")
        password = request.form.get("password")

        if not faculty_id or not password:
            error1 = "Please fill out All fields!"
            return render_template('faculty_login.html', error1=error1)

        # confirming that, teacher id exist or not
        student_exist = False
        for i in blockchain.getFacultyData():
            if i.data.get("id") == faculty_id:
                student_exist = True
        if not student_exist:
            error3 = "Faculty-ID doesn't exist!"
            return render_template('faculty_login.html', error3=error3)

        # confirming password of above id
        check = {}
        for i in blockchain.getFacultyData():
            if i.data.get("id") == faculty_id:
                check = i
                break
        if (check.data.get("id") != faculty_id or check.data.get("password") != password):
            error2 = "Wrong Password!"
            return render_template('faculty_login.html', error2=error2)
        global current_faculty
        current_faculty = check.data
        return render_template("faculty_dashboard.html", currentuser = current_faculty.get("name"))

    return render_template("faculty_login.html")


# displaying students details
@app.route('/student_detail')
def student_details():
    chain = blockchain.getStudentData()
    return render_template("student_detail.html", chain= chain)


# displaying faculty details
@app.route('/faculty_detail')
def faculty_details():
    chain = blockchain.getFacultyData()

    return render_template("faculty_detail.html", chain=chain)


@app.route('/student_dashboard')
def student_dashboard():
    global current_student
    return render_template("student_dashboard.html", currentuser=(current_student.get("name")))


@app.route('/faculty_dashboard')
def faculty_dashboard():

    return render_template("faculty_dashboard.html", currentuser=(current_faculty.get("name")))


@app.route("/attendance", methods=['POST', 'GET'])
def attendance():
    
    if request.method == "POST":
        
        subject = request.form.get('subject')
        date = request.form.get('date')
        present = request.form.get('present')


        # adding student attendance on blockchain...
        data = {"id":current_student.get("id"),"name":current_student.get("name"), "program":current_student.get("program"), "semester":current_student.get("semester"), "subject": subject,"date": date,"present": present, "Attendance":True}
        new_blocks = Block((len(blockchain.get_chain()) + 1), datetime.datetime.now().date(), data, "","")
        blockchain.add_block(new_blocks)

        confirm = "Attendance Marked Successfully!"
        return render_template('attendance.html', comfirm=confirm, currentuser = (current_student.get("name")))

    return render_template("attendance.html", currentuser = (current_student.get("name")))


@app.route("/student_reviews", methods=['POST', 'GET'])
def student_reviews():
          
    if request.method == "POST":

        date = request.form.get('date')
        reviews = request.form.get('reviews')
        print (reviews)
        # adding student data on blockchain...
        data = {"id":current_student.get("id"),"name":current_student.get("name"), "date": date,"reviews": reviews, "Reviews":True}
        new_blocks = Block((len(blockchain.get_chain()) + 1), datetime.datetime.now().date(), data, "","")
        blockchain.add_block(new_blocks)

        confirm = "Reviews sent to Blockchain Successfully!"

        return render_template('student_reviews.html', comfirm=confirm, currentuser=(current_student.get("name")))
    chain = blockchain.getStudentData()

    return render_template("student_reviews.html", chain = chain, currentuser=(current_student.get("name")))


@app.route("/student_absjustification", methods=['POST', 'GET'])
def student_absjustification():
          
    if request.method == "POST":

        date = request.form.get('date')
        justification = request.form.get('justification')
        # adding student data on blockchain...
        data = {"id":current_student.get("id"),"name":current_student.get("name"), "date": date, "justification": justification, "Justification":True}
        new_blocks = Block((len(blockchain.get_chain()) + 1), datetime.datetime.now().date(), data, "","")
        blockchain.add_block(new_blocks)

        confirm = "Justification sent to Blockchain Successfully!"

        return render_template('student_absjustification.html', comfirm=confirm, currentuser=(current_student.get("name")))
    chain = blockchain.getJustificationData()
    
   
    return render_template("student_absjustification.html", chain = chain, currentuser=(current_student.get("name")))


@app.route("/view_attendance")
def view_attendance():
    chain = blockchain.getAttendanceData()
    return render_template("view_attendance.html", chain = chain)


@app.route("/view_attendancestudent")
def view_attendancestudent():
    chain = blockchain.getAttendanceData()
    return render_template("view_attendancestudent.html", chain = chain)

@app.route("/view_attendance_faculty")
def view_attendance_faculty():
    chain = blockchain.getAttendanceData()
    global current_faculty
    return render_template("view_attendance_faculty.html", chain = chain, currentuser = current_faculty.get("name"))

@app.route("/view_justification_admin")
def view_justification_admin():
    chain = blockchain.getJustificationData()
    return render_template("view_justification_admin.html", chain = chain)


@app.route("/view_justification_faculty")
def view_justification_faculty():
    chain = blockchain.getJustificationData()
    global current_faculty
    return render_template("view_justification_faculty.html", chain = chain, currentuser = current_faculty.get("name"))


@app.route('/view_reviews_faculty')
def view_reviews_faculty():
    chain = blockchain.getReviewsData()
    global current_faculty
    return render_template("view_reviews_faculty.html", chain= chain, currentuser = current_faculty.get("name"))


@app.route('/view_reviews')
def view_reviews():
    chain = blockchain.getReviewsData()

    return render_template("view_reviews.html", chain=chain)
    
@app.route("/all_blocks")
def all_blocks():
    chain = blockchain.getAllData()
    blockchain.isValidchain()
    return render_template("all_blocks.html", chain = chain)


@app.route("/admin_logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin"))

@app.route("/faculty_logout")
def faculty_logout():
    session.clear()
    global current_faculty
    current_faculty = None
    return redirect(url_for("faculty"))

@app.route("/student_logout")
def student_logout():
    session.clear()
    global current_student
    current_student = None
    return redirect(url_for("student"))


app.run(debug=True)
