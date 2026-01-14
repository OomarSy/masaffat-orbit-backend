# fill_overtime_date.py
import os
import django
from django.utils.timezone import localtime

from django.utils.timezone import make_aware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.overtime.models import EmployeeOvertime

# استرجاع جميع السجلات التي date فيها فارغ
overtimes = EmployeeOvertime.objects.filter(date__isnull=True)
print(f"Found {overtimes.count()} records with empty date.")

for ot in overtimes:
    ot.date = localtime(ot.start_datetime).date()  # استخدام تاريخ بداية الدوام
    ot.save(update_fields=['date'])

print("Done updating date field for all records.")
