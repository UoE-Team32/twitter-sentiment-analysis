from django.shortcuts import render
from django.http import JsonResponse
from utils.twitter import create_session


def index(request):
    return render(request, "index.html")


def pie_chart_endpoint(request):
    return JsonResponse({"This is json": "true"})
