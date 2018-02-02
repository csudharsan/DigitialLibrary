from django import forms
from .models import SoftwareTutorials, Book
from django.contrib.auth.models import User


class SoftwareTutorialsForm(forms.ModelForm):
    
    class Meta:
        model = SoftwareTutorials
        widgets={
            'language_description' : forms.Textarea(attrs={'rows': 4, 'cols': 23}),
            }
        fields = ['language','language_description','creator','lang_logo']
        
        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_title','book_author','pdf_file', 'price']
    


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']