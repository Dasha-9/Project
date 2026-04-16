from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название документа (обязательно)'}),
            'full_text': forms.Textarea(attrs={'rows': 20, 'class': 'form-control', 'placeholder': 'Введите текст документа (необязательно)'}),
            'created_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'event_context': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Саммит БРИКС 2023 (необязательно)'}),
            'place_created': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город, страна (необязательно)'}),
            'subjects': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Россия, Китай, Индия... (необязательно)'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'key_themes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'многополярность, регионализация... (необязательно)'}),
            'original_language': forms.Select(attrs={'class': 'form-control'}),
            'discourse_type': forms.Select(attrs={'class': 'form-control'}),
            'related_documents': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Ссылки на связанные документы (необязательно)'}),
            'has_translations': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'translation_languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'русский, английский, китайский (необязательно)'}),
            'original_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем все поля необязательными, кроме title
        for field_name, field in self.fields.items():
            if field_name != 'title':
                field.required = False