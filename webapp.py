import hackbright_app
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    row2 = hackbright_app.get_student_report(student_github)

    return render_template("student_info.html", first_name=row[0], last_name=row[1], github=row[2], list_of_grades=row2)

@app.route("/project")
def get_project_grades():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    rows = hackbright_app.get_project_grades(project_title)
    project_info = hackbright_app.get_project_by_title(project_title)
    print "PROJECT INFO", project_info
    title = project_info[0]
    description = project_info[1]
    max_grade = project_info[2]
    
    return render_template("project_grades.html", student_grades=rows, title=title, description=description, max_grade=max_grade)

@app.route("/new_student", methods=["POST"])
def make_new_student():
    hackbright_app.connect_to_db()
    new_firstname = request.form.get("firstname")
    new_lastname = request.form.get("lastname")
    new_github = request.form.get("github")
    hackbright_app.make_new_student(new_firstname, new_lastname, new_github)

    return redirect("/student?github=%s" % new_github)

@app.route("/new_project", methods=["POST"])
def make_new_project():
    hackbright_app.connect_to_db()
    title = request.form.get("project_title")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")
    hackbright_app.make_new_project(title, description, max_grade)

    return redirect("/project?project_title=%s" % title) 
    
@app.route("/assign_grade", methods=["POST"])
def assign_grade():
    hackbright_app.connect_to_db()
    student_github = request.form.get("github")
    title = request.form.get("title")
    grade = request.form.get("grade")
    hackbright_app.assign_grade(student_github, title, grade)

    return redirect("/student?github=%s" % student_github)


if __name__ == "__main__":
    app.run(debug=True)
