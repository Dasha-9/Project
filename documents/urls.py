from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.DocumentListView.as_view(), name='document_list'),
    path('document/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('document/create/', views.DocumentCreateView.as_view(), name='document_create'),
    path('document/<int:pk>/edit/', views.DocumentUpdateView.as_view(), name='document_update'),
    path('document/<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document_delete'),
]