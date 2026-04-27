from django.db import models

class Document(models.Model):
    # Список жанров
    GENRE_CHOICES = [
        ('declaration', 'Декларация'),
        ('communique', 'Коммюнике'),
        ('joint_statement', 'Совместное заявление'),
        ('protocol', 'Протокол'),
        ('charter', 'Хартия'),
        ('agreement', 'Соглашение'),
        ('treaty', 'Договор'),
        ('memorandum', 'Меморандум'),
        ('official_message', 'Официальное сообщение'),
    ]
    
    INSTITUTION_CHOICES = [
        ('sco', 'ШОС'),
        ('brics', 'БРИКС'),
        ('eas', 'ЕАС'),
    ]

    # Список политико-дискурсивных типов
    DISCOURSE_TYPE_CHOICES = [
        ('programmatic', 'Программный'),
        ('normative', 'Нормативный'),
        ('declarative', 'Декларативный'),
        ('strategic', 'Стратегический'),
        ('operational', 'Операционный'),
    ]
    
    # Языки
    LANGUAGE_CHOICES = [
        ('russian', 'Русский'),
        ('english', 'Английский'),
        ('chinese', 'Китайский'),
        ('french', 'Французский'),
        ('german', 'Немецкий'),
        ('spanish', 'Испанский'),
        ('arabic', 'Арабский'),
    ]
    
    # === ОБЯЗАТЕЛЬНЫЕ ПОЛЯ (только самые важные) ===
    title = models.CharField(max_length=500, verbose_name="Название документа")
    full_text = models.TextField(verbose_name="Полный текст документа", blank=True, null=True)
    created_at = models.DateField(verbose_name="Дата создания", blank=True, null=True)
    
    # === ОПЦИОНАЛЬНЫЕ ПОЛЯ (можно не заполнять) ===
    event_context = models.CharField(
        max_length=500, 
        verbose_name="Событие / обстоятельства создания", 
        blank=True, 
        null=True,
        help_text="Например: Саммит БРИКС 2023 (необязательно)"
    )
    
    place_created = models.CharField(
        max_length=300, 
        verbose_name="Место создания", 
        blank=True, 
        null=True,
        help_text="Город, страна (необязательно)"
    )
    
    subjects = models.TextField(
        verbose_name="Субъекты (участники, акторы)", 
        blank=True, 
        null=True,
        help_text="Список государств, лидеров, институтов (необязательно)"
    )
    
    genre = models.CharField(
        max_length=50, 
        choices=GENRE_CHOICES, 
        verbose_name="Жанр документа",
        blank=True, 
        null=True
    )
    
    key_themes = models.TextField(
        verbose_name="Ключевые темы (концепты)",
        blank=True, 
        null=True,
        help_text="Теги через запятую (необязательно)"
    )
    
    original_language = models.CharField(
        max_length=20, 
        choices=LANGUAGE_CHOICES, 
        verbose_name="Язык оригинала", 
        blank=True, 
        null=True,
        default='russian'
    )
    
    discourse_type = models.CharField(
        max_length=20,
        choices=DISCOURSE_TYPE_CHOICES,
        verbose_name="Политико-дискурсивный тип",
        blank=True,
        null=True
    )

    institution = models.CharField(
        max_length=10,
        choices=INSTITUTION_CHOICES,
        verbose_name="Институт",
        blank=True,
        null=True,
    )
    
    related_documents = models.ManyToManyField(
        'self',
        verbose_name="Связанные документы",
        blank=True,
        symmetrical=False,
    )
    
    has_translations = models.BooleanField(
        verbose_name="Наличие переводов", 
        default=False,
        blank=True
    )
    
    translation_languages = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        verbose_name="Язык перевода",
        blank=True,
        null=True,
    )

    translation_file = models.FileField(
        upload_to='documents/translations/%Y/%m/',
        verbose_name="Файл перевода (PDF, DOC, TXT)",
        blank=True,
        null=True,
    )

    original_file = models.FileField(
        upload_to='documents/%Y/%m/',
        verbose_name="Оригинальный документ (PDF, DOC, TXT)",
        blank=True,
        null=True,
        help_text="Загрузите оригинальный файл (необязательно)"
    )
    
    # Служебные поля
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки в систему")
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-created_at']
        # Добавляем индексы для быстрого поиска
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['genre']),
            models.Index(fields=['original_language']),
        ]
    
    def __str__(self):
        return self.title