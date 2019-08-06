from . import views
from django.conf.urls import url

app_name = 'webpage'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^hostels/(?P<pk>[0-9]+)/$', views.HostelDetailView, name='hostel_details'),
    url(r'^hostels/edit/(?P<pk>[0-9]+)/$', views.HostelEditView, name='hostel_edit'),
    url(r'^hostel/(?P<pk>[0-9]+)/rate/(?P<rate>[1-5]+)/$', views.rating, name='rate'),
    url(r'^register_form/(?P<user_type>[a-zA-Z_]+)/$', views.register_form_view, name='register_form'),
    url(r'^login/', views.login_form_view, name='login'),
    url(r'^logout/', views.log_out, name='logout'),
    url(r'^search_bar/', views.search_bar, name='search_bar'),
    url(r'^user_page/hostel_owner/(?P<user_id>[0-9]+)/$', views.user_hostel_owner, name='user_hostel_owner'),
    url(r'^user_page/student/(?P<user_id>[0-9]+)/$', views.user_student, name='user_student'),
]
