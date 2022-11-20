from django.urls import path

from app.core.views import LoginUser, logout_user


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
