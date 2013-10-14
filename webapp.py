import hackbright_app
from flask import Flask, render_template, request

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
    print rows
    
    return render_template("project_grades.html", student_grades=rows)

if __name__ == "__main__":
    app.run(debug=True)
