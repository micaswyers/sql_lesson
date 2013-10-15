import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    return row

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added new project: %s" % title

def get_student_grade(first_name, title):
    query = """SELECT Students.first_name, Grades.project_title, Grades.grade \
            FROM Students JOIN Grades ON Students.github = Grades.student_github\
            WHERE Students.first_name = ? AND Grades.project_title = ?"""
    DB.execute(query, (first_name, title))
    row = DB.fetchone()
    print """\
Student name: %s 
Project Title: %s 
Grade: %d""" % (row[0], row[1], row[2])

def assign_grade(student_github, project_title, grade):
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    

def get_student_report(student_github):
    query = """SELECT student_github, project_title, grade FROM Grades WHERE student_github = ?"""
    DB.execute(query, (student_github,))
    rows = DB.fetchall()
    return rows

def get_project_grades(project_title):
    print "TITLE", project_title
    query = """SELECT * FROM Grades WHERE project_title = ?"""
    DB.execute(query, (project_title, ))
    rows = DB.fetchall()
    return rows

def get_all_projects():
    query = """SELECT Title FROM Projects"""
    DB.execute(query)
    titles = DB.fetchall()
    return titles

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "title":
            get_project_by_title(*args)
        elif command == "new_project":
            title = tokens[1]
            description = " ".join(tokens[1:-1])
            max_grade = tokens[-1]
            make_new_project(title, description, max_grade)
        elif command == "get_grade":
            get_student_grade(*args)
        elif command == "assign_grade":
            assign_grade(*args)
        elif command == "student_report":
            get_student_report(*args)
        elif command == "project_grades":
            get_project_grades(*args)
        elif command == "projects":
            get_all_projects()

    CONN.close()

if __name__ == "__main__":
    main()
