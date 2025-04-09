import os
import qrcode
from django.db import models
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
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

class POSITION_CHOICES(models.TextChoices):
    DIRECTOR = 'DIR', 'Директор'
    DEPUTY_DIRECTOR = 'DDIR', 'Заместитель директора'
    HEAD_OF_DEPARTMENT = 'HOD', 'Начальник отдела'
    MANAGER = 'MGR', 'Менеджер'
    SENIOR_SPECIALIST = 'SSP', 'Ведущий специалист'
    SPECIALIST = 'SPC', 'Специалист'
    JUNIOR_SPECIALIST = 'JSP', 'Младший специалист'
    INTERN = 'INT', 'Стажер'
    STUDENT = 'STD', 'Студент'
    OTHER = 'OTH', 'Другое'




#!models

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Member(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ф. И. О.")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания")
    position = models.CharField(
        max_length=4,
        choices=POSITION_CHOICES.choices,
        verbose_name="Должность",
        default=POSITION_CHOICES.OTHER
    )
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    role = models.IntegerField(choices=ROLE_CHOISES.choices, default=3)
    qr_code = models.ImageField(upload_to='qr_codes/members/', blank=True, null=True)
    registration_time = models.TimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return f"{self.name}  ({self.company})"

    def create_qr_code_with_text(self):
        # Create QR code
        qr_data = f"{self.id}"  # Keep only ID in QR data
        qr = qrcode.make(qr_data)

        width, height = 708, 414  # 6 cm * 300 dpi and 4 cm * 300 dpi
        img = Image.new('RGB', (width, height), 'white')

        # Make QR code slightly smaller to accommodate larger text
        qr_size = (int(width * 0.45), int(width * 0.45))
        qr_pos_x = int((width - qr_size[0]) / 2)
        qr_pos_y = int((height - qr_size[1]) / 2) + 20  # Move QR down a bit
        img.paste(qr.resize(qr_size), (qr_pos_x, qr_pos_y))

        try:
            # Try to use a bold font with larger size for name
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSans-Bold.ttf')
            name_font = ImageFont.truetype(font_path, 48)  # Bigger size for name
        except IOError:
            print("Default font will be used")
            name_font = ImageFont.load_default()

        # Create a drawing context
        draw = ImageDraw.Draw(img)

        # Draw name at the top
        name_text = self.name.upper()  # Make name uppercase
        name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_height = name_bbox[3] - name_bbox[1]
        
        # Position name text higher up
        name_y = 20  # Fixed position from top
        draw.text(
            ((width - name_width) / 2, name_y),
            name_text,
            fill="black",
            font=name_font
        )

        # Create directory if it doesn't exist
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes', 'members')
        if not os.path.exists(qr_dir):
            os.makedirs(qr_dir)

        # Save the image
        qr_image_path = os.path.join(qr_dir, f'member-{self.id}.png')
        img.save(qr_image_path)

        self.qr_code = f'qr_codes/members/member-{self.id}.png'
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        if not self.qr_code:
            self.create_qr_code_with_text()

class Feedback(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="tickets")
    feedback_body = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member_id.name}"



