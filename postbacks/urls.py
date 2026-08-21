from django.urls import path
from . import views

app_name = 'postbacks'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('campaign/<slug:slug>/', views.campaign_detail, name='campaign_detail'),
    path('campaign/<slug:slug>/export.<str:fmt>', views.export_events, name='export'),
    path('postback/<slug:slug>/<str:status>/', views.receive_postback, name='receive'),
]
