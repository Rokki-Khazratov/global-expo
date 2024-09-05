from django.db import models

class Participant(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    company = models.CharField(max_length=200, verbose_name="Компания")
    position = models.CharField(max_length=150, verbose_name="Должность")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        ordering = ['registration_date']  # Сортировка по дате регистрации

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company})"
