from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ф. И. О.")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", blank=True)
    email = models.EmailField(unique=True, verbose_name="Email", blank=True)
    company = models.CharField(max_length=200, verbose_name="Компания")
    position = models.CharField(max_length=150, verbose_name="Должность", blank=True)
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        ordering = ['registration_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company})"

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=255, unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="tickets")
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"Ticket {self.ticket_id} for {self.member.first_name} {self.member.last_name}"
