from django.urls import path
from members.views import ListBoardView
# from django.contrib.auth.decorators import login_required

from . import views

app_name = 'members_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('people/all/', views.list_all, name='list_all'),
    path('board/', ListBoardView.as_view(), name='list_board'),
    path('members/active/', views.list_active, name='list_active'),
    path('members/inactive/', views.list_inactive, name='list_inactive'),
    path('needs_review/', views.needs_review, name='needs_review'),
    path('person/<int:person_id>/', views.show_person, name='show_person'),
    path('edit_person/<int:person_id>/', views.edit_person, name='edit_person'),
    path('save_person/', views.save_person, name='save_person'),
    path('save_address/', views.save_address, name='save_address'),
    path('member/<int:member_id>/', views.show_member, name='show_member'),
    path('edit_member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('save_member/', views.save_member, name='save_member'),
    path('search/', views.search_results, name='search_results'),
    path('board/committees/', views.list_committees, name='list_committees'),
]
