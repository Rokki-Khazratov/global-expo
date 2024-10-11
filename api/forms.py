from django import forms
from .models import Feedback

# forms.py
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['member_id', 'feedback_body']  # Убрал 'audio_feedback'

        labels = {
            'member_id': 'ID Участника',
            'feedback_body': 'Текст отзыва',
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['member_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['feedback_body'].widget.attrs.update({'class': 'form-control'})

