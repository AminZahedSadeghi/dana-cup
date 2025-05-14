import random

from django.conf import settings

fake = settings.FAKE


def generate_random_html_description():
    # Randomly generate various sections
    intro = fake.sentence(nb_words=random.randint(6, 10))
    paragraph_1 = fake.paragraph(nb_sentences=random.randint(4, 6))
    paragraph_2 = fake.paragraph(nb_sentences=random.randint(4, 6))
    list_items = [fake.word() for _ in range(random.randint(3, 6))]

    # Constructing a random HTML description with different tags
    description = f"""
    <h2>{fake.sentence()}</h2>
    <p>{intro}</p>

    <h3>{fake.word().capitalize()} بررسی</h3>
    <p>{paragraph_1}</p>

    <h3>{fake.word().capitalize()} جزئیات</h3>
    <p>{paragraph_2}</p>

    <h3>ویژگی‌های کلیدی</h3>
    <ul>
    """
    for item in list_items:
        description += f"<li>{item}</li>\n"

    description += f"""
    </ul>

    <p><strong>{fake.word().capitalize()} حقایق:</strong> {fake.sentence(nb_words=random.randint(5, 7))}</p>

    <p><em>{fake.sentence(nb_words=random.randint(6, 8))}</em></p>
    """

    return description

