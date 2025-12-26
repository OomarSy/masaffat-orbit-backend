from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

from decimal import Decimal

from ..models import Overtime
from apps.attendance.utils import ensure_aware


class OvertimeService:

    @staticmethod
    def validate_entries(user, entries):
        errors = []
        now = timezone.now()

        validated_ranges = []  # (index, start_dt, end_dt)

        for idx, entry in enumerate(entries):
            start_dt = ensure_aware(
                datetime.combine(entry['start_date'], entry['start_time'])
            )
            end_dt = ensure_aware(
                datetime.combine(entry['end_date'], entry['end_time'])
            )

            if start_dt >= end_dt:
                errors.append({
                    "index": idx,
                    "message": "وقت البدء يجب أن يكون قبل وقت الانتهاء."
                })
                continue

            if end_dt > now:
                errors.append({
                    "index": idx,
                    "message": "لا يمكن تسجيل دوام إضافي في المستقبل."
                })
                continue

            if Overtime.objects.filter(
                user=user,
                start_datetime__lt=end_dt,
                end_datetime__gt=start_dt
            ).exists():
                errors.append({
                    "index": idx,
                    "message": "توجد فترة متداخلة مع دوام إضافي مسجل مسبقًا."
                })
                continue

            conflict = False
            for prev_idx, prev_start, prev_end in validated_ranges:
                if start_dt < prev_end and end_dt > prev_start:
                    errors.append({
                        "index": idx,
                        "message": f"توجد فترة متداخلة مع الإدخال رقم {prev_idx + 1} في نفس الطلب."
                    })
                    conflict = True
                    break

            if conflict:
                continue

            validated_ranges.append((idx, start_dt, end_dt))

        return errors

    
    @staticmethod
    def create_overtime(user, entries):
        created = []

        for entry in entries:
            start_dt = ensure_aware(
                datetime.combine(entry['start_date'], entry['start_time'])
            )
            end_dt = ensure_aware(
                datetime.combine(entry['end_date'], entry['end_time'])
            )

            delta = end_dt - start_dt
            hours = Decimal(round(delta.total_seconds() / 3600, 2))

            overtime = Overtime.objects.create(
                user=user,
                start_datetime=start_dt,
                end_datetime=end_dt,
                hours=hours,
                note=entry.get("note", "")
            )

            created.append({
                "id": overtime.id,
                "start_datetime": overtime.start_datetime.isoformat(),
                "end_datetime": overtime.end_datetime.isoformat(),
                "hours": float(hours),
                "note": overtime.note
            })

        return created

class ListOvertimeService:

    @staticmethod
    def get_user_overtimes(user, from_date=None, to_date=None):
        """
        جلب أوقات العمل الإضافي لمستخدم محدد بين تاريخين.
        إذا لم يتم تمرير التاريخين، سيتم إرجاع آخر شهرين.
        يمكن تمرير from_date و to_date بصيغة 'YYYY-MM-DD'.
        """

        # إذا لم يتم تمرير التواريخ: آخر شهرين
        if not from_date and not to_date:
            to_dt = timezone.now()
            from_dt = to_dt - relativedelta(months=2)
        else:
            # تحويل from_date إلى بداية اليوم
            if from_date:
                from_dt = make_aware(datetime.fromisoformat(from_date))
            else:
                from_dt = None

            # تحويل to_date إلى نهاية اليوم
            if to_date:
                to_dt_raw = datetime.fromisoformat(to_date) + timedelta(days=1) - timedelta(seconds=1)
                to_dt = make_aware(to_dt_raw)
            else:
                to_dt = None

        # بناء الـ queryset
        qs = Overtime.objects.filter(user=user)
        if from_dt:
            qs = qs.filter(start_datetime__gte=from_dt)
        if to_dt:
            qs = qs.filter(end_datetime__lte=to_dt)

        return qs