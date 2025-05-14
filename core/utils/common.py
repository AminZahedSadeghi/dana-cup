import random

from typing import Literal

from django.contrib.humanize.templatetags.humanize import intcomma
from django.shortcuts import reverse
from django.urls import URLResolver, URLPattern
from django.urls import get_resolver
from pydantic import Field, create_model, BaseModel


def create_exception_schema(cls_name: str, message: str, description: str = None) -> BaseModel:
    return create_model(
        cls_name,
        detail=(str, Field(example=message, description=description))
    )


def get_format_file_size(bytes_) -> tuple[int | float, Literal['MB', 'KB']]:
    kb = bytes_ / 1024  # Convert bytes to KB
    if kb >= 1024:  # If the size is greater than or equal to 1024 KB (1 MB)
        return round(kb / 1024, 1), 'MB'  # Convert KB to MB and return as a float with 1 decimal place
    else:
        return round(kb), 'KB'  # Return the size in KB as a float (rounded to whole number)


def get_video_metadata(file_path: str) -> dict:
    """Get duration of video in either second or minute"""
    with VideoFileClip(file_path) as video:
        duration = round(video.duration)
        width, height = video.size
        video_metadata = dict(
            duration_in_second=duration,
            duration_in_minute=round(duration / 60),
            fps=int(video.fps),
            resolution=f"{width}x{height}"
        )

    return video_metadata


def translate_number(value):
    """If language is farsi, then translate the number, otherwise return the actual number."""

    value = str(value)
    english_to_persian_table = value.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return value.translate(intcomma(english_to_persian_table))


def ninja_reverse(url_name: str, args=None, kwargs=None):
    args = args or []  # Ensure args is a list or tuple
    kwargs = kwargs or {}  # Ensure kwargs is a dictionary
    return reverse(f'dana_cup:{url_name}', args=args, kwargs=kwargs)


def get_api_endpoint_names(namespace="dana_cup") -> list[str]:
    """
        Return a list of url patterns that are related to a specific namespace
        Example: ['profile@full_information', 'sheet_music@list']
    """

    urlpatterns = get_resolver().url_patterns
    for url_resolver in urlpatterns:  # type: URLResolver
        if url_resolver.namespace == namespace:
            # TODO: Do we need to add naghmegar# ?!
            return [url_pattern.name for url_pattern in url_resolver.url_patterns]  # type: URLPattern


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


DATE_REGEX = r"(\d{4})/(0?[1-9]|1[0-2])/(0?[1-9]|[12]\d|3[01])"

TQDM_COLOURS = ['RED', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']
# get_tqdm_color = lambda: 'RED'
get_tqdm_color = lambda: str(random.choice(TQDM_COLOURS))
