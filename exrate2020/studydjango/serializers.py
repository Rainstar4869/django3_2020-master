from rest_framework import serializers
from .models import Student, School


class SchoolSerializer(serializers.ModelField):
    class Meta:
        model = School
        fields = "__all__"


class StudentSerializers(serializers.ModelSerializer):
    school = serializers.SlugRelatedField(read_only=True, slug_field="name")
    school_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Student
        fields = ("id", "name", "age", "school", "school_id")
        read_only_fields = ("id",)

    def create(self, validated_data):
        school_id = validated_data.pop("school_id")
        school = School.objects.filter(pk=school_id).first()
        if school:
            validated_data["school"] = school

        student = Student.objects.create(**validated_data)

        return student
