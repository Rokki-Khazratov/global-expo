import os
import qrcode
from django.db import models
from django.conf import settings

class Member(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ф. И. О.")
    email = models.EmailField(unique=True, verbose_name="Email")
    company = models.CharField(max_length=200, verbose_name="Компания")
    position = models.CharField(max_length=150, verbose_name="Должность", blank=True)
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    qr_code = models.ImageField(upload_to='qr_codes/members/', blank=True, null=True)  # Поле для QR-кода

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        ordering = ['registration_date']

    def __str__(self):
        return f"{self.first_name}  ({self.company})"

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


class Ticket(models.Model):
    ticket_id = models.CharField(max_length=255, unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="tickets")
    is_valid = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='qr_codes/tickets/', blank=True, null=True)  # Поле для QR-кода

    def __str__(self):
        return f"Ticket {self.ticket_id} for {self.member.first_name} {self.member.last_name}"
