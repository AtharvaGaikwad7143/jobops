# from django.urls import path

# from .views import JobDetailView, JobListCreateView


# urlpatterns = [
#     path("", JobListCreateView.as_view()),
#     path("<int:pk>/", JobDetailView.as_view()),
# ]

from django.urls import path

from .views import JobDetailView, JobListCreateView


urlpatterns = [
    path("", JobListCreateView.as_view()),
    path("<int:pk>/", JobDetailView.as_view()),
]