import pytest
from rest_framework.test import APIClient
from model_bakery import baker

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

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    data = {'name': 'course2'}
    response = client.post('/api/v1/courses/', data=data)
    res_json = response.json()

    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    assert res_json['name'] == data['name']

@pytest.mark.django_db
def test_update_course(client, factory_course):
    courses = factory_course(_quantity=10)
    id_course = courses[0].id
    data = {'name': 'course3'}
    response = client.patch(f'/api/v1/courses/{id_course}/', data=data)

    assert response.status_code == 200
    assert Course.objects.filter(id=id_course)[0].name == data['name']

@pytest.mark.django_db
def test_delete_course(client, factory_course):
    courses = factory_course(_quantity=10)
    count = Course.objects.count()
    id_course = courses[4].id

    response = client.delete(f'/api/v1/courses/{id_course}/')

    assert response.status_code == 204
    assert count - 1 == Course.objects.count()

@pytest.mark.django_db
def test_get_one_course(client, factory_course):
    courses = factory_course(_quantity=1)
    id_course = courses[0].id

    response = client.get(f'/api/v1/courses/{id_course}/')
    res_json = response.json()

    assert response.status_code == 200
    assert Course.objects.filter(id=id_course)[0].name == res_json['name']

@pytest.mark.django_db
def test_get_list_courses(client, factory_course):
    courses = factory_course(_quantity=20)

    response = client.get('/api/v1/courses/')
    res_json = response.json()

    assert response.status_code == 200
    assert len(res_json) == len(courses)
    for i, course in enumerate(res_json):
        assert course['name'] == courses[i].name

@pytest.mark.django_db
def test_filter_courses_id(client, factory_course):
    courses = factory_course(_quantity=10)
    id_course = courses[5].id
    data = {'id': id_course}

    response = client.get(f'/api/v1/courses/', data=data)
    res_json = response.json()

    assert response.status_code == 200
    assert res_json[0]['id'] == id_course

@pytest.mark.django_db
def test_filter_course_name(client, factory_course, settings):
    courses = factory_course(_quantity=10)
    name_course = courses[5].name
    data = {'name': name_course}

    response = client.get(f'/api/v1/courses/', data=data)
    res_json = response.json()

    assert response.status_code == 200
    assert res_json[0]['name'] == name_course
    assert Course.objects.filter(name=name_course)[0].name == res_json[0]['name']

@pytest.mark.parametrize(
    ['num_students', 'answer'],
    (
        (1, 201),
        (20, 201),
        (22, 400)
    )
)
@pytest.mark.django_db
def test_students_limit(client, factory_student, num_students, answer, settings):
    students = factory_student(_quantity=num_students)
    id_students = [student.id for student in students]
    data = {'name': 'TestCourse', 'students': id_students}
    settings.MAX_STUDENTS_PER_COURSE = 20
    response = client.post('/api/v1/courses/', data=data)

    assert response.status_code == answer
    assert settings.MAX_STUDENTS_PER_COURSE
    assert settings.MAX_STUDENTS_PER_COURSE == 20

@pytest.mark.parametrize(
    ['num_students', 'valid'],
    (
        (1, True),
        (30, True),
        (32, False)
    )
)
@pytest.mark.django_db
def test_students_limit_without_db(num_students, valid, settings):
    res = num_students <= settings.MAX_STUDENTS_PER_COURSE

    assert res is valid
