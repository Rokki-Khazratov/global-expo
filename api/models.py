import os
import qrcode
from django.db import models
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from PIL import Image, ImageDraw, ImageFont
import qrcode
from django.core.validators import MinValueValidator, MaxValueValidator


#!utils

def upload_audio_to(instance, filename):
    """Формируем имя файла на основе ID участника."""
    ext = filename.split('.')[-1]
    filename = f"audio/member_{instance.member_id.id}.{ext}"
    return os.path.join('audio_feedbacks', filename)

class ROLE_CHOISES(models.IntegerChoices):
    VIP = 1, 'VIP'
    Exhibitor = 2, 'Exhibitor'
    Visitor = 3, 'Visitor'
    NotGived = 4, 'Not gived'

class EXPO_TYPE(models.IntegerChoices):
    Banks = 1, 'Banks&Business'
    UzCharm = 2, 'UzCharmEURASIA'


#!models

class Member(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ф. И. О.")
    expo = models.IntegerField(choices=EXPO_TYPE.choices,default=1)
    company = models.CharField(max_length=200, verbose_name="Компания", blank=True, null=True) 
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True, null=True) 

    position = models.CharField(max_length=250, verbose_name="Должность", blank=True)
    role = models.IntegerField(choices=ROLE_CHOISES.choices,default=3)

    qr_code = models.ImageField(upload_to='qr_codes/members/', blank=True, null=True) 
    registration_time = models.TimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return f"{self.name}  ({self.company})"

    def create_qr_code_with_text(self):
        # Create QR code
        qr_data = f"{self.id}"
        qr = qrcode.make(qr_data)

        width, height = 708, 414  # 6 cm * 300 dpi and 4 cm * 300 dpi
        img = Image.new('RGB', (width, height), 'white')

        qr_size = (int(width * 0.5), int(width * 0.5))  # Maintain the same width for height
        img.paste(qr.resize(qr_size), (int((width - qr_size[0]) / 2), int((height - qr_size[1]) / 2)))  # Center the QR code


        try:
            font = ImageFont.truetype('DejaVuSans-Bold.ttf', 40)  # Use a different bold font
        except IOError:
            print("error")
            font = ImageFont.load_default()

        # Create a drawing context
        draw = ImageDraw.Draw(img)

        # Calculate text size and position
        name_text = self.name
        id_text = str(self.id)

        # Top text
        name_bbox = draw.textbbox((0, 0), name_text, font=font)
        name_width = name_bbox[2] - name_bbox[0]  # width
        draw.text(((width - name_width) / 2, 10), name_text, fill="black", font=font) 

        # Bottom text
        id_bbox = draw.textbbox((0, 0), id_text, font=font)
        id_width = id_bbox[2] - id_bbox[0]  # width
        draw.text(((width - id_width) / 2, height - id_bbox[3] - 10), id_text, fill="black", font=font)  # Centered at the bottom



        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes', 'members')
        if not os.path.exists(qr_dir):
            os.makedirs(qr_dir)

        qr_image_path = os.path.join(qr_dir, f'member-{self.id}.png')
        img.save(qr_image_path)

        self.qr_code = f'qr_codes/members/member-{self.id}.png'
        self.save()


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  

        if not self.qr_code:
            self.create_qr_code_with_text() 

class Bank(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # @property
    # def total_points(self):
    #     """Calculate the total points from related feedback."""
    #     return self.feedback_set.aggregate(total=models.Sum('stars'))['total'] or 0




class Feedback(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="tickets")
    feedback_body = models.TextField(blank=True, null=True)

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.member_id.name}"



