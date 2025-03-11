import unittest
import psycopg2
import testing.postgresql

from app import (filter_groups_by_students_count,
                 filter_students_by_name_of_course,
                 add_new_student,
                 remove_student_by_student_id,
                 add_student_on_course,
                 remove_student_from_course)


class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql(port=7654)
        self.conn = psycopg2.connect(self.postgresql.url())
        self.cursor = self.conn.cursor()
        # Create necessary tables
        self.cursor.execute("""
            CREATE TABLE students(
                student_id SERIAL PRIMARY KEY,
                group_id VARCHAR(50),
                first_name VARCHAR(50),
                last_name VARCHAR(50)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE courses (
                course_id SERIAL PRIMARY KEY,
                name VARCHAR(100)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE groups (
                name VARCHAR(5) PRIMARY KEY
            )
        """)
        self.cursor.execute("""
            CREATE TABLE courses_students (
                student_id INTEGER REFERENCES students(student_id),
                course_id INTEGER REFERENCES courses(course_id)
            )
        """)
        self.cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('John', 'Doe', 'SD-50')")
        self.cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('Alice', 'Smith', 'SD-52')")
        self.cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('Bob', 'Johnson', 'SD-52')")
        self.cursor.execute("INSERT INTO groups (name) VALUES ('SD-50')")
        self.cursor.execute("INSERT INTO groups (name) VALUES ('SD-51')")
        self.cursor.execute("INSERT INTO groups (name) VALUES ('SD-52')")
        self.cursor.execute("INSERT INTO courses (name) VALUES ('Math')")
        self.cursor.execute("INSERT iNTO courses (name) VALUES ('Biology')")
        self.cursor.execute("INSERT INTO courses_students (student_id, course_id) VALUES (1, 1)")
        self.cursor.execute("INSERT INTO courses_students (student_id, course_id) VALUES (2, 2)")
        self.cursor.execute("INSERT INTO courses_students (student_id, course_id) VALUES (3, 2)")
        self.conn.commit()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()
        self.postgresql.stop()

    def test_filter_groups_by_students_count(self):
        result = filter_groups_by_students_count(1, self.cursor)
        self.assertEqual(result, [('SD-50', 1)])

    def test_filter_students_by_name_of_course(self):
        result = filter_students_by_name_of_course('math', self.cursor)
        self.assertEqual(result, [('John', 'Doe', 'Math')])

    def test_add_new_student(self):
        result = add_new_student('Dmytro', 'Karasava', self.cursor)
        self.assertEqual(result, (4, 'Dmytro', 'Karasava'))

    def test_remove_student_by_student_id(self):
        self.cursor.execute('SELECT student_id from students WHERE student_id = 3')
        self.assertEqual(self.cursor.fetchall()[0][0], 3)
        result = remove_student_by_student_id(3, self.cursor)
        self.assertEqual(result, [])

    def test_add_student_on_course(self):
        self.cursor.execute("SELECT cs.student_id, c.name FROM courses_students cs "
                            "INNER JOIN courses c "
                            "ON c.course_id=cs.course_id "
                            "WHERE cs.student_id=1 and c.name='Biology'")
        self.assertEqual(self.cursor.fetchall(), [])
        result = add_student_on_course(1, 'Biology', self.cursor)
        self.cursor.execute("SELECT cs.student_id, c.name FROM courses_students cs "
                            "INNER JOIN courses c "
                            "ON c.course_id=cs.course_id "
                            "WHERE cs.student_id=1 and c.name='Biology'")
        self.assertEqual(self.cursor.fetchall(), [(1, 'Biology')])

    def test_remove_student_from_course(self):
        self.cursor.execute("SELECT cs.student_id, c.name FROM courses_students cs "
                            "INNER JOIN courses c "
                            "ON c.course_id=cs.course_id "
                            "WHERE cs.student_id=2 and c.name='Biology'")
        self.assertEqual(self.cursor.fetchall(), [(2, 'Biology')])
        result = remove_student_from_course(2, 'Biology', self.cursor)
        self.cursor.execute("SELECT cs.student_id, c.name FROM courses_students cs "
                            "INNER JOIN courses c "
                            "ON c.course_id=cs.course_id "
                            "WHERE cs.student_id=2 and c.name='Biology'")
        self.assertEqual(self.cursor.fetchall(), [])


if __name__ == '__main__':
    unittest.main()
