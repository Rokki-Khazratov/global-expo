from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['member_id', 'feedback_body']  # Удаляем 'audio_feedback'
        
        labels = {
            'member_id': 'ID Участника',
            'feedback_body': 'Текст отзыва',
        }