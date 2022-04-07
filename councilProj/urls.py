from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$',auth_views.LoginView.as_view(template_name="members/login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="members/welcome.html"), name='logout'),
    url(r'^admin-Ca7pJ6c0/', admin.site.urls),
    path('', include('members.urls')),
]
