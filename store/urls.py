from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views 

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('product/<int:pk>',views.product,name='product'),
    path('category/<str:cat>',views.category,name='category'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
