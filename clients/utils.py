from PIL import Image
from django.conf import settings
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
import io


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
