from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.Users.as_view()),
    url(r'^/activation$',views.ActiveView.as_view()),
]