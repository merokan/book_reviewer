from django.conf.urls import url 
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.success), 
    url(r'^books/add$', views.add),
    url(r'^books/process$', views.process),
    url(r'^books/(?P<book_id>\d+)/add_review$', views.add_review),
    url(r'^books/(?P<book_id>\d+)$', views.book),
    url(r'^users/(?P<user_id>\d+)$', views.user),
    url(r'^users/(?P<review_id>\d+)/delete$', views.delete_review),
    url(r'^logout$', views.logout)
]