import random
from django.db import models
import qrcode
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO
from django.core.files import File


class BinsStats(models.Model):
    BinID = models.CharField(max_length=6, unique=True)
    status = models.CharField(max_length=4, blank=True,null=True)
    refreshStats = models.CharField(max_length=4, blank=True)
    lastRefresh = models.DateField(blank=True)
    fillUp = models.IntegerField(blank=True)
    Lat = models.CharField(blank=True, null=True,max_length=100)
    Lon = models.CharField(blank=True, null=True,max_length=100)
    Area = models.CharField(max_length=200, blank=True)
    City = models.CharField(max_length=200,blank=True)

class BINQRs(models.Model):
    data = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='qrcode', blank=True)

    def save(self, *args, **kwargs):
        # Ensure that the image field is not empty before saving
        if not self.image:
            self.generate_qr_code()

        super().save(*args, **kwargs)

    def generate_qr_code(self):
        qr_code = qrcode.make(self.data)
        canvas = Image.new("RGB", (400, 400), "white")
        canvas.paste(qr_code)
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default()  # You can load a specific font if needed
        text = f'{self.data}'
        text_color = "black"
        draw.text((50, 350), text, font=font, fill=text_color)
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.image.save(f'image{random.randint(1, 9999999)}.png', File(buffer), save=False)
        canvas.close()