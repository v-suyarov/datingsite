from PIL import Image
from django.conf import settings
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def apply_watermark(image, path_to_watermark):
    watermark = Image.open(os.path.join(settings.BASE_DIR, path_to_watermark))
    watermark = watermark.resize(image.size)

    image.paste(watermark, (0, 0), mask=watermark)

    output = io.BytesIO()
    image.save(output, format='PNG')

    uploaded_file = InMemoryUploadedFile(
        output,
        None,
        'watermarked.png',
        'image/png',
        output.tell,
        None
    )

    return uploaded_file


def send_sympathy_email(evaluating, evaluated):
    context = {
        'first_name_1': evaluated.first_name,
        'last_name_1': evaluated.last_name,
        'email_1': evaluated.email,

        'first_name_2': evaluating.first_name,
        'last_name_2': evaluating.last_name,
        'email_2': evaluating.email,
    }
    html_message = render_to_string('email_mutual_sympathy.html', context)
    return send_mail(
        "Поздравляем! У вас взаимные симпатии!",
        strip_tags(html_message),
        settings.EMAIL_HOST_USER,
        [evaluated.email, evaluating.email],
        fail_silently=False,
        html_message=html_message
        )

