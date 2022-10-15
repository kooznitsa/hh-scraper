from django.contrib import admin
from django.urls import path
from api.views import JobListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', JobListView.as_view()),
]