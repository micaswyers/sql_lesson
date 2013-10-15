import hackbright_app
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def get_github():
    # hackbright_app.connect_to_db()
    # projects_list = hackbright_app.get_all_projects()
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

@app.route("/new_student")
def make_new_student():
    hackbright_app.connect_to_db()
    new_firstname = request.args.get("firstname")
    new_lastname = request.args.get("lastname")
    new_github = request.args.get("github")
    hackbright_app.make_new_student(new_firstname, new_lastname, new_github)

    return render_template("student_info.html", first_name=new_firstname, last_name=new_lastname, github=new_github)

@app.route("/new_project")
def make_new_project():
    hackbright_app.connect_to_db()
    title = request.args.get("project_title")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    hackbright_app.make_new_project(title, description, max_grade)

    return render_template("project_grades.html", title=title, description=description, max_grade=max_grade)

@app.route("/assign_grade")
def assign_grade():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    title = request.args.get("title")
    grade = request.args.get("grade")
    hackbright_app.assign_grade(student_github, title, grade)

    row = hackbright_app.get_student_by_github(student_github)
    row2 = hackbright_app.get_student_report(student_github)

    return render_template("student_info.html", first_name=row[0], last_name=row[1], github=student_github, list_of_grades=row2)


if __name__ == "__main__":
    app.run(debug=True)
