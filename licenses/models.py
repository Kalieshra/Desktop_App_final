from django.db import models


class Channel(models.Model):
    name = models.CharField('اسم القناة', max_length=255)
    date = models.DateField('التاريخ', null=True, blank=True)
    created_by = models.CharField('أنشئ بواسطة', max_length=255, blank=True)
    is_accepted = models.BooleanField('مقبول', default=False)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'قناة'
        verbose_name_plural = 'القنوات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class PlaceLicense(models.Model):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE,
        related_name='place_licenses', verbose_name='القناة'
    )
    license_duration = models.CharField('مدة الترخيص', max_length=255, blank=True)
    date_from = models.DateField('تاريخ من', null=True, blank=True)
    date_to = models.DateField('تاريخ إلى', null=True, blank=True)
    is_paid = models.BooleanField('تم السداد', default=False)
    is_accepted = models.BooleanField('مقبول', default=False)
    attachment = models.FileField('المرفق', upload_to='licenses/place/%Y/%m/', blank=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'ترخيص مكاني'
        verbose_name_plural = 'التراخيص المكانية'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.channel.name} - ترخيص مكاني"


class PersonalLicense(models.Model):
    CATEGORY_CHOICES = [
        ('خبير وقاية', 'خبير وقاية'),
        ('مستخدم', 'مستخدم'),
        ('فني', 'فني'),
        ('مساعد فني', 'مساعد فني'),
    ]

    LICENSE_TYPE_CHOICES = [
        ('جديد', 'جديد'),
        ('تجديد', 'تجديد'),
        ('تعديل', 'تعديل'),
    ]

    DURATION_CHOICES = [
        ('شهر', 'شهر'),
        ('سنة', 'سنة'),
        ('سنتين', 'سنتين'),
        ('3 سنوات', '3 سنوات'),
    ]

    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE,
        related_name='personal_licenses', verbose_name='القناة'
    )
    applicant_name = models.CharField('اسم المتقدم', max_length=255)
    category = models.CharField('الفئة', max_length=100, choices=CATEGORY_CHOICES, blank=True)
    job = models.CharField('الوظيفة', max_length=255, blank=True)
    phone = models.CharField('رقم الهاتف', max_length=50, blank=True)
    license_type = models.CharField('نوع الترخيص', max_length=100, choices=LICENSE_TYPE_CHOICES, blank=True)
    date_from = models.DateField('تاريخ من', null=True, blank=True)
    date_to = models.DateField('تاريخ إلى', null=True, blank=True)
    license_duration = models.CharField('مدة الترخيص', max_length=100, choices=DURATION_CHOICES, blank=True)
    is_paid = models.BooleanField('تم السداد', default=False)
    is_accepted = models.BooleanField('مقبول', default=False)
    attachment = models.FileField('المرفق', upload_to='licenses/personal/%Y/%m/', blank=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'ترخيص شخصي'
        verbose_name_plural = 'التراخيص الشخصية'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.applicant_name} - {self.channel.name}"


class Inspection(models.Model):
    AUTHORITY_CHOICES = [
        ('تفتيش الوكالة', 'تفتيش الوكالة'),
        ('تفتيش هيئة الرقابة النووية والإشعاعية', 'تفتيش هيئة الرقابة النووية والإشعاعية'),
    ]

    RESULT_CHOICES = [
        ('استيفاء متطلبات', 'استيفاء متطلبات'),
        ('ملاحظات', 'ملاحظات'),
        ('توصيات', 'توصيات'),
        ('اشتراطات', 'اشتراطات'),
        ('تقرير', 'تقرير'),
        ('إجراءات تصحيحية', 'إجراءات تصحيحية'),
    ]

    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE,
        related_name='inspections', verbose_name='القناة'
    )
    inspector_name = models.CharField('اسم المفتش', max_length=255)
    job = models.CharField('الوظيفة', max_length=255, blank=True)
    authority = models.CharField('جهة التفتيش', max_length=255, choices=AUTHORITY_CHOICES, blank=True)
    visit_date = models.DateField('تاريخ الزيارة', null=True, blank=True)
    result = models.CharField('النتيجة', max_length=255, choices=RESULT_CHOICES, blank=True)
    is_accepted = models.BooleanField('مقبول', default=False)
    attachment = models.FileField('المرفق', upload_to='licenses/inspection/%Y/%m/', blank=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'تفتيش'
        verbose_name_plural = 'التفتيشات'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.inspector_name} - {self.channel.name}"
