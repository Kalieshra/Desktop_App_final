from django.db import models
from decimal import Decimal


def _dec(**kwargs):
    return models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0'), blank=True, **kwargs)


class InvestmentPlan(models.Model):
    name = models.CharField('اسم الخطة', max_length=255)

    # ── 1. الأراضي والمباني ──────────────────────────────────────
    lands_project = _dec(verbose_name='أراضي - بيان المشروع')
    lands_original = _dec(verbose_name='أراضي - الخطة الأصلية')
    lands_modified = _dec(verbose_name='أراضي - الخطة المعدلة')

    residential_buildings_project = _dec(verbose_name='مباني سكنية - بيان المشروع')
    residential_buildings_original = _dec(verbose_name='مباني سكنية - الخطة الأصلية')
    residential_buildings_modified = _dec(verbose_name='مباني سكنية - الخطة المعدلة')

    non_residential_buildings_project = _dec(verbose_name='مباني غير سكنية - بيان المشروع')
    non_residential_buildings_original = _dec(verbose_name='مباني غير سكنية - الخطة الأصلية')
    non_residential_buildings_modified = _dec(verbose_name='مباني غير سكنية - الخطة المعدلة')

    # ── 2. التشييدات ─────────────────────────────────────────────
    constructions_project = _dec(verbose_name='تشييدات - بيان المشروع')
    constructions_original = _dec(verbose_name='تشييدات - الخطة الأصلية')
    constructions_modified = _dec(verbose_name='تشييدات - الخطة المعدلة')

    # ── 3. الآلات والمعدات ───────────────────────────────────────
    machinery_local_project = _dec(verbose_name='آلات محلي - بيان المشروع')
    machinery_local_original = _dec(verbose_name='آلات محلي - الخطة الأصلية')
    machinery_local_modified = _dec(verbose_name='آلات محلي - الخطة المعدلة')

    machinery_foreign_project = _dec(verbose_name='آلات أجنبي - بيان المشروع')
    machinery_foreign_original = _dec(verbose_name='آلات أجنبي - الخطة الأصلية')
    machinery_foreign_modified = _dec(verbose_name='آلات أجنبي - الخطة المعدلة')

    machinery_self_financed_project = _dec(verbose_name='تمويل ذاتي - بيان المشروع')
    machinery_self_financed_original = _dec(verbose_name='تمويل ذاتي - الخطة الأصلية')
    machinery_self_financed_modified = _dec(verbose_name='تمويل ذاتي - الخطة المعدلة')

    # ── 4. النقل والأثاث ─────────────────────────────────────────
    transport_means_project = _dec(verbose_name='وسائل نقل - بيان المشروع')
    transport_means_original = _dec(verbose_name='وسائل نقل - الخطة الأصلية')
    transport_means_modified = _dec(verbose_name='وسائل نقل - الخطة المعدلة')

    furniture_equipment_project = _dec(verbose_name='أثاث وتجهيزات - بيان المشروع')
    furniture_equipment_original = _dec(verbose_name='أثاث وتجهيزات - الخطة الأصلية')
    furniture_equipment_modified = _dec(verbose_name='أثاث وتجهيزات - الخطة المعدلة')

    livestock_project = _dec(verbose_name='ثروة حيوانية - بيان المشروع')
    livestock_original = _dec(verbose_name='ثروة حيوانية - الخطة الأصلية')
    livestock_modified = _dec(verbose_name='ثروة حيوانية - الخطة المعدلة')

    transport_subtotal_project = _dec(verbose_name='جملة النقل والأثاث - بيان المشروع')
    transport_subtotal_original = _dec(verbose_name='جملة النقل والأثاث - الخطة الأصلية')
    transport_subtotal_modified = _dec(verbose_name='جملة النقل والأثاث - الخطة المعدلة')

    # ── 5. تجهيزات وأبحاث ───────────────────────────────────────
    setup_preparations_project = _dec(verbose_name='تجهيزات - بيان المشروع')
    setup_preparations_original = _dec(verbose_name='تجهيزات - الخطة الأصلية')
    setup_preparations_modified = _dec(verbose_name='تجهيزات - الخطة المعدلة')

    transport_travel_expenses_project = _dec(verbose_name='وسائل نقل وانتقال - بيان المشروع')
    transport_travel_expenses_original = _dec(verbose_name='وسائل نقل وانتقال - الخطة الأصلية')
    transport_travel_expenses_modified = _dec(verbose_name='وسائل نقل وانتقال - الخطة المعدلة')

    research_studies_project = _dec(verbose_name='أبحاث ودراسات - بيان المشروع')
    research_studies_original = _dec(verbose_name='أبحاث ودراسات - الخطة الأصلية')
    research_studies_modified = _dec(verbose_name='أبحاث ودراسات - الخطة المعدلة')

    setup_subtotal_project = _dec(verbose_name='جملة التجهيزات - بيان المشروع')
    setup_subtotal_original = _dec(verbose_name='جملة التجهيزات - الخطة الأصلية')
    setup_subtotal_modified = _dec(verbose_name='جملة التجهيزات - الخطة المعدلة')

    # ── 6. الإجماليات ────────────────────────────────────────────
    total_fixed_investment_project = _dec(verbose_name='جملة الاستثمار الثابت - بيان المشروع')
    total_fixed_investment_original = _dec(verbose_name='جملة الاستثمار الثابت - الخطة الأصلية')
    total_fixed_investment_modified = _dec(verbose_name='جملة الاستثمار الثابت - الخطة المعدلة')

    advance_payments_project = _dec(verbose_name='دفعات مقدمة واعتمادات مستندية - بيان المشروع')
    advance_payments_original = _dec(verbose_name='دفعات مقدمة واعتمادات مستندية - الخطة الأصلية')
    advance_payments_modified = _dec(verbose_name='دفعات مقدمة واعتمادات مستندية - الخطة المعدلة')

    grand_total_project = _dec(verbose_name='إجمالي الاستثمارات - بيان المشروع')
    grand_total_original = _dec(verbose_name='إجمالي الاستثمارات - الخطة الأصلية')
    grand_total_modified = _dec(verbose_name='إجمالي الاستثمارات - الخطة المعدلة')

    # ── 7. حقول إضافية ───────────────────────────────────────────
    manqool_minh_project = _dec(verbose_name='منقول منه - بيان المشروع')
    manqool_minh_original = _dec(verbose_name='منقول منه - الخطة الأصلية')
    manqool_minh_modified = _dec(verbose_name='منقول منه - الخطة المعدلة')

    manqool_ilaih_project = _dec(verbose_name='منقول اليه - بيان المشروع')
    manqool_ilaih_original = _dec(verbose_name='منقول اليه - الخطة الأصلية')
    manqool_ilaih_modified = _dec(verbose_name='منقول اليه - الخطة المعدلة')

    nisbat_munaffaz_project = _dec(verbose_name='نسبه المنفذ - بيان المشروع')
    nisbat_munaffaz_original = _dec(verbose_name='نسبه المنفذ - الخطة الأصلية')
    nisbat_munaffaz_modified = _dec(verbose_name='نسبه المنفذ - الخطة المعدلة')

    mutayyiqas_project = _dec(verbose_name='المتيقى - بيان المشروع')
    mutayyiqas_original = _dec(verbose_name='المتيقى - الخطة الأصلية')
    mutayyiqas_modified = _dec(verbose_name='المتيقى - الخطة المعدلة')

    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'خطة استثمار'
        verbose_name_plural = 'خطط الاستثمار'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_section_groups(self):
        """Return the matrix data grouped by section for template rendering."""
        hundred = Decimal('100')

        def row(label, key, is_subtotal=False):
            p = getattr(self, f'{key}_project')
            o = getattr(self, f'{key}_original')
            m = getattr(self, f'{key}_modified')
            if key == 'nisbat_munaffaz':
                # Stored as a percentage; display the resolved amount.
                grand_o = self.grand_total_original or Decimal('0')
                grand_m = self.grand_total_modified or Decimal('0')
                disp_o = (o or Decimal('0')) / hundred * grand_o
                disp_m = (m or Decimal('0')) / hundred * grand_m
                return {
                    'label': f'{label} ({o or 0}% / {m or 0}%)',
                    'key': key,
                    'project': p,
                    'original': disp_o.quantize(Decimal('0.01')),
                    'modified': disp_m.quantize(Decimal('0.01')),
                    'difference': (disp_o - disp_m).quantize(Decimal('0.01')),
                    'is_subtotal': is_subtotal,
                }
            return {
                'label': label,
                'key': key,
                'project': p,
                'original': o,
                'modified': m,
                'difference': o - m,
                'is_subtotal': is_subtotal,
            }

        return [
            {
                'section_label': 'الأراضي والمباني',
                'rows': [
                    row('أراضي', 'lands'),
                    row('مباني سكنية', 'residential_buildings'),
                    row('مباني غير سكنية', 'non_residential_buildings'),
                ],
            },
            {
                'section_label': 'التشييدات',
                'rows': [
                    row('تشييدات', 'constructions'),
                ],
            },
            {
                'section_label': 'الآلات والمعدات',
                'rows': [
                    row('محلي', 'machinery_local'),
                    row('أجنبي', 'machinery_foreign'),
                    row('تمويل ذاتي', 'machinery_self_financed'),
                ],
            },
            {
                'section_label': 'النقل والأثاث',
                'rows': [
                    row('وسائل نقل', 'transport_means'),
                    row('أثاث وتجهيزات', 'furniture_equipment'),
                    row('ثروة حيوانية', 'livestock'),
                    row('جملة', 'transport_subtotal', is_subtotal=True),
                ],
            },
            {
                'section_label': 'تجهيزات وأبحاث',
                'rows': [
                    row('تجهيزات', 'setup_preparations'),
                    row('وسائل نقل وانتقال', 'transport_travel_expenses'),
                    row('أبحاث ودراسات', 'research_studies'),
                    row('جملة', 'setup_subtotal', is_subtotal=True),
                ],
            },
            {
                'section_label': 'الإجماليات',
                'rows': [
                    row('جملة الاستثمار الثابت', 'total_fixed_investment', is_subtotal=True),
                    row('دفعات مقدمة واعتمادات مستندية', 'advance_payments'),
                    row('إجمالي الاستثمارات', 'grand_total', is_subtotal=True),
                ],
            },
        ]


