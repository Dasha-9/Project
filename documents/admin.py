from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'genre', 'original_language', 'uploaded_at']
    list_filter = ['genre', 'original_language', 'created_at']
    search_fields = ['title', 'full_text', 'subjects', 'key_themes']
    list_per_page = 20