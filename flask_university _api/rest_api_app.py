import os
import psycopg2
from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from flasgger import swag_from, Swagger
from dotenv import load_dotenv

from app import (filter_groups_by_students_count, filter_students_by_name_of_course, remove_student_from_course,
                 remove_student_by_student_id, add_student_on_course, add_new_student)

load_dotenv()
user = os.getenv("DB_LOGIN")
password = os.getenv("DB_PASSWORD")
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
conn = psycopg2.connect(
    dbname="university",
    user=f"{user}",
    password=f"{password}",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


class GetGroupsByQuantity(Resource):
    @swag_from('./swagger_docs/groups_by_quantity.yml')
    def get(self):
        numbers = request.args.get('quantity', type=str, default='30')
        if not numbers.isnumeric():
            abort(400, "Write only numbers")
        answer = filter_groups_by_students_count(numbers)
        if not answer:
            abort(400, f'less {numbers} does`t exist')
        cursor.close()
        conn.close()
        return jsonify(answer)


class GetStudentsByCourse(Resource):
    @swag_from('./swagger_docs/students_by_course.yml')
    def get(self):
        course = request.args.get('course', type=str)
        answer = filter_students_by_name_of_course(course)
        cursor.close()
        conn.close()
        return jsonify(answer)


class PutStudent(Resource):
    @swag_from('./swagger_docs/put_student.yml')
    def put(self):
        first_name = request.args.get('First name', type=str)
        last_name = request.args.get('Last name', type=str)
        if not first_name.isalpha() or not last_name.isalpha():
            cursor.close()
            conn.close()
            abort(400, 'You need write in first name and last name only letters')
        answer = add_new_student(first_name, last_name)
        cursor.close()
        conn.close()
        return jsonify(answer)


class DeleteStudentId(Resource):
    @swag_from('./swagger_docs/delete_student_by_id.yml')
    def delete(self):
        try:
            student_id = request.args.get('Student ID', type=str)
            answer = remove_student_by_student_id(student_id)
            cursor.close()
            conn.close()
            return jsonify(answer)
        except:
            cursor.close()
            conn.close()
            return jsonify("Somethings wrong")


class AddStudentOnCourse(Resource):
    @swag_from('./swagger_docs/add_student_on_course.yml')
    def put(self):
        try:
            student_id = request.args.get('student_id', type=str)
            course_name = request.args.get('course_name', type=str)
            add_student_on_course(student_id, course_name)
            cursor.close()
            conn.close()
            return jsonify(f'Student with ID {student_id}, was added on curse {course_name}')
        except:
            cursor.close()
            conn.close()
            return jsonify("Somethings wrong")


class DeleteStudentFromCourse(Resource):
    @swag_from('./swagger_docs/delete_student_from_course.yml')
    def delete(self):
        try:
            student_id = request.args.get('student_id', type=str)
            course_name = request.args.get('course_name', type=str)
            remove_student_from_course(student_id, course_name)
            cursor.close()
            conn.close()
            return jsonify(f'Student with ID {student_id}, was delete from curse {course_name}')
        except:
            cursor.close()
            conn.close()
            return jsonify("Somethings wrong")


api.add_resource(GetGroupsByQuantity, '/groups/')
api.add_resource(GetStudentsByCourse, '/students/course/')
api.add_resource(PutStudent, '/students/')
api.add_resource(DeleteStudentId, '/students/delete/')
api.add_resource(AddStudentOnCourse, '/course/add/')
api.add_resource(DeleteStudentFromCourse, '/course/delete/')


if __name__ == "__main__":
    app.run(debug=True)
