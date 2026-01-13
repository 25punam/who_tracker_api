# api/urls.py
from django.urls import path
from .views import CVERecordListAPIView,AllTasksStatusAPIView, FetchWHODataAPIView

urlpatterns = [
    path("fetch-who/", FetchWHODataAPIView.as_view()),
    path("cve-records/", CVERecordListAPIView.as_view()),
    path("task-status/", AllTasksStatusAPIView.as_view()),
]
