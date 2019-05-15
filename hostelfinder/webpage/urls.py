from . import views
from django.conf.urls import url

app_name = 'webpage'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^register_form/(?P<user_type>[a-zA-Z_]+)/$', views.register_form_view, name='register_form'),
]
