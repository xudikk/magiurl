from django.urls import path
from app.views import index, shorten_url, go_to, qr_short_url, logout_view, about, dashboard

urlpatterns = [
    path('', index, name='home'),
    path('logout/', logout_view, name='logout'),
    path('about/', about, name='about'),

    path('dashboard/', dashboard, name='dashboard'),
    path('user_urls/<int:user_id>/', dashboard, name='user_urls'),
    path('user_urls/<null_user>/', dashboard, name='null_users'),

    path('short/', shorten_url, name='short'),
    path('qr_short/', qr_short_url, name='qr_short'),

    path('go/<str:pk>/', go_to, name='go')
]
