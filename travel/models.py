from django.db import models


class TravelType(models.Model):
    """Travel/course type lookup table (e.g., دورة تدريبية, ورشة عمل, مؤتمر)"""
    name = models.CharField(max_length=100, unique=True, verbose_name='اسم النوع')
    description = models.TextField(blank=True, verbose_name='الوصف')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'نوع السفرية'
        verbose_name_plural = 'أنواع السفريات'
        ordering = ['name']

    def __str__(self):
        return self.name


class Travel(models.Model):
    TITLE_CHOICES = [
        ('أ.د', 'أ.د'),
        ('أ.م.د', 'أ.م.د'),
        ('دكتور', 'دكتور'),
        ('م. مساعد', 'م. مساعد'),
        ('مهندس', 'مهندس'),
        ('أخصائي', 'أخصائي'),
        ('فني', 'فني'),
        ('عامل/ خدمات', 'عامل/ خدمات'),
        ('دبلوم', 'دبلوم'),
    ]

    COURSE_TYPE_CHOICES = [
        ('دورة تدريبية', 'دورة تدريبية'),
        ('ورشة عمل', 'ورشة عمل'),
        ('فعالية', 'فعالية'),
        ('اجتماع فني', 'اجتماع فني'),
        ('المدرسة الروسية', 'المدرسة الروسية'),
        ('دورة مشتركة', 'دورة مشتركة'),
    ]

    DEPARTMENT_CHOICES = [
        ('مفاعل الثاني', 'مفاعل الثاني'),
        ('مصنع الوقود النووي', 'مصنع الوقود النووي'),
        ('مصنع النظائر المشعة', 'مصنع النظائر المشعة'),
        ('مصنع اليورانيوم', 'مصنع اليورانيوم'),
    ]

    name = models.CharField('الاسم', max_length=255)
    title = models.CharField('اللقب', max_length=100, choices=TITLE_CHOICES, blank=True)
    department = models.CharField('الجهة', max_length=255, choices=DEPARTMENT_CHOICES, blank=True)
    position = models.CharField('الوظيفة', max_length=255, blank=True)
    travel_type = models.ForeignKey(
        TravelType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='travels',
        verbose_name='نوع السفرية'
    )
    course_type = models.CharField('نوع الدورة (قديم)', max_length=100, choices=COURSE_TYPE_CHOICES, blank=True)
    course_name = models.CharField('اسم الدورة التدريبية', max_length=500, blank=True)
    course_location = models.CharField('مكان إنعقاد الدورة', max_length=255, blank=True)
    date_from = models.DateField('تاريخ من', null=True, blank=True)
    date_to = models.DateField('تاريخ إلى', null=True, blank=True)
    deadline = models.DateField('DadLine', null=True, blank=True)
    followup = models.CharField('المتابعة', max_length=255, blank=True)
    attachment = models.FileField('المرفق', upload_to='attachments/%Y/%m/', blank=True)
    event_code = models.CharField('Event Code', max_length=100, blank=True)
    total_travels = models.CharField('إجمالي سفريات', max_length=100, blank=True)
    is_accepted = models.BooleanField('مقبول', default=False)

    # New fields
    aps = models.BooleanField('APS', default=False)
    publish_committee = models.BooleanField('لجنه النشر', default=False)
    visual_presentation = models.BooleanField('عرض مرئي', default=False)
    sader = models.IntegerField('صادر', null=True, blank=True)

    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'سفرية'
        verbose_name_plural = 'السفريات'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.course_location}"
