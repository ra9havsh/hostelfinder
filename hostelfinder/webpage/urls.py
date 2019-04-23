from . import views
from django.conf.urls import url

app_name = 'homepage'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
]
