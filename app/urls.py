from django.urls import path
from app.views import index, shorten_url, go_to, qr_short_url, logout_view

urlpatterns = [
    path('', index, name='home'),
    path('logout/', logout_view, name='logout'),
    path('short/', shorten_url, name='short'),
    path('qr_short/', qr_short_url, name='qr_short'),
    path('go/<str:pk>/', go_to, name='go')
]
