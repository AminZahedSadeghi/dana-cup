import re


def convert_to_snake_case(s):
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', s).lower()
