from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Job
from .serializers import JobSerializer


class JobListCreateView(APIView):

    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            job = serializer.save()

            return Response(
                JobSerializer(job).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class JobDetailView(APIView):

    def get(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response(
                {"detail": "Job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSerializer(job)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response(
                {"detail": "Job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSerializer(
            job,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            job = serializer.save()
            return Response(JobSerializer(job).data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response(
                {"detail": "Job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        job.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )