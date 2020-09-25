from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .models import Student
from .serializers import StudentSerializers
import json
import logging


logger = logging.getLogger("error")


class StudentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializers(instance=students, many=True)
        return Response(serializer.data)

    def post(self, request):
        # input_data = json.loads(request.body)
        # logger.error(input_data)
        serializer = StudentSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data)

        return Response({
            "result": "error",
            "errors": serializer.error_messages
        })
