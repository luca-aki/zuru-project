from django.contrib import admin
from django.urls import path, include
from links import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('u/', views.homeU, name='homeU'),
    path('accounts/', include('accounts.urls')),
    path('<link_id>', views.transfer, name='transfer'),
]
