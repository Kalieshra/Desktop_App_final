from django.db import models


class SupplyChannel(models.Model):
    name = models.CharField('اسم القناة', max_length=255)
    date = models.DateField('التاريخ', null=True, blank=True)
    created_by = models.CharField('أنشئ بواسطة', max_length=255, blank=True)
    is_accepted = models.BooleanField('مقبول', default=False)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'قناة توريد'
        verbose_name_plural = 'قنوات التوريد'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class BuyOrder(models.Model):
    supply_channel = models.ForeignKey(
        SupplyChannel, on_delete=models.CASCADE,
        related_name='buy_orders', verbose_name='القناة'
    )
    requester_name = models.CharField('اسم مقدم الطلب', max_length=255)
    job = models.CharField('الوظيفة', max_length=255, blank=True)
    location = models.CharField('المكان', max_length=255, blank=True)
    description = models.TextField('البيان', blank=True)
    estimated_value = models.DecimalField(
        'القيمة التقديرية', max_digits=12, decimal_places=2,
        null=True, blank=True
    )
    company_entity = models.CharField('الشركة/الجهة', max_length=255, blank=True)
    # Offer checkboxes
    offer_envap = models.BooleanField('عرض Envap', default=False)
    offer_first = models.BooleanField('عرض أول', default=False)
    offer_second = models.BooleanField('عرض ثان', default=False)
    offer_third = models.BooleanField('عرض ثالث', default=False)
    offer_divisible = models.BooleanField('عرض قابل للتجزئة', default=False)
    # Committee checkboxes
    committee_technical = models.BooleanField('لجنة فنية', default=False)
    committee_legal = models.BooleanField('ش. قانونية', default=False)
    committee_financial = models.BooleanField('ش. مالية', default=False)
    committee_legal_signature = models.BooleanField('توقيع ش. قانونية', default=False)
    committee_supervisor_signature = models.BooleanField('توقيع المشرف', default=False)
    # Other new fields
    memo = models.FileField('مذكرة', upload_to='supplies/buy_orders/memos/%Y/%m/', blank=True)
    supply_order_no = models.CharField('استخراج أمر التوريد رقم', max_length=255, blank=True)
    is_accepted = models.BooleanField('مقبول', default=False)
    attachment = models.FileField(
        'المرفق', upload_to='supplies/buy_orders/%Y/%m/', blank=True
    )
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'طلب شراء'
        verbose_name_plural = 'طلبات الشراء'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requester_name} - {self.supply_channel.name}"


class ServiceOrder(models.Model):
    buy_order = models.ForeignKey(
        BuyOrder, on_delete=models.CASCADE,
        related_name='service_orders', verbose_name='طلب الشراء'
    )
    service_order_no = models.CharField('Service Order No', max_length=255, blank=True)
    date = models.DateField('Date', null=True, blank=True)
    object_description = models.TextField('Object', blank=True)
    reference = models.CharField('Reference', max_length=255, blank=True)
    # To INVAP — multi-select checkboxes
    to_invap_reactor  = models.BooleanField('Al-Reactor / المفاعل', default=False)
    to_invap_fuel     = models.BooleanField('Nuclear Fuel Factory / مصنع الوقود النووي', default=False)
    to_invap_isotopes = models.BooleanField('Radioactive Isotopes Factory / مصنع النظائر المشعة', default=False)
    to_invap_uranium  = models.BooleanField('Uranium Factory / مصنع اليورانيو', default=False)
    description = models.TextField('Description', blank=True)
    signature = models.CharField('The signature', max_length=255, blank=True)
    is_accepted = models.BooleanField('مقبول', default=False)
    attachment = models.FileField(
        'attached', upload_to='supplies/service_orders/%Y/%m/', blank=True
    )
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'أمر خدمة'
        verbose_name_plural = 'أوامر الخدمة'
        ordering = ['-created_at']

    def __str__(self):
        return f"أمر خدمة - {self.buy_order}"


class Offer(models.Model):
    buy_order = models.ForeignKey(
        BuyOrder, on_delete=models.CASCADE,
        related_name='offers', verbose_name='طلب الشراء'
    )
    company_name = models.CharField('اسم الشركة', max_length=255)
    price = models.DecimalField(
        'السعر', max_digits=12, decimal_places=2,
        null=True, blank=True
    )
    description = models.TextField('الوصف', blank=True)
    attachment = models.FileField(
        'المرفق', upload_to='supplies/offers/%Y/%m/'
    )
    is_selected = models.BooleanField('مختار', default=False)
    is_accepted = models.BooleanField('مقبول', default=False)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'عرض'
        verbose_name_plural = 'العروض'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} - {self.buy_order}"


