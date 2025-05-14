from datetime import date, datetime
from enum import Enum

from jalali_date.templatetags.jalali_tags import date2jalali, datetime2jalali
from jdatetime import date as jdate, datetime as jdatetime


class FormatsEnum(Enum):
    HOUR_12 = "%b. %d, %Y, %I:%M %p"  # Feb. 09, 2025, 02:30 PM
    SLASHED_DATETIME = "%Y-%m-%d %H:%M"  # 2025-02-09 14:30
    SLASHED_DATE = '%Y/%m/%d'  # 2025/02/09


def humanize_date(input_date: date | datetime | jdate | jdatetime) -> str:
    """
        Converts a date, datetime, jdatetime or jdate to a human-readable string.
        Handles both Gregorian and Jalali (Shamsi) dates.
    """
    # If it's a datetime or jdatetime  object, convert to date
    if isinstance(input_date, datetime) or isinstance(input_date, jdatetime):
        input_date = input_date.date()

    # Handle Gregorian (normal) dates
    if isinstance(input_date, date):
        input_date = date2jalali(input_date)

    # Handle Jalali (Shamsi) dates
    if isinstance(input_date, jdate):
        month_fa = jdate.j_months_fa[input_date.month - 1]
        weekday_fa = jdate.j_weekdays_fa[input_date.weekday()]

        return f"{weekday_fa}، {input_date.day} {month_fa} {input_date.year}"

    raise ValueError("Unsupported date type")


def humanize_datetime(input_datetime: datetime | jdatetime):
    """
        Converts a datetime or jdatetime to a human-readable string.
        Handles both Gregorian and Jalali (Shamsi) dates.
    """
    if isinstance(input_datetime, datetime):
        input_datetime = datetime2jalali(input_datetime)

    if isinstance(input_datetime, jdatetime):
        jtime = input_datetime.time()
        humanized_date = humanize_date(input_datetime)
        return humanized_date + f" - ساعت {jtime.hour}:{jtime.minute}"

    raise ValueError("Unsupported datetime type")


def format_datetime(dt: datetime | jdatetime, format_: FormatsEnum = FormatsEnum.HOUR_12, jalali=True) -> str:
    if isinstance(dt, datetime) and jalali:
        dt = datetime2jalali(dt)

    return dt.strftime(format_.value)
