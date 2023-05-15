from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'course'

urlpatterns = [

    path('answer/<lession_id>', views.answer, name='answer'),
    path('yes_no/<yes_or_no>/<answer_id>', views.yes_no, name='yes_no'),

    path('enter/<course_id>', views.enter, name='enter'),
    path('cabinet', views.cabinet, name='cabinet'),
    
    path('lessions/<course_id>', views.lessions, name='lessions'),

    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    path('', views.index, name='index'),

    path('<path>', views.table, name='table'),
    
    path('<path>/create', views.create, name='create'),
    path('<path>/delete/<id>', views.delete, name='delete'),
    path('<path>/update/<id>', views.update, name='update'),

    path('courses/<id>', views.course, name='course'),
]