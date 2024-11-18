from django import forms
from .models import  Feedback, Question, RentVehicle, SellVehicle
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text', 'rating']
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

    def init(self, *args, **kwargs):
        super(QuestionForm, self).init(*args, **kwargs)

class SellVehicleForm(forms.ModelForm):
    class Meta:
        model = SellVehicle
        exclude = ['seller']
        
class RentVehicleForm(forms.ModelForm):
    class Meta:
        model = RentVehicle
        exclude = ['owner']