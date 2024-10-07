import os
import qrcode
from django.db import models
from django.conf import settings

def upload_audio_to(instance, filename):
    """Формируем имя файла на основе ID участника."""
    ext = filename.split('.')[-1]
    filename = f"audio/member_{instance.member_id.id}.{ext}"
    return os.path.join('audio_feedbacks', filename)

class ROLE_CHOISES(models.IntegerChoices):
    JANUARY = 1, 'VIP'
    FEBRUARY = 2, 'Exhibitor'
    MARCH = 3, 'Visitor'


class Member(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ф. И. О.")
    email = models.EmailField(unique=True, verbose_name="Email")
    company = models.CharField(max_length=200, verbose_name="Компания")
    position = models.CharField(max_length=150, verbose_name="Должность", blank=True)
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    qr_code = models.ImageField(upload_to='qr_codes/members/', blank=True, null=True) 
    role = models.IntegerField(choices=ROLE_CHOISES.choices,default=3)

    # class Meta:
    #     verbose_name = "Участник"
    #     verbose_name_plural = "Участники"
    #     ordering = ['registration_date']

    def __str__(self):
        return f"{self.name}  ({self.company})"

    def save(self, *args, **kwargs):
        # Сохраняем объект для получения ID
        super().save(*args, **kwargs)

        # Если QR-код еще не был сгенерирован, создаём его
        if not self.qr_code:
            # Формат данных для QR-кода: member-{self.id}-ticket
            qr_data = f"{self.id}"
            
            # Путь для сохранения QR-кода
            qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes', 'members')
            qr_image_path = os.path.join(qr_dir, f'member-{self.id}.png')

            # Убедимся, что директория существует
            if not os.path.exists(qr_dir):
                os.makedirs(qr_dir)

            # Генерация QR-кода с использованием вышеуказанного формата данных
            qr = qrcode.make(qr_data)
            qr.save(qr_image_path)

            # Сохраняем путь к изображению в поле `qr_code`
            self.qr_code = f'qr_codes/members/member-{self.id}.png'

            # Сохраняем изменения в базе данных
            super().save(*args, **kwargs)



class Feedback(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="tickets")
    feedback_body= models.TextField(blank=True, null=True)
    audio_feedback = models.FileField(upload_to=upload_audio_to, blank=True, null=True)  # Используем функцию для именования файлов

    #!voice


    def __str__(self):
        return f"{self.member_id.name}"