class ContractOperation(models.Model):
    OPERATION_TYPE_CHOICES = [
        ('supplies', 'توريدات'),
        ('maintenance', 'صيانة'),
        ('contracting', 'مقاولات'),
    ]
    ASSIGNMENT_METHOD_CHOICES = [
        ('direct', 'أمر مباشر'),
        ('tender', 'مناقصة'),
        ('', '-'),
    ]

    supply_channel = models.ForeignKey(
        SupplyChannel, on_delete=models.CASCADE,
        related_name='contract_operations', verbose_name='القناة'
    )
    operation_type = models.CharField(
        'نوع العملية', max_length=20, choices=OPERATION_TYPE_CHOICES
    )
    operation_name = models.CharField('اسم العملية', max_length=255)
    contracting_entity = models.CharField('جهة التعاقد', max_length=255, blank=True)
    contract_start_date = models.DateField('تاريخ بداية التعاقد', null=True, blank=True)
    assignment_method = models.CharField(
        'طريقة الإسناد', max_length=20, choices=ASSIGNMENT_METHOD_CHOICES, blank=True
    )
    total_amount = models.DecimalField(
        'المبلغ الإجمالي', max_digits=14, decimal_places=2, null=True, blank=True
    )
    amount_paid = models.DecimalField(
        'المبلغ المدفوع', max_digits=14, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField('ملاحظات', blank=True)
    attachment = models.FileField(
        'المرفق', upload_to='supplies/contract_operations/%Y/%m/', blank=True
    )
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'عملية تعاقد'
        verbose_name_plural = 'عمليات التعاقد'
        ordering = ['operation_type', '-created_at']

    def __str__(self):
        return f"{self.get_operation_type_display()} - {self.operation_name}"

    @property
    def remaining_amount(self):
        total = self.total_amount or 0
        paid = self.amount_paid or 0
        return total - paid


class ATSContract(models.Model):
    buy_order = models.ForeignKey(
        BuyOrder, on_delete=models.CASCADE,
        related_name='ats_contracts', verbose_name='طلب الشراء'
    )
    entity = models.CharField('الجهة', max_length=255)
    supply_order_no = models.CharField('رقم أمر التوريد', max_length=255, blank=True)
    amount_dollar = models.DecimalField(
        'المبلغ بالدولار', max_digits=14, decimal_places=2, null=True, blank=True
    )
    amount_egyptian = models.DecimalField(
        'المبلغ بالمصري', max_digits=14, decimal_places=2, null=True, blank=True
    )
    statement = models.TextField('بيان', blank=True)
    supply_duration = models.CharField('مدة التوريد', max_length=255, blank=True)
    amount_fully_disbursed = models.DecimalField(
        'ما تم صرفه بالكامل', max_digits=14, decimal_places=2, null=True, blank=True
    )
    remaining = models.DecimalField(
        'الباقي', max_digits=14, decimal_places=2, null=True, blank=True
    )
    not_disbursed_current_year = models.DecimalField(
        'ما لم يتم صرفه السنة الحالية', max_digits=14, decimal_places=2, null=True, blank=True
    )
    # Previous years not supplied — checkboxes
    prev_year_2020 = models.BooleanField('2020', default=False)
    prev_year_2021 = models.BooleanField('2021', default=False)
    prev_year_2022 = models.BooleanField('2022', default=False)
    prev_year_2023 = models.BooleanField('2023', default=False)
    prev_year_2024 = models.BooleanField('2024', default=False)
    prev_year_2025 = models.BooleanField('2025', default=False)
    prev_year_2026 = models.BooleanField('2026', default=False)
    attachment = models.FileField(
        'مرفق', upload_to='supplies/ats_contracts/%Y/%m/', blank=True
    )
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'عقد ATS'
        verbose_name_plural = 'عقود ATS'
        ordering = ['-created_at']

    def __str__(self):
        return f"عقد ATS - {self.entity} - {self.buy_order}"


class Tender(models.Model):
    TENDER_TYPE_CHOICES = [
        ('limited', 'محدودة'),
        ('public', 'عامة'),
    ]

    supply_channel = models.ForeignKey(
        SupplyChannel, on_delete=models.CASCADE,
        related_name='tenders', verbose_name='القناة'
    )
    tender_name = models.CharField('اسم المناقصة', max_length=1000)
    formal_inspection_minutes = models.BooleanField('محضر فحص شكلي', default=False)
    formal_inspection_minutes_attachment = models.FileField(
        'مرفق محضر فحص شكلي', upload_to='supplies/tenders/formal_inspection/%Y/%m/', blank=True
    )
    admin_formation_order = models.BooleanField('بأمر إداري تشكيل', default=False)
    admin_formation_order_attachment = models.FileField(
        'مرفق بأمر إداري تشكيل', upload_to='supplies/tenders/admin_formation/%Y/%m/', blank=True
    )
    technical_minutes = models.BooleanField('محضر فني', default=False)
    technical_minutes_attachment = models.FileField(
        'مرفق محضر فني', upload_to='supplies/tenders/technical_minutes/%Y/%m/', blank=True
    )
    minutes_1 = models.BooleanField('محضر 1', default=False)
    minutes_1_attachment = models.FileField(
        'مرفق محضر 1', upload_to='supplies/tenders/minutes_1/%Y/%m/', blank=True
    )
    technical_report = models.BooleanField('تقرير فني', default=False)
    technical_report_attachment = models.FileField(
        'مرفق تقرير فني', upload_to='supplies/tenders/technical_report/%Y/%m/', blank=True
    )
    minutes_2 = models.BooleanField('محضر 2', default=False)
    minutes_2_attachment = models.FileField(
        'مرفق محضر 2', upload_to='supplies/tenders/minutes_2/%Y/%m/', blank=True
    )
    financial_opening = models.BooleanField('فتح مالي', default=False)
    financial_opening_attachment = models.FileField(
        'مرفق فتح مالي', upload_to='supplies/tenders/financial_opening/%Y/%m/', blank=True
    )
    financial_report = models.BooleanField('تقرير مالي', default=False)
    financial_report_attachment = models.FileField(
        'مرفق تقرير مالي', upload_to='supplies/tenders/financial_report/%Y/%m/', blank=True
    )
    minutes_3 = models.BooleanField('محضر 3', default=False)
    minutes_3_attachment = models.FileField(
        'مرفق محضر 3', upload_to='supplies/tenders/minutes_3/%Y/%m/', blank=True
    )
    bid_acceptance_notification = models.BooleanField('إخطار قبول العطاء', default=False)
    bid_acceptance_notification_attachment = models.FileField(
        'مرفق إخطار قبول العطاء', upload_to='supplies/tenders/bid_acceptance/%Y/%m/', blank=True
    )
    # New checkboxes
    linking = models.BooleanField('ارتباط', default=False)
    linking_attachment = models.FileField(
        'مرفق الارتباط', upload_to='supplies/tenders/linking/%Y/%m/', blank=True
    )
    estimated_value_minutes = models.BooleanField('القيمة التقديرية', default=False)
    estimated_value_attachment = models.FileField(
        'مرفق القيمة التقديرية', upload_to='supplies/tenders/estimated_value/%Y/%m/', blank=True
    )
    envelope_opening_minutes = models.BooleanField('محضر فض مظاريف', default=False)
    envelope_opening_attachment = models.FileField(
        'مرفق محضر فض مظاريف', upload_to='supplies/tenders/envelope_opening/%Y/%m/', blank=True
    )
    # Tender / Auction type selection
    tender_type = models.CharField(
        'مناقصات / مزايدات', max_length=20, choices=TENDER_TYPE_CHOICES, blank=True
    )
    tender_type_attachment = models.FileField(
        'مرفق مناقصات / مزايدات', upload_to='supplies/tenders/tender_type/%Y/%m/', blank=True
    )
    attachment = models.FileField(
        'مرفق', upload_to='supplies/tenders/%Y/%m/', blank=True
    )
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'مناقصة'
        verbose_name_plural = 'المناقصات'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tender_name} - {self.supply_channel.name}"


class ChannelPost(models.Model):
    supply_channel = models.ForeignKey(
        SupplyChannel, on_delete=models.CASCADE,
        related_name='posts', verbose_name='القناة'
    )
    name = models.CharField('العنوان', max_length=255)
    date = models.DateField('التاريخ', null=True, blank=True)
    description = models.TextField('الوصف', blank=True)
    attachment = models.FileField(
        'المرفق', upload_to='supplies/posts/%Y/%m/', blank=True
    )
    price = models.DecimalField(
        'السعر', max_digits=12, decimal_places=2,
        null=True, blank=True
    )
    is_accepted = models.BooleanField('مقبول', default=False)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'منشور'
        verbose_name_plural = 'المنشورات'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.supply_channel.name}"
