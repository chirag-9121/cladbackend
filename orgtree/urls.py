from django.urls import path
from .views import NodeListView, NodeDetailView

app_name = "orgtree"

urlpatterns = [
    path('nodes/', NodeListView.as_view(), name='node-list'),
    path('nodes/<int:pk>/', NodeDetailView.as_view(), name='node-detail'),
]
