from rest_framework import serializers

from accounts.models import Profile
from company.models import SalaryIncrease, Company, Department


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)
    full_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Profile
        fields = ("email", "full_name", "salary",
                  "image", "department", "level")

    def update(self, instance, validated_data):
        instance.user = validated_data.get("user", instance.user)
        instance.image = validated_data.get("image", instance.image)
        instance.department = validated_data.get("department", instance.department)
        instance.salary = validated_data.get("salary", instance.salary)
        if validated_data.get("level") and instance.level != validated_data.get("level"):
            increase_salary = SalaryIncrease.objects.get(
                department=instance.department,
                level=validated_data.get("level")).salary_increment
            instance.level = validated_data.get("level", instance.level)
            instance.salary += increase_salary
        instance.save()
        return instance

class DepartmentSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class CompanySerialzier(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.departments.exists:
            representation["departments"] = DepartmentSerialzier(instance.departments.all(),
                                                                 many=True).data
        return representation