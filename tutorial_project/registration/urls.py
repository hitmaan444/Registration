from django.urls import path
from . import views

#{% static 'css/styles.css' %}
app_name = "registration"

urlpatterns = [
    path("", views.index, name="index"),
    path('login', views.login_page, name="login"),
    path('registration', views.registrationView, name='registration'),
    path('logout/', views.logoutView, name='logout'),
    path('editProfile', views.edit_profile, name='editProfile'),
    path('changePassword', views.change_password, name='changePassword'),
    path("activate/<slug:uuid>", views.user_activate, name="activate"),


]