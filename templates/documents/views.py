from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Document
from .forms import DocumentForm


class HomeView(TemplateView):
    template_name = 'documents/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_documents'] = Document.objects.order_by('-uploaded_at')[:6]
        context['total_documents'] = Document.objects.count()
        context['total_genres'] = Document.objects.exclude(genre__isnull=True).exclude(genre='').values('genre').distinct().count()
        context['total_languages'] = Document.objects.exclude(original_language__isnull=True).exclude(original_language='').values('original_language').distinct().count()
        context['docs_with_files'] = Document.objects.exclude(original_file='').exclude(original_file__isnull=True).count()

        genre_counts = Document.objects.exclude(genre__isnull=True).exclude(genre='').values('genre').annotate(count=Count('id'))
        genre_dict = {g: n for g, n in Document.GENRE_CHOICES}
        context['genre_stats'] = [(g['genre'], genre_dict.get(g['genre'], g['genre']), g['count']) for g in genre_counts]

        return context

# Эти страницы доступны всем (чтение)
class DocumentListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        search_query = self.request.GET.get('q')
        genre_filter = self.request.GET.get('genre')
        language_filter = self.request.GET.get('language')
        year_filter = self.request.GET.get('year')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(full_text__icontains=search_query) |
                Q(place_created__icontains=search_query)
            )
        
        if genre_filter:
            queryset = queryset.filter(genre=genre_filter)
        
        if language_filter:
            queryset = queryset.filter(original_language=language_filter)
        
        if year_filter:
            queryset = queryset.filter(created_at__year=year_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from datetime import datetime
        current_year = datetime.now().year
        
        context['genres'] = Document.GENRE_CHOICES
        lang_values = Document.objects.values_list('original_language', flat=True).distinct()
        lang_dict = dict(Document.LANGUAGE_CHOICES)
        context['languages'] = [(lang, lang_dict.get(lang, lang)) for lang in lang_values if lang]
        context['years'] = range(2000, current_year + 1)
        
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'genre': self.request.GET.get('genre', ''),
            'language': self.request.GET.get('language', ''),
            'year': self.request.GET.get('year', ''),
        }
        
        return context

# Чтение документа - доступно всем
class DocumentDetailView(DetailView):
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'

# СОЗДАНИЕ документа - только авторизованным пользователям
class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'
    success_url = reverse_lazy('documents:document_list')
    login_url = '/accounts/login/'  # Перенаправление на страницу входа

# РЕДАКТИРОВАНИЕ - только авторизованным
class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_form.html'
    success_url = reverse_lazy('documents:document_list')
    login_url = '/accounts/login/'

# УДАЛЕНИЕ - только авторизованным
class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'documents/document_confirm_delete.html'
    success_url = reverse_lazy('documents:document_list')
    login_url = '/accounts/login/'