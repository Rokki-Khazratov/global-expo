# api/forms.py

from django import forms
from .models import Member

class FeedbackForm(forms.Form):
    member_id = forms.ChoiceField(
        label='ID Участника',
        choices=[],  # We'll populate this in the view
        widget=forms.Select(attrs={'id': 'member_id'})
    )
    feedback_body = forms.CharField(
        label='Текст отзыва',
        widget=forms.Textarea(attrs={'placeholder': 'Напишите ваш отзыв...'})
    )
    stars = forms.ChoiceField(
        label='Оценка',
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        # Populate the choices dynamically from the database
        self.fields['member_id'].choices = [
            (member.id, f"{member.name} ({member.company}) - {member.id}")
            for member in Member.objects.all()
        ]
