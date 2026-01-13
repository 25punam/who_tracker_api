from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django_celery_results.models import TaskResult
from .tasks import fetch_who_data_task
from .models import CVERecord
from .serializers import CVERecordSerializer
from .models import CeleryTaskTracker
from celery.result import AsyncResult


# Fetch WHO data → Celery task trigger API
class FetchWHODataAPIView(APIView):
    def post(self, request):
        task = fetch_who_data_task.delay()

        # Save task_id to tracker table
        CeleryTaskTracker.objects.create(task_id=task.id)

        return Response(
            {
                "message": "WHO data fetch started",
                "task_id": task.id
            },
            status=status.HTTP_202_ACCEPTED
        )

# All Task status check API
class AllTasksStatusAPIView(APIView):
    """
    Return all triggered Celery tasks and their live status + result
    """
    def get(self, request):
        tasks = CeleryTaskTracker.objects.all().order_by("-created_at")
        task_list = []

        for task in tasks:
            result = AsyncResult(task.task_id)
            task_list.append({
                "task_id": task.task_id,
                "status": result.status,     # PENDING / STARTED / SUCCESS / FAILURE
                "result": result.result      # None if task not complete
            })

        return Response(task_list, status=200)

# CVE records list (existing API)
class CVERecordListAPIView(ListAPIView):
    queryset = CVERecord.objects.all().order_by("-created_at")
    serializer_class = CVERecordSerializer
