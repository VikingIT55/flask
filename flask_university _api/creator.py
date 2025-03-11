import os
import random
import psycopg2
import string
from faker import Faker
from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv


fake = Faker()
load_dotenv()
user = os.getenv("DB_LOGIN")
password = os.getenv("DB_PASSWORD")
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost/university")
Base.metadata.create_all(engine)
conn = psycopg2.connect(
    dbname="university",
    user=f"{user}",
    password=f"{password}",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


def create_groups():
    groups = []
    for _ in range(10):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=2))
        group_name = f"{letters}-{numbers}"
        groups.append(group_name)

    courses = {'Math': 'Mathematics explores the fundamental principles of numbers, shapes, and patterns.',
               'Biology': 'Biology is the study of living organisms and their interactions with the environment.',
               'Physics': 'Physics is the study of matter, energy, and the fundamental forces that govern the universe.',
               'Chemistry': 'Chemistry is the study of matter and its properties, composition, structure, '
                            'and changes it undergoes during chemical reactions.',
               'History': 'History is the study of past events, societies, cultures, and civilizations.',
               'Literature': 'Literature is the study of written works, including novels, poems, plays, and essays, '
                             'that reflect human experiences, values, and cultures',
               'Computer science': 'Computer Science is the study of algorithms, computation,'
                                   ' and information processing.',
               'Art': 'Art is the expression of human creativity and imagination through various forms and mediums',
               'Music': 'Music is the art of organizing sounds in time to create melody, harmony, rhythm, and '
                        'expression. ',
               'Geography': "Geography is the study of Earth's landscapes, environments,"
                            " and the relationships between people and their surroundings."}


    first_names = [fake.first_name() for _ in range(20)]
    last_names = [fake.last_name() for _ in range(20)]
    students = [(fake.random_element(first_names), fake.random_element(last_names)) for _ in range(200)]

    for group_name in groups:
        cursor.execute("INSERT INTO groups (name) VALUES (%s)", (group_name,))

    for course_name, description in courses.items():
        cursor.execute("INSERT INTO courses (name, description) VALUES (%s, %s)", (course_name, description))

    for first_name, last_name in students:
        cursor.execute("INSERT INTO students (group_id, first_name, last_name) VALUES (%s, %s, %s)",
                       (random.choice(groups), first_name, last_name))

    cursor.execute("CREATE TABLE courses_students(student_id INTEGER REFERENCES students(student_id),"
                   "course_id INTEGER REFERENCES courses(course_id),"
                   "CONSTRAINT courses_students_pk PRIMARY KEY(course_id, student_id))")
    for id in range(1, len(students)+1):
        course = random.sample(range(1, 11), random.randint(1, 3))
        if len(course) == 1:
            cursor.execute("INSERT INTO courses_students (student_id, course_id) "
                           f"VALUES ({id},{course[0]})")
        elif len(course) == 2:
            cursor.execute("INSERT INTO courses_students (student_id, course_id) VALUES "
                           f"({id},{course[0]}), ({id},{course[1]})")
        else:
            cursor.execute("INSERT INTO courses_students (student_id, course_id)"
                           f" VALUES ({id},{course[0]}), ({id},{course[1]}), ({id},{course[2]})")

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    create_groups()
