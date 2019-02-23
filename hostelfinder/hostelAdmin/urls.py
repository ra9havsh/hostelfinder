from . import views
from django.conf.urls import url

app_name = 'hostelAdmin'

urlpatterns = [
    url(r'^$', views.HostelView.as_view(), name='hostels'),
    url(r'^hostels/$', views.HostelView.as_view(), name='hostels'),
    url(r'^hostels/(?P<pk>[0-9]+)/$', views.HostelDetailView.as_view(), name='hostel_details'),
    url(r'^hostels/add/$', views.HostelCreate.as_view(), name='hostel_add'),
    url(r'^customers/$', views.customers, name='customers')
]
