from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Document
@login_required
def my_documents(request):
    docs = Document.objects.filter(owner=request.user)
    return render(request, 'documents/list.html', {'documents': docs})
@login_required
def document_detail(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    # Authorization: only owner or staff (admin) can view
    if doc.owner != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this document.")
    return render(request, 'documents/detail.html', {'document': doc})