MANQOOL_SOURCE_FIELD_CHOICES = [
    ('lands', 'أراضي (Lands)'),
    ('residential_buildings', 'مباني سكنية (Residential Buildings)'),
    ('non_residential_buildings', 'مباني غير سكنية (Non-residential Buildings)'),
    ('constructions', 'تشييدات (Constructions/Infrastructure)'),
    ('machinery_local', 'محلي (Local)'),
    ('machinery_foreign', 'أجنبي (Foreign)'),
    ('machinery_self_financed', 'تمويل ذاتي (Self-financed)'),
    ('transport_means', 'وسائل نقل (Means of Transport)'),
    ('furniture_equipment', 'أثاث وتجهيزات (Furniture & Equipment)'),
    ('livestock', 'ثروة حيوانية (Livestock)'),
    ('setup_preparations', 'تجهيزات (Setup/Technical Preparations)'),
    ('transport_travel_expenses', 'وسائل نقل وانتقال (Travel Expenses)'),
    ('research_studies', 'أبحاث ودراسات (Research & Studies)'),
    ('advance_payments', 'دفعات مقدمة (Advance Payments)'),
]


class ManqoolMinhEntry(models.Model):
    plan = models.ForeignKey(
        InvestmentPlan,
        on_delete=models.CASCADE,
        related_name='manqool_minh_entries',
        verbose_name='الخطة',
    )
    source_field = models.CharField(
        'الحقل المصدر',
        max_length=64,
        choices=MANQOOL_SOURCE_FIELD_CHOICES,
    )
    main_value = models.DecimalField(
        'القيمة الأساسية',
        max_digits=14, decimal_places=2, default=Decimal('0'),
    )
    order = models.PositiveIntegerField('الترتيب', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'سجل منقول منه'
        verbose_name_plural = 'سجلات منقول منه'

    @property
    def chosen_modified(self):
        return getattr(self.plan, f'{self.source_field}_modified', Decimal('0')) or Decimal('0')

    @property
    def difference(self):
        return (self.main_value or Decimal('0')) - self.chosen_modified

    def __str__(self):
        return f'{self.get_source_field_display()} = {self.main_value}'
