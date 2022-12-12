import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from django.conf import settings
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def factory_course():
    def course(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return course

@pytest.fixture
def factory_student():
    def student(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return student

# @pytest.mark.django_db
# def test_get_courses(client, course_factory):
#     # Arrange
# #    client = APIClient()
# #    Student.objects.create(name='Alex')
#     Course.objects.create(name='course1')
#     courses = course_factory(_quantity=10)
#
#
#     # Act
#     response = client.get('http://127.0.0.1:8000/api/v1/courses/')
#
#     # Assert
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == len(courses) + 1
#     assert data[0]['name'] == 'course1'
#     assert data[0]['id'] == 1

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    data = {'name': 'course2'}
    response = client.post('http://127.0.0.1:8000/api/v1/courses/', data=data)
    res_json = response.json()

    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    assert res_json['name'] == data['name']

@pytest.mark.django_db
def test_update_course(client, factory_course):
    courses = factory_course(_quantity=10)
    id_course = courses[0].id
    data = {'name': 'course3'}
    response = client.patch(f'http://127.0.0.1:8000/api/v1/courses/{id_course}/', data=data)

    assert response.status_code == 200
    assert Course.objects.filter(id=id_course)[0].name == data['name']

@pytest.mark.django_db
def test_delete_course(client, factory_course):
    courses = factory_course(_quantity=10)
    count = Course.objects.count()
    id_course = courses[4].id

    response = client.delete(f'http://127.0.0.1:8000/api/v1/courses/{id_course}/')

    assert response.status_code == 204
    assert count - 1 == Course.objects.count()

@pytest.mark.django_db
def test_get_one_course(client, factory_course):
    courses = factory_course(_quantity=1)
    id_course = courses[0].id

    response = client.get(f'http://127.0.0.1:8000/api/v1/courses/{id_course}/')
    res_json = response.json()

    assert response.status_code == 200
    assert Course.objects.filter(id=id_course)[0].name == res_json['name']

@pytest.mark.django_db
def test_get_list_courses(client, factory_course):
    courses = factory_course(_quantity=20)

    response = client.get('http://127.0.0.1:8000/api/v1/courses/')
    res_json = response.json()

    assert response.status_code == 200
    assert len(res_json) == len(courses)
    for i, course in enumerate(res_json):
        assert course['name'] == courses[i].name

@pytest.mark.django_db
def test_filter_courses_id(client, factory_course):
    courses = factory_course(_quantity=10)
    id_course = courses[5].id

    response = client.get(f'http://127.0.0.1:8000/api/v1/courses/?{id_course}/')
    res_json = response.json()

    assert response.status_code == 200
    assert res_json[5]['id'] == id_course

@pytest.mark.django_db
def test_filter_course_name(client, factory_course):
    courses = factory_course(_quantity=10)
    name_course = courses[5].name

    response = client.get(f'http://127.0.0.1:8000/api/v1/courses/?{name_course}/')
    res_json = response.json()

    assert response.status_code == 200
    assert res_json[5]['name'] == name_course
    assert Course.objects.filter(name=name_course)[0].name == res_json[5]['name']

@pytest.mark.parametrize(
    ['num_students', 'answer'],
    (
        (1, 201),
        (20, 201),
        (22, 400)
    )
)
@pytest.mark.django_db
def test_students_limit(client, factory_student, num_students, answer):
    students = factory_student(_quantity=num_students)
    id_students = [student.id for student in students]
    data = {'name': 'TestCourse', 'students': id_students}
    response = client.post('http://127.0.0.1:8000/api/v1/courses/', data=data)

    assert response.status_code == answer
    assert settings.MAX_STUDENTS_PER_COURSE == 20