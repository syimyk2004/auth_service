from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from accounts.models import Profile
from .models import Company
from .serializers import ProfileSerializer, CompanySerialzier
from rest_framework import generics


class EmployeeDepartmentAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        employees = Profile.objects.filter(department=pk)
        serializers = ProfileSerializer(employees, many=True)
        from rest_framework.response import Response
        return Response(serializers.data, status=status.HTTP_200_OK)


class CompanyApiView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerialzier
