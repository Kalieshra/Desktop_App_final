from decimal import Decimal
from django.db import models


CHAPTER_COUNT = 6
CHAPTER_CHOICES = [(i, f'باب {i}') for i in range(1, CHAPTER_COUNT + 1)]


def _money(**kwargs):
    return models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0'),
        blank=True,
        **kwargs,
    )


class Budget(models.Model):
    name = models.CharField('اسم الميزانية', max_length=255)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التعديل', auto_now=True)

    class Meta:
        verbose_name = 'ميزانية'
        verbose_name_plural = 'الميزانيات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def ensure_chapters(self):
        """Make sure all 6 chapters exist for this budget."""
        existing = set(self.chapters.values_list('chapter_number', flat=True))
        missing = [i for i in range(1, CHAPTER_COUNT + 1) if i not in existing]
        for num in missing:
            BudgetChapter.objects.create(budget=self, chapter_number=num)

    @property
    def total_allocated(self):
        return sum((c.allocated for c in self.chapters.all()), Decimal('0'))

    @property
    def total_reinforcement(self):
        return sum((c.reinforcement for c in self.chapters.all()), Decimal('0'))

    @property
    def total_commitment(self):
        return sum((c.commitment for c in self.chapters.all()), Decimal('0'))

    @property
    def total_expenditure(self):
        return sum((c.expenditure for c in self.chapters.all()), Decimal('0'))

    @property
    def total_remaining(self):
        return (
            self.total_allocated
            + self.total_reinforcement
            + self.total_commitment
            - self.total_expenditure
        )


class BudgetChapter(models.Model):
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name='chapters',
        verbose_name='الميزانية',
    )
    chapter_number = models.PositiveSmallIntegerField('رقم الباب', choices=CHAPTER_CHOICES)
    allocated = _money(verbose_name='المبلغ الموزع')
    reinforcement = _money(verbose_name='تعزيز')
    commitment = _money(verbose_name='ارتباط')
    expenditure = _money(verbose_name='صرف')

    class Meta:
        verbose_name = 'باب ميزانية'
        verbose_name_plural = 'أبواب الميزانية'
        ordering = ['chapter_number']
        unique_together = [('budget', 'chapter_number')]

    def __str__(self):
        return f'{self.budget.name} - باب {self.chapter_number}'

    @property
    def remaining(self):
        return (
            (self.allocated or Decimal('0'))
            + (self.reinforcement or Decimal('0'))
            + (self.commitment or Decimal('0'))
            - (self.expenditure or Decimal('0'))
        )
