from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['member_id', 'feedback_body']
        
        # Optionally, you can customize the labels and widgets here
        labels = {
            'member_id': 'Member ID',
            'feedback_body': 'Feedback'
        }
        widgets = {
            'member_id': forms.Select(),  # You can use a select widget if there are many members
            'feedback_body': forms.Textarea(attrs={'rows': 4})
        }