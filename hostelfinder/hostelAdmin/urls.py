from . import views
from django.conf.urls import url

app_name = 'hostelAdmin'

urlpatterns = [
    url(r'^$', views.HostelView, name='hostels'),
    url(r'^hostels/$', views.HostelView, name='hostels'),
    url(r'^hostels/(?P<pk>[0-9]+)/$', views.HostelDetailView, name='hostel_details'),
    url(r'^hostels/edit/(?P<pk>[0-9]+)/$', views.HostelEditView, name='hostel_edit'),
    url(r'^hostels/delete/(?P<pk>[0-9]+)/$', views.HostelDeleteView, name='hostel_delete'),
    url(r'^hostels/add/$', views.formHostel, name='hostel_add'),
    url(r'^customers/$', views.customers, name='customers')
]
