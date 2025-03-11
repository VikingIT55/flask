import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
user = os.getenv("DB_LOGIN")
password = os.getenv("DB_PASSWORD")
conn = psycopg2.connect(
    dbname="university",
    user=f"{user}",
    password=f"{password}",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


def filter_groups_by_students_count(value, cur=cursor):
    cur.execute("SELECT group_id, COUNT(student_id) as number_of_students FROM students "
                "GROUP BY group_id "
                f"HAVING COUNT(student_id) <= {value} "
                "ORDER BY number_of_students DESC")
    return cur.fetchall()


def filter_students_by_name_of_course(name_of_curse, cur=cursor):
    name_of_curse = name_of_curse.capitalize()
    cur.execute("SELECT s.first_name, s.last_name, c.name as name_of_course "
                "FROM courses_students cs "
                "INNER JOIN students s "
                "ON s.student_id=cs.student_id "
                "INNER JOIN courses c "
                "ON c.course_id=cs.course_id "
                f"WHERE c.name = '{name_of_curse}'")
    return cur.fetchall()


def add_new_student(first_name, last_name, cur=cursor):
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()
    cur.execute("INSERT INTO students (first_name, last_name) "
                f"VALUES ('{first_name}', '{last_name}') ")
    conn.commit()
    cur.execute('SELECT student_id, first_name, last_name FROM students')
    return cur.fetchall()[-1]


def remove_student_by_student_id(student_id, cur=cursor):
    cur.execute(f"DELETE FROM courses_students WHERE student_id={student_id}")
    cur.execute(f"DELETE FROM students WHERE student_id={student_id}")
    conn.commit()
    cur.execute(f'SELECT student_id FROM students WHERE student_id={student_id}')
    return cur.fetchall()


def add_student_on_course(student_id, course_name, cur=cursor):
    cur.execute("INSERT INTO courses_students (student_id, course_id) "
                f"VALUES ({student_id}, (SELECT course_id FROM courses WHERE name='{course_name}'))")
    conn.commit()


def remove_student_from_course(student_id, course_name, cur=cursor):
    cur.execute("DELETE FROM courses_students "
                f"WHERE student_id={student_id} "
                f"AND course_id=(SELECT course_id FROM courses WHERE name='{course_name}')")
    conn.commit()
