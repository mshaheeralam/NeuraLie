from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.signin, name="login"),
    path('logout', views.signout, name="logout"),
    path('interview', views.interview, name="interview"),
    path('logs', views.logs, name="logs"),
    path('log', views.log, name="log"),
    path('demo', views.demo, name="demo"),
    path('record', views.record, name="record"),
    path('upload/', views.upload, name='upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)