from django.contrib.auth import views
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('moodle.urls')),
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
]
