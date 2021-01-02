from django import forms
from . models import Comment,Post
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","password1",'password2')

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username","password")    
          

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            "content": "Your comment"
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('description',)

        widgets = {
            'description': forms.Textarea(attrs={'class':'col-100'}),
        }
