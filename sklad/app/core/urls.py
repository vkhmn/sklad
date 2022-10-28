from django.urls import path

from app.core.views import (
    LoginUser, logout_user, ajax_view, search_result
)


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('ajax/', ajax_view, name='ajax'),
    path('search/', search_result, name='search')
]
