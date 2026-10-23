from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_documents, name='my_documents'),
    path('create/', views.create_document, name='create_document'),
    path('<int:doc_id>/', views.document_detail, name='document_detail'),
    path('<int:doc_id>/edit/', views.edit_document, name='edit_document'),
    path('<int:doc_id>/delete/', views.delete_document, name='delete_document'),

]

