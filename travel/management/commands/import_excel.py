from datetime import datetime, date, timedelta

import openpyxl
from django.core.management.base import BaseCommand

from travel.models import Travel


def parse_date(value):
    """Parse date from various Excel formats."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S'):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
    if isinstance(value, (int, float)):
        try:
            base = date(1899, 12, 30)
            return base + timedelta(days=int(value))
        except (ValueError, OverflowError):
            pass
    return None


class Command(BaseCommand):
    help = 'Import travel records from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to the Excel file')
        parser.add_argument('--clear', action='store_true', help='Clear existing records before import')

    def handle(self, *args, **options):
        filepath = options['filepath']

        if options['clear']:
            deleted, _ = Travel.objects.all().delete()
            self.stdout.write(f'Cleared {deleted} existing records.')

        wb = openpyxl.load_workbook(filepath, data_only=True)
        ws = wb.worksheets[0]

        count = 0
        for row in ws.iter_rows(min_row=9, values_only=True):
            if not row[1]:
                continue

            Travel.objects.create(
                name=str(row[1] or '').strip(),
                title=str(row[2] or '').strip(),
                department=str(row[3] or '').strip(),
                position=str(row[4] or '').strip(),
                course_type=str(row[5] or '').strip(),
                course_name=str(row[6] or '').strip(),
                course_location=str(row[7] or '').strip(),
                date_from=parse_date(row[8]),
                date_to=parse_date(row[9]),
                deadline=parse_date(row[10]),
                followup=str(row[11] or '').strip(),
                event_code=str(row[13] or '').strip(),
                total_travels=str(row[14] or '').strip(),
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} records.'))
