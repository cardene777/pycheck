from django import forms
from PIL import Image
from .models import QuestionModel, Comment

class UploodImgForm(forms.ModelForm):

    class Meta:
        model = QuestionModel
        fields = ('title', 'content', 'idea', 'category', 'level','image_1', 'image_2', 'image_3', 'image_4',)
    
class CategoryForm(forms.Form):
    choice1 = forms.fields.ChoiceField(
        required=True,
        widget=forms.widgets.Select
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'comment',
        )