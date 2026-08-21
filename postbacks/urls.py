from django.urls import path
from . import views

app_name = 'postbacks'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/new/', views.campaign_create, name='campaign_create'),
    path('campaign/<slug:slug>/', views.campaign_detail, name='campaign_detail'),
    path('campaign/<slug:slug>/edit/', views.campaign_edit, name='campaign_edit'),
    path('campaign/<slug:slug>/export.<str:fmt>', views.export_events, name='export'),
    path('events/', views.event_list, name='event_list'),
    path('postback/<slug:slug>/<str:status>/', views.receive_postback, name='receive'),
]
