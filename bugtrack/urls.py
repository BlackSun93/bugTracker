from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/<username>', views.profile, name='profile'),
    path("createBug/", views.createBug, name='createBug'),
    path("bugPage/<bugId>", views.bugPage, name="bugPage"),
    path('bugPage/newSolver/', views.newSolver, name='newSolver'),
    path('bugPage/newUpdate/', views.newUpdate, name='newUpdate'),
    path('bugPage/bugSolved/<bugId>', views.bugSolved, name='bugSolved'),
    path('bugPage/bugNotSolved/<bugId>', views.bugNotSolved, name='bugNotSolved'),
    path('finishedBugs', views.finishedBugList, name='finishedBugs'),
    path('notifications', views.notifications, name='notifications')


]