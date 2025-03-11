import unittest

from rest_api_app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_groups_by_quantity(self):
        response = self.app.get('/groups/?quantity=30')
        self.assertEqual(response.status_code, 200)

    def test_get_students_by_course(self):
        response = self.app.get('/students/course/?course=Math')
        self.assertEqual(response.status_code, 200)

    def test_put_student(self):
        response = self.app.put('/students/?First%20name=John&Last%20name=Doe')
        self.assertEqual(response.status_code, 200)

    def test_delete_student_by_id(self):
        response = self.app.delete('/students/delete/?Student%20ID=1')
        self.assertEqual(response.status_code, 200)

    def test_add_student_on_course(self):
        response = self.app.put('/course/add/?student_id=2&course_name=Math')
        self.assertEqual(response.status_code, 200)

    def test_delete_student_from_course(self):
        response = self.app.delete('/course/delete/?student_id=2&course_name=Math')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
