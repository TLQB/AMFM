from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.request import HttpRequest

# Create your views here.
class TestApi(APIView):
	def get(self, request: HttpRequest) -> Response:
		return Response({"test api": "data response ..."})

	def post(self, request: HttpRequest) -> Response:
		data: dict = request.data
		return Response(data)
