from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from users import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dash', views.dash, name='dash'),
    path('login', views.user_login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('blog', views.blog, name='blog'),
    path('blogpost/<pk>',views.blogpost, name='blogpost'),
    path('appointment/<pk>',views.create_appointment,name="appointment"),
    path('appointments_list',views.appointments_list,name="appointments_list"),
    path('appointment_details/<pk>',views.appointment_details,name="appointment_details")
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)