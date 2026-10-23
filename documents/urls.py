from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_documents, name='my_documents'),
    path('<int:doc_id>/', views.document_detail, name='document_detail'),
]
