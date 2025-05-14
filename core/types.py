# import hmac
# from datetime import datetime, date
# from importlib import import_module
# from typing import Annotated, Literal
#
# from dateutil.relativedelta import relativedelta
# from django.conf import settings
# from django.utils.timezone import now as django_now
# from jalali_date.templatetags.jalali_tags import datetime2jalali, date2jalali
# from jdatetime import datetime as jdatetime
# from pydantic import AfterValidator, BeforeValidator, StringConstraints, Field
#
# from ..core.utils.datetime import humanize_date, humanize_datetime
#
# TokenType = Annotated[str, StringConstraints(min_length=40, max_length=40, pattern="^[a-z0-9]{40}$")]
#
# DateIn = Annotated[
#     date,
#     BeforeValidator(lambda v: str(jdatetime.strptime(str(v), "%Y/%m/%d").togregorian().date()) if isinstance(v, str) else v),
#     Field(examples=['1403/07/17'])
# ]
# DateOut = Annotated[
#     date,
#     AfterValidator(lambda v: date2jalali(v).strftime("%Y/%m/%d")),
#     Field(examples=['1403/07/17'])
# ]
# DateHumanOut = Annotated[
#     date,
#     AfterValidator(humanize_date),
#     Field(examples=['جمعه، 23 آذر 1403'])
# ]
#
# DateTimeOut = Annotated[
#     datetime,
#     AfterValidator(lambda v: datetime2jalali(v).strftime("%Y/%m/%d %H:%M:%S")),
#     Field(examples=['1403/07/17 07:14:27'])
# ]
# DateTimeHumanOut = Annotated[
#     datetime,
#     AfterValidator(humanize_datetime),
#     Field(examples=['جمعه، 23 آذر 1403 - ساعت 18:39'])
# ]
#
# SlugType = Annotated[str, Field(pattern=r'^[a-z0-9]+(?:[-_][a-z0-9]+)*$')]
# UnicodeSlugType = Annotated[
#     str,
#     Field(pattern=r'^[\p{L}\p{N}]+(?:[-_][\p{L}\p{N}]+)*$')
# ]
#
# TaggitList = Annotated[
#     list[str],
#     BeforeValidator(lambda tags: map(lambda tag: tag.name, tags))  # tags: list[Tag]
# ]
#
# RichText = Annotated[str, Field(None, description='rich text')]
# RichTextUpload = Annotated[str, Field(None, description='rich text upload')]
# Price = Annotated[int, Field(ge=5000, examples=[370000])]
# FreePrice = Annotated[int, Field(ge=0, examples=[370000])]
# PriceWord = Annotated[str, Field(examples=['سیصد و هفتاد هزار'])]
#
# Gender = Literal['male', 'female'] | object
# Age = Annotated[int, Field(ge=5, le=100, examples=[21, 18, 17, 24, 40])]
# Avatar = Annotated[str, Field(..., alias='avatar.url', examples=['https://avatar.iran.liara.run/public/47'])]
#
#
# def birthday_validator(v: date):
#     """
#     Validates that the input date is within the valid range for user age.
#
#     The date must be between the current date minus `MAX_USER_AGE` years
#     and the current date minus `MIN_USER_AGE` years, as defined in
#     `app_settings.MAX_USER_AGE` and `app_settings.MIN_USER_AGE`.
#     """
#     now = django_now().date()
#     if not (now - relativedelta(years=5) <= v <= now - relativedelta(years=100)):
#         raise ValueError(
#             f"The date must be between `5` and `100` years ago."
#         )
#     return v
#
#
# BirthDayIn = Annotated[
#     date,
#     BeforeValidator(lambda v: str(jdatetime.strptime(str(v), "%Y/%m/%d").togregorian().date()) if isinstance(v, str) else v),
#     AfterValidator(birthday_validator),
#     Field(
#         examples=['1384/07/17'],
#         description=f"The date must be between `5` and `100` years ago."
#     ),
# ]
# FirstName = Annotated[str, Field(max_length=100)]
# LastName = Annotated[str, Field(max_length=100)]
# FullName = Annotated[str, Field(max_length=255)]
#
#
# def validate_secret_key(v: str):
#     signature, random_value = v.split(':')
#
#     # Get hash function from environment variables
#     hash_function = getattr(import_module(settings.HMAC_HASH_MODULE), settings.HMAC_HASH_FUNCTION)
#     hmac_key = bytearray(settings.HMAC_KEY.encode())
#
#     # Create signature with "random_value" and the hmac_key
#     new_signature = hmac.new(key=hmac_key, msg=bytearray(random_value.encode()), digestmod=hash_function).hexdigest()
#
#     assert signature == new_signature, "Invalid secret key"
#
#
# UUID4 = Annotated[
#     str,
#     Field(
#         ..., pattern="^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$",
#         max_length=36, examples=['4e229f02-666c-4bd3-a2bf-6d4c30a3e104']
#     )
# ]
#
# SecretKey = Annotated[
#     str,
#     Field(pattern="^[a-zA-Z0-9]+:[a-zA-Z0-9]+$", examples=["signature:random_value"]),
#     AfterValidator(validate_secret_key)
# ]
