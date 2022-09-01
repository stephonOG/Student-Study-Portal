from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views


app_name='dashboard'
urlpatterns = [
    path('', views.HomeView.as_view(), name='Home'),
    path('notes/', views.notesAdd, name='Notes'),
    path('homework/', views.HomeworkFormView, name='Home_work'),
    path('todo/', views.todo, name='todo'),
    path('youtube/', views.youtube, name='youtube'),
    path('books/', views.books, name='books'),
    path('dictionary/', views.dictionary, name='dictionary'),
    path('wiki/', views.wiki, name='wiki'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('notes-delete/<int:pk>/', views.deletenote, name='Notes_delete'),
    path('notes-detail/<int:pk>/', views.NoteDetailView.as_view(), name='Notes_detail'),
    path('homework-update/<int:pk>/', views.update_homework, name='homework_update'),
    path('homework-delete/<int:pk>/', views.delete_homework, name='homework_delete'),
    path('todo-delete/<int:pk>/', views.todo_delete, name='todo_delete'),
    path('todo-update/<int:pk>/', views.update_todo, name='todo_update'),
    path('login/', LoginView.as_view(), name='Login'),
    path('logout/', LogoutView.as_view(), name='Logout')
]