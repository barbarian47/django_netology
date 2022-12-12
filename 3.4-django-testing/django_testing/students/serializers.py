from rest_framework import serializers

from django.conf import settings
from .models import Course, Student


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, attrs):
        count = Student.objects.count()
        if count > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError('Limit 20 students per course')

        return super().validate(attrs)