from . import views
from django.conf.urls import url

app_name = 'webpage'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^register/', views.register_view, name='register'),
]
