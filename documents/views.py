from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Document
from .models import AuditLog
from django.shortcuts import redirect


@login_required
def my_documents(request):
    docs = Document.objects.filter(owner=request.user).order_by('-created_at')

    recent_logs = AuditLog.objects.filter(
        user=request.user
    ).select_related('document').order_by('-timestamp')[:5]

    context = {
        'documents': docs,
        'total_documents': docs.count(),
        'recent_logs': recent_logs,
    }

    return render(request, 'documents/list.html', context)
   
@login_required
def document_detail(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    # Authorization: only owner or staff (admin) can view
    if doc.owner != request.user and not request.user.is_staff:
        AuditLog.objects.create(user=request.user, document=doc, action='deny',
                                details='Unauthorized access attempt')
        return HttpResponseForbidden("You do not have permission to view this document.")
    AuditLog.objects.create(user=request.user, document=doc, action='view')
    return render(request, 'documents/detail.html', {'document': doc})
from django.shortcuts import redirect

@login_required
def create_document(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if not title or not content:
            return render(request, 'documents/create.html', {
                'error': 'Both title and content are required.',
            })
        doc = Document.objects.create(owner=request.user, title=title, content=content)
        AuditLog.objects.create(user=request.user, document=doc, action='create')
        return redirect('my_documents')
    return render(request, 'documents/create.html')

@login_required
def edit_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    
    # Only owner or admin can edit
    if doc.owner != request.user and not request.user.is_staff:
        AuditLog.objects.create(user=request.user, document=doc, action='deny',
                                details='Unauthorized edit attempt')
        return HttpResponseForbidden("You do not have permission to edit this document.")
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # Simple validation (add more as needed)
        if not title or not content:
            return render(request, 'documents/edit.html', {
                'document': doc,
                'error': 'Title and content cannot be empty.'
            })
        doc.title = title
        doc.content = content
        doc.save()
        AuditLog.objects.create(user=request.user, document=doc, action='edit')
        return redirect('document_detail', doc_id=doc.id)
    return render(request, 'documents/edit.html', {'document': doc})


@login_required
def delete_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)

    # Only owner or admin can delete
    if doc.owner != request.user and not request.user.is_staff:
        AuditLog.objects.create(user=request.user, document=doc, action='deny',
                                details='Unauthorized delete attempt')
        return HttpResponseForbidden("You do not have permission to delete this document.")

    if request.method == 'POST':
        AuditLog.objects.create(user=request.user, document=doc, action='delete')
        doc.delete()
        return redirect('my_documents')

    return render(request, 'documents/delete_confirm.html', {'document': doc})
